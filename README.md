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

## Lancement

```bash
python -m engine.main
```

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
