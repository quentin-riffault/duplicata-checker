import argparse
from pathlib import Path

from core.deduplicata import DeDuplicata
from core.libs.explorers.walk_explorer import WalkExplorer

def main():

    parser = argparse.ArgumentParser(
        prog="detecto-duplicata",
        description="Détecte les duplicas d'images dans une arborescence",
    )

    parser.add_argument("-d", "--directory", required=True, type=Path)

    args = parser.parse_args()

    duplicata_checker = DeDuplicata(args.directory)
    print("{} éléments à traiter.".format(duplicata_checker.discover(WalkExplorer)))






if __name__ == "__main__":
    main()
