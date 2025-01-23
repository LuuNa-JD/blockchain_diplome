import hashlib
from blockchain.dilithium import sign, verify
from time import time


class Block:
    def __init__(self, index, timestamp=None, data="", previous_hash="",
                 private_key=None, public_key=None):
        self.index = index
        self.timestamp = timestamp if timestamp is not None else \
            int(time() * 1000)
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
        self.signature = None
        self.public_key = public_key
        if private_key:
            self.signature = sign(self.hash.encode(), private_key)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if hasattr(self, '_data'):  # Vérifie si l'attribut est déjà initialisé
            raise AttributeError(
                "Les données du bloc sont immuables après création."
            )
        self._data = value

    def calculate_hash(self):
        content = (
            f"{self.index}"
            f"{self.timestamp}"
            f"{self.data}"
            f"{self.previous_hash}"
        )
        return hashlib.sha256(content.encode()).hexdigest()

    def verify_block(self, public_key):

        if not self.signature:
            return False  # Pas de signature, donc invalide
        try:
            return verify(self.signature, self.hash.encode(), public_key)
        except ValueError:
            return False

    def to_dict(self):
        """
        Convertit le bloc en un dictionnaire sérialisable.
        """
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
            "signature": self.signature.hex() if self.signature else None,
            "public_key": self.public_key.hex() if self.public_key else None
        }

    @classmethod
    def from_dict(cls, data):
        """
        Reconstruit un bloc à partir d'un dictionnaire.
        """
        block = cls(
            index=data["index"],
            timestamp=data["timestamp"],
            data=data["data"],
            previous_hash=data["previous_hash"],
            private_key=None,  # La clé privée n'est pas restaurée
            public_key=(
                bytes.fromhex(data["public_key"]) if data["public_key"]
                else None
            )
        )
        # Restaure la signature en bytes
        block.signature = (
            bytes.fromhex(data["signature"]) if data["signature"] else None
        )
        return block
