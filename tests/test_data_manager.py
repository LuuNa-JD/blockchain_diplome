import json
from data_manager import fragmentation, compression
from blockchain.dilithium import KeyManager
from blockchain.blockchain import Blockchain
from data_manager.fragmentation import (
    add_file_to_blockchain,
    extract_file_from_blockchain,
)
from data_manager.compression import decompress_data
from data_manager.chiffrement import generate_kem_keys


def test_fragment_and_compress():
    file_path = "tests/pdf_test.pdf"
    fragments = fragmentation.fragment_file(file_path)
    assert len(fragments) > 0

    for fragment in fragments:
        compressed_fragment = compression.compress_data(fragment)
        if compressed_fragment[:3] == b"CMP":
            assert len(compressed_fragment) <= len(fragment)
        elif compressed_fragment[:3] == b"NOC":
            assert len(compressed_fragment) > len(fragment)

        decompressed_fragment = compression.decompress_data(
            compressed_fragment)
        assert decompressed_fragment == fragment


def test_add_and_extract_file_from_blockchain():
    # Chemins des fichiers
    test_file_path = "tests/pdf_test.pdf"
    reconstructed_file_path = "tests/pdf_test_reconstructed.pdf"

    # Vérifie que le fichier d'entrée existe
    with open(test_file_path, "rb") as f:
        original_content = f.read()
    assert len(original_content) > 0, "Le fichier PDF d'entrée est vide !"

    # Génère les clés de signature et de chiffrement
    key_manager = KeyManager()
    sig_public_key = key_manager.get_public_key()
    sig_private_key = key_manager.get_private_key()
    kem_public_key, kem_private_key = generate_kem_keys()

    # Crée une blockchain
    blockchain = Blockchain()

    # Ajoute le fichier à la blockchain
    add_file_to_blockchain(
        test_file_path, blockchain, kem_public_key,
        sig_private_key, sig_public_key
    )

    # Vérifie que des blocs ont été ajoutés
    assert len(blockchain.chain) > 1, "Aucun bloc ajouté à la blockchain."

    blockchain.save_to_file("tests/test_chain2.json")

    # Vérifie chaque bloc de la blockchain
    for block in blockchain.chain[1:]:
        compressed_fragment = bytes.fromhex(block.data)
        encrypted_data_bytes = decompress_data(compressed_fragment)

        # Désérialisation JSON
        encrypted_data = json.loads(encrypted_data_bytes.decode())
        assert "ciphertext" in encrypted_data, "Fragment chiffré manquant."
        assert "nonce" in encrypted_data, "Nonce manquant."
        assert "tag" in encrypted_data, "Tag AES manquant."
        assert "kem_ct" in encrypted_data, "Clé encapsulée manquante."

    # Extrait le fichier depuis la blockchain
    extract_file_from_blockchain(
        blockchain, reconstructed_file_path, kem_private_key, sig_public_key
    )

    # Vérifie que le fichier extrait est identique à l'original
    with open(reconstructed_file_path, "rb") as f:
        extracted_content = f.read()
    assert extracted_content == original_content, \
        "Le fichier reconstruit est différent de l'original."
