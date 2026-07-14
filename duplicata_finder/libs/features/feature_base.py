from abc import ABC, abstractmethod
from pathlib import Path


class FeatureBase(ABC):

    def __init__(self, file_path: str | Path) -> None:
        super().__init__()
        self._filename = str(file_path)


    @property
    def filename(self) -> str:
        return self._filename

    @abstractmethod
    def compute(self):
        pass

    @abstractmethod
    def similarity(self, other: "FeatureBase") -> float:
        pass

    @abstractmethod
    def __eq__(self, value: object) -> bool:
        return super().__eq__(value)

    def __repr__(self) -> str:
        return super().__repr__()