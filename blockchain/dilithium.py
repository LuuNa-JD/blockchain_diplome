from pqc.sign import dilithium5 as dilithium


class KeyManager:
    def __init__(self):
        self.public_key, self.private_key = generate_keys()

    def get_public_key(self):
        return self.public_key

    def get_private_key(self):
        return self.private_key


def generate_keys():
    """
    Génère une paire de clés SPHINCS+.
    """
    public_key, private_key = dilithium.keypair()
    return public_key, private_key


public_key, private_key = generate_keys()
# print("Public Key:", public_key)
# print("Private Key:", private_key)


def sign(data, private_key):
    """
    Signe un message avec une clé privée SPHINCS+.
    """
    signature = dilithium.sign(data, private_key)
    return signature


data_signé = sign(b"Hello, World!", private_key)
# print("data signé:", data_signé)


def verify(signature, data, public_key):
    """
    Vérifie la signature d'un message avec une clé publique SPHINCS+.
    """
    try:
        dilithium.verify(signature, data, public_key)
        return True
        print("Vérifié")
    except ValueError as e:
        return False
        print("Erreur:", e)


print("Vérifié:", verify(data_signé, b"Hello, World!", public_key))
