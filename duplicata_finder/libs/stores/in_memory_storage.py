from typing import Generator

from duplicata_finder.libs.features.feature_base import FeatureBase
from duplicata_finder.libs.stores.storage_base import StorageBase


class InMemoryStorage(StorageBase):

    def __init__(self) -> None:
        super().__init__()
        self._data: list[FeatureBase] = []

    def insert(self, feature: FeatureBase):
        self._data.append(feature)

    def delete(self, feature: FeatureBase):
        self._data.remove(feature)

    def find_all_similar(
        self, feature: FeatureBase, threshold: float = 0.7
    ) -> Generator[FeatureBase, None, None]:
        for other in self._data:
            similarity = feature.similarity(other)
            if similarity >= threshold:
                yield other

        raise StopIteration

    def find_all_duplicates(
        self, feature: FeatureBase
    ) -> Generator[FeatureBase, None, None]:
        yield from filter(
            lambda other: feature.filename != other.filename, self.find_all(feature)
        )

    def find_all(self, feature: FeatureBase) -> Generator[FeatureBase, None, None]:
        yield from filter(lambda other: other == feature, self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Generator[FeatureBase, None, None]:
        for datum in self._data:
            yield datum
