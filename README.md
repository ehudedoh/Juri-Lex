# JuriLex

**Comprendre avant de signer.**

Application web progressive (PWA) d'aide à la compréhension des documents
juridiques et administratifs au Togo : extraction du texte, explication en
français simple, traduction en éwé et synthèse vocale éwé.

## Architecture

- **`frontend/`** — application React / Vite (JavaScript, sans TypeScript), PWA.
- **`backend/`** — API Python / FastAPI (Pydantic), orchestration des modèles.
- **`docs/`** — cahier des charges, protocole, structure des données, rapport de
  faisabilité.
- **`AVANCEMENT.md`** — suivi réel de l'implémentation.

> **Confidentialité :** JuriLex ne conserve **aucun** document, texte, traduction
> ni fichier audio dans un historique. Aucune base de données persistante n'est
> utilisée (cf. `docs/STRUCTURE_DES_DONNEES.md`).

## Prérequis

- Python ≥ 3.11 (testé sur 3.14)
- Node.js ≥ 18 et npm
- Git
- **Tesseract OCR** (binaire `tesseract` + langue `fra`) — pour l'OCR des images
  et PDF numérisés
- **Poppler** (`pdftoppm`) — pour le rendu des pages de PDF scannés

Sur Debian/Ubuntu :

```bash
sudo apt-get install tesseract-ocr tesseract-ocr-fra poppler-utils
```

## Installation

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```

Dépendances des modèles (Phase 5/6), installées séparément :

```bash
# torch en version CPU uniquement (cette machine n'a pas de GPU CUDA)
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements-ml.txt
```

### Configuration

```bash
cp .env.example .env   # puis renseigner les valeurs
```

Les secrets (`GEMINI_API_KEY`, etc.) ne doivent jamais être commités.

### Frontend

```bash
cd frontend
npm install
```

## Lancement local

```bash
# Terminal 1 — backend (depuis backend/)
source .venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2 — frontend (depuis frontend/)
npm run dev
```

L'API est servie sur `http://localhost:8000` (endpoint de santé :
`GET /api/health`) et le frontend sur `http://localhost:5173` (proxy `/api`
configuré vers le backend).

## Tests

```bash
# Backend
cd backend
source .venv/bin/activate
python -m pytest

# Frontend
cd frontend
npm test
```

### Évaluation linguistique (traduction)

```bash
cd backend
source .venv/bin/activate
python eval_translation.py --limit 5   # ou sans limite pour le corpus complet
```

Le corpus de 36 phrases (`corpus_fr_ewe.py`) couvre obligations, interdictions,
montants, dates, délais, conditions, exceptions, pénalités, résiliation et
ambiguïtés. La qualité finale doit être relue par des locuteurs éwé.

## PWA

Le frontend est une PWA : `manifest.webmanifest` + service worker
(`public/sw.js`). Le service worker met en cache **uniquement les ressources
statiques** ; il ne met jamais en cache les documents, textes, explications,
traductions ni fichiers audio (les requêtes `/api/*` sont ignorées).

## Avertissement

Les modèles de traduction et de synthèse vocale sont sous licence **non
commerciale** (CC-BY-NC(-SA)). Une exploitation commerciale nécessite une
autorisation distincte des ayants droit. Voir `docs/RAPPORT_DE_FAISABILITE.md`.
