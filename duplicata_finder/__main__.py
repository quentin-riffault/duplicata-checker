import argparse
from pathlib import Path
from os import mkdir
from shutil import move
from typing import Sequence

from duplicata_finder.deduplicata import DeDuplicata
from duplicata_finder.libs.explorers.walk_explorer import WalkExplorer
from duplicata_finder.libs.features.feature_md5 import FeatureMD5
from duplicata_finder.libs.stores.in_memory_storage import InMemoryStorage

DEFAULT_CONFINE_OUTPUT_PATH = Path("duplicata-checker-output")


def move_duplicates(
    files_to_move: Sequence[str | Path], output_directory: Path, dry_run: bool = False
):
    print("Déplacement des duplicas")
    current_file_output_dir = Path(output_directory, Path(files_to_move[0]).name)
    if not dry_run:
        mkdir(current_file_output_dir)

    for idx, file in enumerate(files_to_move):
        dst = Path(current_file_output_dir, f"{idx}-{Path(file).name}")
        print(f"Déplacement de {file} vers {dst}")
        if not dry_run:
            move(file, dst)


def find_duplicates(
    input_directory: Path,
    output_directory: Path | None = None,
    confine: bool = False,
    dry_run: bool = False,
):

    duplicata_checker = DeDuplicata(input_directory)
    to_process = duplicata_checker.discover(WalkExplorer)
    print(f"{to_process} éléments à traiter.")

    print("Calcul des hashes")

    hash_storage = InMemoryStorage()

    duplicata_checker.compute_features(FeatureMD5, hash_storage)

    already_found_duplicates: set[str] = set()

    if output_directory is None:
        output_directory = DEFAULT_CONFINE_OUTPUT_PATH

    if confine:
        print(f"Mode confinement activé. Répertoire de sortie : {output_directory}")
        if not dry_run:
            mkdir(output_directory)

    # Identification des duplicas
    for item in hash_storage:
        current_item_duplicates: list[str] = []

        if item.filename in already_found_duplicates:
            continue

        for found_item in hash_storage.find_all_duplicates(item):
            already_found_duplicates.add(found_item.filename)
            current_item_duplicates.append(found_item.filename)

            print(f"Duplica trouvé : [{item.filename}] -> [{found_item.filename}]")

        if confine and len(current_item_duplicates) >= 1:
            current_item_duplicates.insert(0, item.filename)
            move_duplicates(current_item_duplicates, output_directory, dry_run)


def main():

    parser = argparse.ArgumentParser(
        prog="duplicata_finder",
        description="Détecte les duplicas d'images dans une arborescence",
    )

    parser.add_argument(
        "-d",
        "--directory",
        required=True,
        type=Path,
        help="Répertoire où trouver les duplicas récursivement",
    )
    parser.add_argument(
        "-o", "--output_directory", type=Path, help="Répertoire de sortie si applicable"
    )
    parser.add_argument(
        "-c",
        "--confine",
        action="store_true",
        help=(
            "Mode confinement. Déplace les duplicas et l'image originale dans "
            "le répertoire de sortie."
        ),
    )
    parser.add_argument(
        "--dry_run",
        action="store_true",
        help="Mode de test. Ne réalise aucune action définitive sur le système de fichier.",
    )

    args = parser.parse_args()

    find_duplicates(args.directory, args.output_directory, args.confine, args.dry_run)


if __name__ == "__main__":
    main()
