from pathlib import Path
from hashlib import md5

from core.libs.features.feature_base import FeatureBase

_NO_HASH = ""
_CHUNK_SIZE = 512

class FeatureMD5(FeatureBase):

    def __init__(self, image_path: Path) -> None:
        super().__init__(image_path)
        self._md5 = _NO_HASH
        self.compute()

    @property
    def md5(self):
        return self._md5

    def compute(self):
        hash_computer = md5(b"")

        try:
            with open(self.filename, 'rb') as image_handle:
                while (data := image_handle.read(_CHUNK_SIZE)):
                    hash_computer.update(data)
        except OSError:
             pass

        self._md5 = hash_computer.hexdigest()


    def similarity(self, other: FeatureBase) -> float:
        if self.md5 is _NO_HASH:
            return 0.0

        if not isinstance(other, FeatureMD5):
            return 0.0

        return 1.0 if self == other else 0.0

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, FeatureMD5):
            return False

        return self.md5 is not _NO_HASH and self.md5 == value.md5

    def __repr__(self) -> str:
        return f"FeatureMD5<{self.filename},{self.md5}>"
