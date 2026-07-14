from pathlib import Path
from typing import Generator
from abc import ABC, abstractmethod

class ExplorerBase(ABC):

    @staticmethod
    @abstractmethod
    def find_files(base_path: Path) -> Generator[Path, None, None]:
        raise NotImplementedError()

