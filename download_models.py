"""
Télécharge les modèles 3D dans engine/models/.
Usage : python download_models.py

---
Où trouver des modèles gratuits compatibles (.obj) :

  - https://sketchfab.com         (filtrer "downloadable", exporter en OBJ)
  - https://free3d.com            (format OBJ directement disponible)
  - https://www.turbosquid.com    (filtrer "free", télécharger en OBJ)
  - https://polyhaven.com/models  (modèles CC0, haute qualité)
  - https://clara.io              (export OBJ disponible)

Compatibilité avec le parser de ce projet :
  ✓  f v/vt/vn   (vertex / texture / normale)  → format Blender par défaut
  ✓  f v//vn     (vertex / normale, sans UV)
  ✗  f v1 v2 v3  (faces simples sans slashes)  → crash au chargement

  Si un modèle n'est pas compatible, l'ouvrir dans Blender et
  l'exporter via File > Export > Wavefront (.obj) en cochant
  "Include Normals" et "Include UVs".
---
"""

import urllib.request
from pathlib import Path

MODELS_DIR = Path(__file__).parent / "engine" / "models"

# Modèles à télécharger : { 'nom_local.obj': 'https://url-directe.obj' }
MODELS = {
    # Utah Teapot — modèle de test classique en informatique graphique
    # Source : alecjacobson/common-3d-test-models (MIT)
    "teapot.obj": "https://raw.githubusercontent.com/alecjacobson/common-3d-test-models/master/data/teapot.obj",
    # Ajoute tes propres modèles ici :
    # 'monModele.obj': 'https://example.com/monModele.obj',
}

_HEADERS = {"User-Agent": "Mozilla/5.0"}


def download(filename: str, url: str) -> None:
    dest = MODELS_DIR / filename
    if dest.exists():
        print(f"  {filename} déjà présent, ignoré.")
        return

    print(f"  Téléchargement de {filename}...")
    try:
        req = urllib.request.Request(url, headers=_HEADERS)
        with urllib.request.urlopen(req) as response:
            dest.write_bytes(response.read())
        print(f"  {filename} téléchargé.")
    except Exception as e:
        print(f"  Erreur pour {filename} : {e}")


if __name__ == "__main__":
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    if not MODELS:
        print("Aucun modèle défini dans MODELS.")
    else:
        for filename, url in MODELS.items():
            download(filename, url)
        print("Terminé.")
