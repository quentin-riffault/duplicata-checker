
from pathlib import Path
from typing import Type
from core.libs.explorers.explorer import ExplorerBase

class DeDuplicata():

    def __init__(self, directory: Path) -> None:
        self._directory = directory
        self._to_process: list[Path] = []

    def discover(self, explorer_class: Type[ExplorerBase]) -> int:
        self._to_process = list(explorer_class.find_files(self._directory))
        return len(self._to_process)


