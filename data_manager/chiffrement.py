from pqc.kem import mceliece6960119 as kemalg
from Crypto.Cipher import AES
import base64


def generate_kem_keys():
    """
    Génère une paire de clés publique/privée pour le chiffrement McEliece.
    """
    return kemalg.keypair()


def encrypt_fragment(fragment, public_key):
    # Étape 1 : Key encapsulation
    assert isinstance(fragment, bytes), "Le fragment doit être en bytes"
    assert isinstance(public_key, bytes), "La clé publique doit être en bytes"
    shared_secret, kem_ct = kemalg.encap(public_key)

    # Étape 2 : Utilisation du shared_secret comme clé AES
    # (prend les 16 premiers octets)
    aes_key = shared_secret[:16]
    cipher = AES.new(aes_key, AES.MODE_EAX)
    nonce = cipher.nonce

    # Étape 3 : Chiffrement du fragment
    ciphertext, tag = cipher.encrypt_and_digest(fragment)

    # Retourne le ciphertext, le nonce, le tag et le KEM ciphertext
    return {
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "nonce": base64.b64encode(nonce).decode(),
        "tag": base64.b64encode(tag).decode(),
        "kem_ct": base64.b64encode(kem_ct).decode(),
    }


def decrypt_fragment(encrypted_data, private_key):
    try:
        # Étape 1 : Récupération des données chiffrées
        ciphertext = base64.b64decode(encrypted_data["ciphertext"])
        nonce = base64.b64decode(encrypted_data["nonce"])
        tag = base64.b64decode(encrypted_data["tag"])
        kem_ct = base64.b64decode(encrypted_data["kem_ct"])

        # Étape 2 : Key de-encapsulation
        shared_secret = kemalg.decap(kem_ct, private_key)

        # Étape 3 : Utilisation du shared_secret comme clé AES
        # (prend les 16 premiers octets)
        aes_key = shared_secret[:16]
        cipher = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)

        # Étape 4 : Déchiffrement
        return cipher.decrypt_and_verify(ciphertext, tag)
    except KeyError as e:
        raise ValueError(f"Clé manquante dans les données chiffrées : {e}")
    except Exception as e:
        raise ValueError(f"Erreur lors du déchiffrement : {e}")
