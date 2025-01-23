from blockchain.dilithium import generate_keys, sign, verify
from data_manager.chiffrement import encrypt_fragment, decrypt_fragment, kemalg


def test_generate_keys():
    public_key, private_key = generate_keys()
    assert public_key is not None
    assert private_key is not None
    assert len(public_key) > 0
    assert len(private_key) > 0


def test_sign():
    public_key, private_key = generate_keys()
    signature = sign(b"Hello, World!", private_key)
    assert signature is not None
    assert len(signature) > 0


def test_verify():
    public_key, private_key = generate_keys()
    signature = sign(b"Hello, World!", private_key)
    assert verify(signature, b"Hello, World!", public_key) is True
    assert verify(signature, b"Hello, Blockchain!", public_key) is False


def test_encryption_decryption():
    public_key, private_key = kemalg.keypair()
    data = b"Hello, Blockchain!"
    encrypted = encrypt_fragment(data, public_key)
    decrypted = decrypt_fragment(encrypted, private_key)
    assert decrypted == data
