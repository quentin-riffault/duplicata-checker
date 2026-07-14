from pathlib import Path
from typing import Generator
from os import walk

from duplicata_finder.libs.explorers.explorer import ExplorerBase

class WalkExplorer(ExplorerBase):

    @staticmethod
    def find_files(base_path: Path) -> Generator[Path, None, None]:

        if base_path.is_file():
            yield base_path
            raise StopIteration

        if not base_path.exists():
            raise StopIteration

        if not base_path.is_dir():
            raise StopIteration

        for dirpath, _unused_dirnames, files in walk(base_path):

            for file in files:
                yield Path(dirpath, file)

