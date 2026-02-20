# Krafton

Moteur 3D avec système de positionnement par vision. Le projet combine un moteur de rendu OpenGL (rotations par quaternions), un pipeline de vision par ordinateur pour la détection de marqueurs LED, et des modèles FreeCAD pour un contrôleur physique.

## Prérequis

- Python 3.10+
- Fichiers de modèles `.obj` à placer dans `engine/models/`

## Installation

Créer et activer un environnement virtuel :

```bash
python -m venv .venv
```

Windows :
```bash
.venv\Scripts\activate
```

Linux / macOS :
```bash
source .venv/bin/activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

## Modèles 3D

Les modèles `.obj` ne sont pas inclus dans le dépôt. Pour les télécharger :

```bash
python download_models.py
```

## Lancement

```bash
python -m engine.main
```

## Développement

Le code est formaté avec [black](https://black.readthedocs.io/). Lancer le formateur avant chaque commit :

```bash
black cameras/ engine/ download_models.py
```

## CI/CD

### Pipelines GitHub Actions

| Workflow | Déclencheur | Rôle |
|----------|-------------|------|
| `ci.yml` | push / PR → `master` | Formatage black, syntaxe Python, tests unitaires (pytest) |
| `release-please.yml` | push → `master` | Crée automatiquement les PRs de release, bumpe la version dans `pyproject.toml` et génère le changelog |

Les tests couvrent la logique pure (math, parsing OBJ, caméra). Les méthodes OpenGL (`compile`, `draw`) et la boucle pygame nécessitent un contexte graphique et ne sont pas testées.

### Release Please

[Release Please](https://github.com/googleapis/release-please) détecte les commits sur `master` et crée une PR de release qui :
- incrémente la version sémantique dans `pyproject.toml`
- génère / met à jour `CHANGELOG.md`
- crée le tag Git et la GitHub Release au merge

La version courante est définie dans `pyproject.toml` (`version = "..."`) et suivie dans `.release-please-manifest.json`.

### Conventional Commits

Release Please s'appuie sur la convention [Conventional Commits](https://www.conventionalcommits.org/) pour déterminer le type de bump et le contenu du changelog.

| Préfixe | Effet sur la version | Exemple |
|---------|----------------------|---------|
| `fix:` | patch (`0.1.0` → `0.1.1`) | `fix: corriger le calcul de l'homographie` |
| `feat:` | mineur (`0.1.0` → `0.2.0`) | `feat: ajouter le support des fichiers .gltf` |
| `feat!:` ou `BREAKING CHANGE:` | majeur (`0.1.0` → `1.0.0`) | `feat!: refactoriser l'API caméra` |
| `chore:`, `docs:`, `refactor:`… | aucun bump | `chore: mettre à jour les dépendances` |

Les commits sans préfixe (comme les commits actuels) sont ignorés par Release Please et n'apparaissent pas dans le changelog.

## Contrôles

| Touche | Action |
|--------|--------|
| `↑ ↓ ← →` | Avancer / reculer / strafe |
| `Espace / C` | Monter / descendre |
| `Z S Q D` | Pitch / Yaw |
| `A E` | Roll |
| `Entrée` | Réinitialiser la position |
| `1` | Sélectionner la caméra |
| `2` | Sélectionner l'objet 1 |
| `Échap` | Quitter |
