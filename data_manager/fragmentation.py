import os
import json
from rich.console import Console
from blockchain.block import Block
from data_manager.compression import compress_data, decompress_data
from data_manager.chiffrement import encrypt_fragment, decrypt_fragment

console = Console()


def fragment_file(file_path, fragment_size_percentage=10):
    """
    Divise un fichier en fragments de taille proportionnelle.
    """
    file_size = os.path.getsize(file_path)
    fragment_size = file_size * fragment_size_percentage // 100

    fragments = []
    with open(file_path, "rb") as f:
        while chunk := f.read(fragment_size):
            fragments.append(chunk)

    return fragments


def add_file_to_blockchain(file_path, blockchain, kem_public_key,
                           sig_private_key, sig_public_key):
    """
    Divise, compresse et ajoute les fragments d'un fichier à la blockchain
    avec signature et chiffrement.
    """
    fragments = fragment_file(file_path)  # Divise le fichier en fragments
    for i, fragment in enumerate(fragments):
        encrypted_fragment = encrypt_fragment(fragment, kem_public_key)
        # Convertit le dictionnaire chiffré en une chaîne JSON pour stockage
        encrypted_fragment_serialized = json.dumps(encrypted_fragment)
        encrypted_fragment_bytes = encrypted_fragment_serialized.encode()
        compressed_fragment = compress_data(encrypted_fragment_bytes)

        blockchain.add_block(Block(
            index=len(blockchain.chain),
            data=compressed_fragment.hex(),
            previous_hash=blockchain.chain[-1].hash,
            private_key=sig_private_key,
            public_key=sig_public_key
        ))


def extract_file_from_blockchain(blockchain, file_path, kem_private_key,
                                 sig_public_key):
    """
    Extrait les fragments de la blockchain et reconstitue un fichier.

    Parameters:
        blockchain (Blockchain): La blockchain contenant les blocs.
        file_path (str): Le chemin de sortie du fichier reconstruit.
        kem_private_key (bytes): La clé privée pour déchiffrer les fragments.
        sig_public_key (bytes): La clé publique pour vérifier les
        signatures des blocs.
    """
    with open(file_path, "wb") as f:
        # Vérifie si la blockchain est valide
        if not blockchain.is_chain_valid():
            raise ValueError("La blockchain est invalide.")

        for block in blockchain.chain[1:]:  # On saute le bloc de genèse
            # Étape 1 : Vérification de la signature du bloc
            if not block.verify_block(sig_public_key):
                raise ValueError(
                    f"Bloc {block.index} invalide (signature incorrecte)."
                )

            try:
                # Étape 2 : Décompression et désérialisation
                compressed_fragment = bytes.fromhex(block.data)
                decrypted_fragment = None

                try:
                    # Vérifie si les données sont des métadonnées
                    data = json.loads(compressed_fragment.decode())
                    if all(
                        key in data
                        for key in ["Nom", "Diplôme", "Date d'obtention"]
                    ):
                        console.print(
                            f"[yellow]Bloc {block.index} : "
                            f"Métadonnées détectées, "
                            f"ignorées pour la reconstruction "
                            f"du fichier.[/yellow]"
                        )
                        continue
                except (json.JSONDecodeError, UnicodeDecodeError):

                    encrypted_data_bytes = decompress_data(compressed_fragment)
                    encrypted_data = json.loads(encrypted_data_bytes.decode())
                    decrypted_fragment = decrypt_fragment(
                        encrypted_data, kem_private_key
                    )

                if decrypted_fragment:
                    f.write(decrypted_fragment)

            except Exception as e:
                raise ValueError(
                    f"Erreur lors du traitement du bloc {block.index} : {e}"
                )
