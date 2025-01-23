from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.progress import Progress
import os
import json
from blockchain.blockchain import Blockchain, Block
from blockchain.dilithium import KeyManager
from data_manager.chiffrement import generate_kem_keys
from data_manager.fragmentation import (
    add_file_to_blockchain,
    extract_file_from_blockchain
)

# Initialiser Rich et les variables globales
console = Console()
blockchain = Blockchain()
key_manager = KeyManager()
sig_public_key = key_manager.get_public_key()
sig_private_key = key_manager.get_private_key()
kem_public_key, kem_private_key = generate_kem_keys()


def save_blockchain(blockchain, filename):
    """
    Sauvegarde une blockchain dans un fichier.
    """
    if not os.path.exists("db_blockchains"):
        os.makedirs("db_blockchains")
    filepath = os.path.join("db_blockchains", filename)
    blockchain.save_to_file(filepath)
    console.print(
        f"[bold green]Blockchain sauvegardée dans {filepath}[/bold green]"
    )


def add_diploma_with_rich():
    """
    Ajouter un diplôme avec une interface utilisateur Rich.
    """
    console.print("[bold cyan]Ajout d'un diplôme à la blockchain[/bold cyan]")

    # Vérifiez ou créez le dossier "blockchains"
    if not os.path.exists("db_blockchains"):
        os.makedirs("db_blockchains")

    # Demande le chemin du fichier PDF
    file_path = Prompt.ask(
        "[green]Entrez le chemin du fichier PDF du diplôme[/green]"
    )
    if not os.path.exists(file_path):
        console.print(
            f"[bold red]Erreur : Le fichier {file_path} "
            f"n'existe pas.[/bold red]"
        )
        return

    # Étape 1 : Ajout des métadonnées
    metadata = {}
    metadata['Nom'] = Prompt.ask("[green]Entrez le nom de l'étudiant[/green]")
    metadata['Diplôme'] = Prompt.ask(
        "[green]Entrez le titre du diplôme[/green]"
    )
    metadata['Date d\'obtention'] = Prompt.ask(
        "[green]Entrez la date d'obtention (format : YYYY-MM-DD)[/green]"
    )

    console.print("[yellow]Ajout des métadonnées à la blockchain...[/yellow]")
    metadata_block_data = json.dumps(metadata).encode()
    metadata_block = Block(
        index=len(blockchain.chain),
        data=metadata_block_data.hex(),
        previous_hash=blockchain.chain[-1].hash,
        private_key=sig_private_key,
        public_key=sig_public_key
    )
    blockchain.add_block(metadata_block)

    # Étape 2 : Ajout des fragments du fichier PDF
    console.print("[yellow]Ajout du fichier à la blockchain...[/yellow]")
    with Progress() as progress:
        task = progress.add_task("[cyan]Ajout des fragments...", total=100)

        add_file_to_blockchain(
            file_path,
            blockchain,
            kem_public_key,
            sig_private_key,
            sig_public_key
        )
        progress.update(task, completed=100)

    # Étape 3 : Sauvegarde de la blockchain
    diploma_count = len(os.listdir('db_blockchains')) + 1
    filename = f"db_blockchains/diploma_{diploma_count}.json"
    blockchain.save_to_file(filename)
    console.print(
        f"[bold green]Diplôme ajouté avec succès à la blockchain et "
        f"sauvegardé dans {filename} ![/bold green]"
    )


def extract_diploma_with_rich():
    """
    Permet à l'utilisateur de choisir une blockchain pour extraire un diplôme,
    et utilise `extract_file_from_blockchain` pour le reconstruire avec une
    interface conviviale.
    """
    console.print(
        "[bold cyan]Extraction d'un diplôme de la blockchain[/bold cyan]"
    )

    # Vérifie si le dossier "blockchains" existe
    if not os.path.exists("db_blockchains") or \
            not os.listdir("db_blockchains"):
        console.print(
            "[bold red]Aucune blockchain de diplôme n'est disponible pour "
            "extraction.[/bold red]"
        )
        return

    # Liste les fichiers de blockchain disponibles
    blockchains = os.listdir("db_blockchains")
    console.print(
        "\n[bold yellow]Diplômes disponibles pour extraction :[/bold yellow]"
    )
    for idx, filename in enumerate(blockchains, start=1):
        console.print(f"[green]{idx}. {filename}[/green]")

    # Demande à l'utilisateur de choisir un fichier blockchain
    choice = Prompt.ask(
        "[green]Entrez le numéro du diplôme à extraire[/green]",
        choices=[str(i) for i in range(1, len(blockchains) + 1)],
    )
    selected_file = blockchains[int(choice) - 1]

    # Demande le chemin de sortie pour le fichier reconstruit
    output_path = Prompt.ask(
        "[green]Entrez le chemin et le nom du fichier de sortie pour la "
        "reconstruction (PDF)"
        "(PDF)[/green]"
    )

    try:
        # Charge la blockchain sélectionnée
        blockchain = Blockchain.load_from_file(
            f"db_blockchains/{selected_file}"
        )

        # Extraction avec barre de progression
        with Progress() as progress:
            task = progress.add_task(
                "[cyan]Reconstruction du fichier...",
                total=len(blockchain.chain) - 1
            )
            extract_file_from_blockchain(
                blockchain, output_path, kem_private_key, sig_public_key
            )
            progress.update(task, completed=100)

        # Affiche un message de succès
        console.print(
            f"[bold green]Diplôme extrait avec succès et sauvegardé à : "
            f"{output_path}[/bold green]"
        )
    except Exception as e:
        # Affiche un message d'erreur
        console.print(
            f"[bold red]Erreur lors de l'extraction : {e}[/bold red]"
        )


def show_all_blockchains():
    """
    Affiche toutes les blockchains (une par diplôme).
    """
    if not os.path.exists("db_blockchains") or \
            len(os.listdir("db_blockchains")) == 0:
        console.print("[bold red]Aucune blockchain disponible ![/bold red]")
        return

    console.print(
        "[bold cyan]Contenu de toutes les blockchains disponibles[/bold cyan]"
    )

    for filename in os.listdir("db_blockchains"):
        file_path = os.path.join("db_blockchains", filename)
        with open(file_path, "r") as file:
            chain_data = json.load(file)

        table = Table(title=f"Blockchain de {filename}")
        table.add_column("Index", justify="center", style="cyan", no_wrap=True)
        table.add_column("Hash", style="magenta")
        table.add_column("Previous Hash", style="magenta")
        table.add_column("Data", style="green")
        table.add_column("Type", style="yellow")

        for block in chain_data:
            block_type = "Genèse" if block["index"] == 0 else (
                "Métadonnées" if block["data"].startswith("{") else "Fragment"
            )
            table.add_row(
                str(block["index"]),
                block["hash"][:8] + "...",
                block["previous_hash"][:8] + "...",
                block["data"][:40] + "..." if len(block["data"]) > 40
                else block["data"],
                block_type
            )

        console.print(table)


def list_diplomas():
    """
    Liste tous les diplômes présents (une blockchain = un diplôme).
    """
    console.print("[bold cyan]Liste des diplômes[/bold cyan]")
    if not os.path.exists("db_blockchains") or \
            len(os.listdir("db_blockchains")) == 0:
        console.print("[bold red]Aucun diplôme trouvé ![/bold red]")
        return

    for filename in os.listdir("db_blockchains"):
        filepath = os.path.join("db_blockchains", filename)
        diploma_blockchain = Blockchain.load_from_file(filepath)
        # Le bloc 1 contient les métadonnées
        metadata_block = diploma_blockchain.chain[1]
        metadata = json.loads(bytes.fromhex(metadata_block.data).decode())

        console.print(
            f"[yellow]{filename} :[/yellow]\n"
            f"  [green]Nom :[/green] {metadata['Nom']}\n"
            f"  [green]Diplôme :[/green] {metadata['Diplôme']}\n"
        )


def verify_all_blockchains():
    """
    Vérifie l'intégrité de toutes les blockchains.
    """
    console.print("[bold cyan]Vérification des blockchains[/bold cyan]")
    if not os.path.exists("db_blockchains") or \
            len(os.listdir("db_blockchains")) == 0:
        console.print("[bold red]Aucune blockchain à vérifier ![/bold red]")
        return

    for filename in os.listdir("db_blockchains"):
        filepath = os.path.join("db_blockchains", filename)
        diploma_blockchain = Blockchain.load_from_file(filepath)
        console.print(f"[bold yellow]Vérification de {filename}[/bold yellow]")

        if not diploma_blockchain.is_chain_valid():
            console.print(f"[bold red]{filename} est invalide ![/bold red]")
        else:
            console.print(f"[bold green]{filename} est valide ![/bold green]")


def main_menu():
    """
    Menu principal
    """
    while True:
        console.print(Panel("[bold cyan]Menu Principal[/bold cyan]\n"
                            "1. Ajouter un diplôme\n"
                            "2. Extraire un diplôme\n"
                            "3. Afficher les blockchains\n"
                            "4. Vérifier les blockchains \n"
                            "5. Afficher la liste des diplomes\n"
                            "6. Quitter", title="Blockchain de Diplômes"))
        choice = Prompt.ask(
            "[green]Choisissez une option[/green]",
            choices=["1", "2", "3", "4", "5", "6"],
            default="6"
        )

        if choice == "1":
            add_diploma_with_rich()
        elif choice == "2":
            extract_diploma_with_rich()
        elif choice == "3":
            show_all_blockchains()
        elif choice == "4":
            verify_all_blockchains()
        elif choice == "5":
            list_diplomas()
        elif choice == "6":
            console.print("[bold green]Au revoir ![/bold green]")
            break


# Exécution du programme
if __name__ == "__main__":
    main_menu()
