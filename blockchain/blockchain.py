from blockchain.block import Block
import json
from time import time


class Blockchain:
    def __init__(self):
        # Initialise la chaîne avec le bloc de genèse
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        """
        Crée le premier bloc de la chaîne (bloc de genèse).
        """
        return Block(
            index=0,
            timestamp=int(time()),
            data="Genesis Block",
            previous_hash="0",
            private_key=None  # Pas besoin de signature pour le genèse
        )

    def add_block(self, new_block):
        """
        Ajoute un nouveau bloc à la chaîne après validation.
        """
        # Récupère le dernier bloc
        last_block = self.chain[-1]

        # Met à jour le hash précédent du nouveau bloc
        new_block.previous_hash = last_block.hash

        # Vérifie la validité du bloc
        if self.is_block_valid(new_block, last_block):
            self.chain.append(new_block)
        else:
            raise ValueError("Bloc invalide : non ajouté à la chaîne.")

    def is_block_valid(self, block, previous_block):
        """
        Vérifie si un bloc est valide en :
        - Comparant le hash précédent avec celui du bloc précédent.
        - Vérifiant le hash du bloc actuel.
        - Validant la signature du bloc.
        """
        if block.previous_hash != previous_block.hash:
            return False

        if block.hash != block.calculate_hash():
            return False

        if not block.verify_block(block.public_key):
            return False

        return True

    def is_chain_valid(self):
        """
        Vérifie la validité de toute la chaîne.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Vérifie chaque bloc
            if not self.is_block_valid(current_block, previous_block):
                return False
        return True

    def rebuild_data(self):
        """
        Reconstruit les données brutes à partir des blocs.
        """
        data = ""
        for block in self.chain:
            data += block.data  # Concatène les données de chaque bloc
        return data

    def save_to_file(self, filename):
        """
        Sauvegarde la chaîne dans un fichier texte.
        """
        with open(filename, "w") as file:
            chain_data = [block.to_dict() for block in self.chain]
            json.dump(chain_data, file, indent=4)

    @classmethod
    def load_from_file(cls, filename="blockchain.json"):
        """
        Charge la blockchain depuis un fichier JSON.
        """
        with open(filename, "r") as file:
            chain_data = json.load(file)
            blockchain = cls()
            blockchain.chain = [Block.from_dict(block) for block in chain_data]
        return blockchain
