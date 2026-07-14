from pathlib import Path
from typing import Type

from duplicata_finder.libs.explorers.explorer import ExplorerBase
from duplicata_finder.libs.features.feature_base import FeatureBase
from duplicata_finder.libs.stores.storage_base import StorageBase


class DeDuplicata:

    def __init__(self, directory: Path) -> None:
        self._directory = directory
        self._to_process: list[Path] = []

    def discover(self, explorer_class: Type[ExplorerBase]) -> int:
        self._to_process = list(explorer_class.find_files(self._directory))
        return len(self._to_process)

    def compute_features(self, feature_class: Type[FeatureBase], storage: StorageBase):
        for file in self._to_process:
            storage.insert(feature_class(file))
