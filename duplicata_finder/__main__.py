import argparse
from pathlib import Path

from duplicata_finder.deduplicata import DeDuplicata
from duplicata_finder.libs.explorers.walk_explorer import WalkExplorer
from duplicata_finder.libs.features.feature_md5 import FeatureMD5
from duplicata_finder.libs.stores.in_memory_storage import InMemoryStorage

def main():

    parser = argparse.ArgumentParser(
        prog="duplicata_finder",
        description="Détecte les duplicas d'images dans une arborescence",
    )

    parser.add_argument("-d", "--directory", required=True, type=Path)

    args = parser.parse_args()

    duplicata_checker = DeDuplicata(args.directory)
    print("{} éléments à traiter.".format(duplicata_checker.discover(WalkExplorer)))

    print("Calcul des hashes")

    hash_storage = InMemoryStorage()

    duplicata_checker.compute_features(FeatureMD5, hash_storage)

    already_found_duplicates: set[str] = set()

    # Identification des duplicas
    for item in hash_storage:

        if item.filename in already_found_duplicates:
            continue

        for found_item in hash_storage.find_all_duplicates(item):
            already_found_duplicates.add(found_item.filename)

            print("Duplica trouvé : [{}] -> [{}]".format(item.filename, found_item.filename))

if __name__ == "__main__":
    main()
