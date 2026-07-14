from abc import ABC, abstractmethod
from typing import Generator, Iterable

from duplicata_finder.libs.features.feature_base import FeatureBase

class StorageBase(ABC, Iterable[FeatureBase]):
    """
    Classe représentant un espace de stockage de features. Cet espace de stockage doit permettre:
    - L'insertion de features
    - La suppression de features
    - La recherche de features similaires
    - La recherche de features exactes
    """

    @abstractmethod
    def insert(self, feature: FeatureBase):
        """
        Méthode d'insertion de features dans l'espace de stockage

        :param feature: feature à insérer dans l'espace de stockage
        """
        pass

    @abstractmethod
    def delete(self, feature: FeatureBase):
        """
        Méthode de suppression de features dans l'espace de stockage. L'élément supprimé doit correspondre exactement
        (filename + feature).

        :param feature: feature à supprimer dans l'espace de stockage
        """
        pass

    @abstractmethod
    def find_all_similar(self, feature: FeatureBase, threshold: float = 0.7) -> Generator[FeatureBase, None, None]:
        pass

    @abstractmethod
    def find_all(self, feature: FeatureBase) -> Generator[FeatureBase, None, None]:
        pass

    @abstractmethod
    def find_all_duplicates(self, feature: FeatureBase) -> Generator[FeatureBase, None, None]:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def __iter__(self) -> Generator[FeatureBase, None, None]:
        pass

