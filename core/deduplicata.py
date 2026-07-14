
from pathlib import Path
from typing import Type
from core.libs.explorers.explorer import ExplorerBase
from core.libs.features.feature_base import FeatureBase

class DeDuplicata():

    def __init__(self, directory: Path) -> None:
        self._directory = directory
        self._to_process: list[Path] = []


    def discover(self, explorer_class: Type[ExplorerBase]) -> int:
        self._to_process = list(explorer_class.find_files(self._directory))
        return len(self._to_process)

    def compute_features(self, feature_class: Type[FeatureBase]):
        for file in self._to_process:
            feature = feature_class(file)
            print(feature)
