# Feedback — Krafton

## Vue d'ensemble

C'est un **moteur 3D avec système de positionnement par vision**, combinant :
- Un moteur de rendu OpenGL (pygame + PyOpenGL)
- Un pipeline de vision par ordinateur (OpenCV, blob detection LED)
- Des fichiers FreeCAD pour un contrôleur physique ("manette")

Le projet est clairement un **prototype académique** (les commits mentionnent "l'oral").

---

## Points positifs

- **Quaternions** pour les rotations — approche mathématiquement solide, évite le gimbal lock
- **Bonne séparation** graphics vs vision (modules distincts)
- **Type hints** récemment ajoutés — bonne direction
- Hiérarchie de classes propre pour les objets 3D (`OBJECT_BASE`, `FACES`, `AXES`, etc.)
- Orthonormalisation de Gram-Schmidt pour maintenir la base caméra

---

## Problèmes critiques

| Problème | Fichier | Impact |
|----------|---------|--------|
| `engine/models/` ignoré par `.gitignore` mais requis au démarrage | `main.py:14` | Crash au lancement |
| Vision et moteur 3D complètement découplés — aucune intégration | Tout le projet | Fonctionnalité incomplète |
| Chemin relatif hardcodé `'engine/models/Theiere.obj'` | `main.py:14` | Fragile |

---

## Problèmes de code

- **16 méthodes de déplacement quasi-identiques** (`forward3D`, `backward3D`, etc.) — `opengl_3d_object.py:169-293`. Une seule fonction paramétrée suffirait.
- **Cache désactivé** avec `force_parse=True` en dur — `dot_obj_parser.py:15`
- **Couleurs aléatoires** à chaque compilation — `opengl_3d_object.py:78,92`
- `produit_scalaire()` dans `fonctions_images.py:37-48` réimplémente ce que NumPy fait nativement
- Aucune gestion d'erreurs (I/O, caméra, OpenGL)
- `if __name__ == "__main__":` absent dans `main.py`

---

## OpenGL Legacy

Le projet utilise des **display lists** (OpenGL 1.x). Pour de meilleures performances, les VBOs (Vertex Buffer Objects) seraient la prochaine étape — mais pour un prototype, c'est acceptable.

---

## Documentation & Qualité

- README d'une seule ligne
- Aucun test (et `test.*` explicitement ignoré dans `.gitignore`)
- Messages de commits peu descriptifs (`"a"`, `"Drop the mic..."`)
- Configuration éparpillée entre `parameters.py` et `main.py`

---

## Priorités si tu veux aller plus loin

1. **Intégrer vision + moteur** — c'est le cœur du projet
2. **Factoriser les méthodes de déplacement** — gain immédiat de lisibilité
3. **Ajouter les modèles au repo** (ou un script de téléchargement)
4. **Documenter le setup** dans le README
