import pytest
from blockchain.block import Block
from blockchain.blockchain import Blockchain
from blockchain.dilithium import KeyManager


def test_block_creation():
    key_manager = KeyManager()
    public_key = key_manager.get_public_key()
    private_key = key_manager.get_private_key()

    block = Block(
        index=1,
        data="Hello Blockchain",
        previous_hash="0",
        private_key=private_key,
        public_key=public_key
    )
    assert block.data == "Hello Blockchain"
    assert block.index == 1
    assert block.hash is not None
    assert block.signature is not None
    assert block.verify_block(public_key) is True

    # Vérifie que le timestamp est non nul et valide
    assert block.timestamp is not None
    assert isinstance(block.timestamp, int)
    assert block.timestamp > 0


def test_block_data_immutability():
    key_manager = KeyManager()
    public_key = key_manager.get_public_key()
    private_key = key_manager.get_private_key()

    block = Block(
        index=1,
        data="Hello Blockchain",
        previous_hash="0",
        private_key=private_key,
        public_key=public_key
    )

    # Tente de modifier les données
    with pytest.raises(AttributeError) as excinfo:
        block.data = "Altered Data"

    # Print l'information sur l'exception AttributeError
    print(f"AttributeError: {excinfo.value}")

    # Vérifie que le bloc reste valide
    assert block.verify_block(public_key) is True


def test_block_verification_failure():
    key_manager = KeyManager()
    public_key = key_manager.get_public_key()
    private_key = key_manager.get_private_key()

    block = Block(
        index=1,
        data="Hello Blockchain",
        previous_hash="0",
        private_key=private_key,
        public_key=public_key
    )

    # Simule une modification externe du hash
    block.hash = "FakeHash"
    assert block.verify_block(public_key) is False


def test_create_blockchain():
    blockchain = Blockchain()

    # Vérifie que la chaîne commence avec le bloc de genèse
    assert len(blockchain.chain) == 1
    genesis_block = blockchain.chain[0]
    assert genesis_block.index == 0
    assert genesis_block.data == "Genesis Block"
    assert genesis_block.signature is None

    # Ajoute un nouveau bloc
    key_manager = KeyManager()
    public_key = key_manager.get_public_key()
    private_key = key_manager.get_private_key()

    blockchain.add_block(Block(
        index=1,
        data="Hello Blockchain",
        previous_hash=genesis_block.hash,
        private_key=private_key,
        public_key=public_key
    ))
    assert blockchain.chain[0].timestamp != blockchain.chain[1].timestamp
    # Vérifie la longueur de la chaîne
    assert len(blockchain.chain) == 2
    assert blockchain.is_block_valid(
        blockchain.chain[1], blockchain.chain[0]
    ) is True
    assert blockchain.is_chain_valid() is True


def test_save_and_load_blockchain():
    blockchain = Blockchain()

    # Vérifie que la chaîne commence avec le bloc de genèse
    assert len(blockchain.chain) == 1
    genesis_block = blockchain.chain[0]
    assert genesis_block.index == 0
    assert genesis_block.data == "Genesis Block"
    assert genesis_block.signature is None

    # Ajoute un nouveau bloc
    key_manager = KeyManager()
    public_key = key_manager.get_public_key()
    private_key = key_manager.get_private_key()

    blockchain.add_block(Block(
        index=1,
        data="Hello Blockchain",
        previous_hash=genesis_block.hash,
        private_key=private_key,
        public_key=public_key
    ))

    # Vérifie la longueur de la chaîne
    assert len(blockchain.chain) == 2
    assert blockchain.is_block_valid(
        blockchain.chain[1], blockchain.chain[0]
    ) is True
    assert blockchain.is_chain_valid() is True

    # Sauvegarde la chaîne
    blockchain.save_to_file("tests/test_chain.json")

    # Charge la chaîne
    new_blockchain = Blockchain.load_from_file("tests/test_chain.json")
    # Vérifie que les deux chaînes sont identiques
    assert len(new_blockchain.chain) == 2
    assert new_blockchain.is_chain_valid() is True
    assert new_blockchain.chain[0].data == "Genesis Block"
    assert new_blockchain.chain[1].data == "Hello Blockchain"
    assert new_blockchain.chain[1].verify_block(public_key) is True
