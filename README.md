# Blockchain de Diplômes : Documentation Complète

## Introduction

La **Blockchain de Diplômes** est un projet pedagogique visant à garantir l'authenticité, la sécurité et l'intégrité des diplômes. Grâce à la blockchain, chaque diplôme est enregistré de manière unique, infalsifiable et traçable. Ce projet utilise des technologies modernes telles que le **chiffrement post-quantique**, la fragmentation des données et la vérification cryptographique.
Il faudrait dans une version plus avancée, décentraliser les données afin de garantir une plus grande sécurité et une meilleure résilience.

---

## Objectifs pédagogiques

1. **Comprendre le fonctionnement de la blockchain** : structure des blocs, hachage, vérification de l'intégrité.
2. **Apprendre à gérer des fichiers sensibles** : fragmentation, chiffrement et compression.
3. **Découvrir les signatures numériques** : garantie d'authenticité des blocs.
4. **Créer une interface utilisateur avec Rich** : une bibliothèque Python pour des interfaces en console élégantes et interactives.

---

## Fonctionnalités

### 1. **Ajout d’un diplôme**
- Fragmentation du fichier PDF.
- Chiffrement de chaque fragment avec une clé publique post-quantique.
- Ajout des métadonnées (nom, diplôme, date) dans un bloc dédié.
- Création d'une blockchain distincte pour chaque diplôme.

### 2. **Extraction d’un diplôme**
- Reconstruction du fichier PDF à partir des fragments enregistrés dans la blockchain.
- Vérification de l’intégrité de chaque fragment et de la validité des signatures.

### 3. **Vérification de la blockchain**
- Vérification de l’intégrité des blocs (hachage, signature).
- Détection des incohérences ou altérations dans les données.

### 4. **Affichage des blockchains**
- Liste des blockchains disponibles (une par diplôme).
- Visualisation des blocs et de leur contenu (Genèse, Métadonnées, Fragments).

### 5. **Liste des diplômes**
- Lecture des blocs de métadonnées pour afficher les diplômes ajoutés.

---

## Concepts techniques

### 1. **Structure d’une blockchain**
Chaque blockchain est composée de blocs organisés de manière linéaire. Un bloc contient :
- **Index** : Position du bloc dans la chaîne.
- **Hash** : Empreinte unique calculée à partir des données du bloc.
- **Previous Hash** : Hash du bloc précédent.
- **Données** : Contenu spécifique au bloc (métadonnées ou fragments chiffrés).
- **Signature** : Garantit que le bloc n’a pas été modifié.

### 2. **Blocs spécifiques**
- **Bloc Genèse** : Le premier bloc de la chaîne, qui sert de point de départ.
- **Bloc Métadonnées** : Contient des informations lisibles (nom, diplôme, date).
- **Blocs Fragments** : Stockent les fragments chiffrés du diplôme.

### 3. **Chiffrement post-quantique**
Le projet utilise le protocole **McEliece** pour le chiffrement, adapté à l’ère post-quantique. Chaque fragment est chiffré avec une clé publique et déchiffré avec une clé privée.

### 4. **Fragmentation**
Les fichiers PDF sont divisés en petits fragments, facilitant leur stockage dans la blockchain. Chaque fragment est chiffré et compressé avant d’être ajouté à un bloc.

### 5. **Signatures numériques post-quantique**
Les signatures numériques Dilithium assurent l’authenticité des blocs et empêchent toute modification frauduleuse.

---

## Installation

### Prérequis
- **Python** : Version 3.10 ou supérieure.
- **Poetry** : Gestionnaire de dépendances.

### Étapes d'installation
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/LuuNa-JD/blockchain_diplome.git
   cd blockchain_diplome
   ```
2. Installez les dépendances avec Poetry :
   ```bash
   poetry install
   ```

3. Activez l’environnement virtuel :
   ```bash
   poetry shell
   ```

---

## Structure du projet

```plaintext
.
├── blockchain/
│   ├── blockchain.py        # Gestion de la blockchain
│   ├── block.py             # Structure des blocs
│   ├── dilithium.py         # Signatures numériques
├── data_manager/
│   ├── chiffrement.py       # Chiffrement post-quantique
│   ├── compression.py       # Compression des fragments
│   ├── fragmentation.py     # Fragmentation des fichiers
├── db_blockchains/          # Stockage des blockchains
├── tests/                   # Tests unitaires
│   ├── test_blockchain.py   # Tests de la blockchain
│   ├── test_data_manager.py # Tests gestion des données
│   ├── test_dilithium.py    # Tests des signatures numériques
├── cli_diplomas.py          # Interface utilisateur Rich
├── README.md                # Documentation
├── .gitignore               # Fichiers à ignorer
├── diploma.pdf              # Fichier PDF de test
├── pyproject.lock           # Verrouillage des dépendances
└── pyproject.toml           # Configuration du projet
```

---

## Utilisation

### Lancer l'application
Dans le terminal, exécutez la commande suivante :
```bash
python cli_diplomas.py
```

### Menu principal
Une interface interactive vous guidera à travers les différentes options :
1. Ajouter un diplôme.
2. Extraire un diplôme.
3. Afficher les blockchains.
4. Vérifier les blockchains.
5. Liste des diplômes.
6. Quitter.

---

## Explications détaillées des fonctionnalités

### Ajouter un diplôme
1. Fournissez le chemin du fichier PDF.
2. Saisissez les métadonnées :
   - Nom de l’étudiant.
   - Titre du diplôme.
   - Date d’obtention.
3. Le fichier est fragmenté, chiffré et ajouté à une nouvelle blockchain.

### Extraire un diplôme
1. Sélectionnez la blockchain correspondant au diplôme à extraire.
2. Saisissez le chemin de sortie du fichier PDF reconstruit.
3. La reconstruction vérifie les signatures et les hachages pour garantir l’intégrité.

### Afficher les blockchains
1. Liste toutes les blockchains disponibles dans le dossier `blockchains/`.
2. Visualise chaque bloc avec son contenu et son type (Genèse, Métadonnées, Fragment).

### Vérifier les blockchains
1. Vérifie globalement si toutes les blockchains sont valides.
2. Identifie les blocs corrompus ou modifiés.

### Liste des diplômes
1. Parcourt chaque blockchain pour lire les blocs de métadonnées.
2. Affiche une liste des diplômes enregistrés.

---

## Tests

### Exécution des tests
Pour exécuter tous les tests unitaires :
```bash
poetry run pytest --cov
```

### Couverture de code
Un rapport de couverture est généré pour vérifier la qualité des tests.

---

## Sécurité

### Mesures de sécurité
1. **Chiffrement post-quantique** : Protection contre les attaques futures des ordinateurs quantiques avec McEliece.
2. **Signatures numériques** : Garantissent l'authenticité des blocs avec Dilithium.
3. **Validation intégrée** : Vérifie les hachages et les signatures à chaque étape.

---

## Auteurs

- **Julien Denizot** : Développeur Logiciel.
