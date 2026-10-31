# JuriLex — Avancement du développement

## État général
- Phase actuelle : Phase 1 — Structure (validée) · prochaine : Phase 2 — Interface
- Dernière mise à jour : 2026-10-31
- État global : EN COURS
- Blocage principal : licences non commerciales (CC-BY-NC(-SA)) à trancher pour
  toute exploitation commerciale ; modèles non encore exécutés localement.

## Phase 0 — Faisabilité
- [x] Vérification des licences (traduction CC-BY-NC-SA-4.0, TTS CC-BY-NC-4.0, base CC-BY-NC-4.0)
- [x] Étude du modèle de traduction (fiche, base, tailles, codes langue, contraintes 512 tokens)
- [x] Étude du modèle TTS (VITS 36,3 M params, F32, ≈ 145 Mo)
- [x] Vérification des dépendances (torch 2.15 / transformers 5.22 / peft / accelerate, compat. Python 3.14)
- [x] Évaluation des ressources mémoire (estimée ≈ 4,5–5 Go simultané fp32 → stratégie charge/décharge)
- [x] Évaluation de l'hébergement (CPU dédié vs inférence distante vs API tierce)
- [x] Décisions techniques documentées (`docs/RAPPORT_DE_FAISABILITE.md`, `docs/STRUCTURE_DES_DONNEES.md`)

## Phase 1 — Structure
- [x] Frontend initialisé (Vite + React, JS, proxy `/api`)
- [x] Backend initialisé (FastAPI, `app/main.py`, `app/config.py`)
- [x] Configuration environnementale (`.env.example`, `Settings` via environnement)
- [x] Dépendances installées (core + dev + ML : torch 2.15 CPU, transformers 4.57, peft, accelerate)
- [x] Lancement local vérifié (uvicorn + `GET /api/health` → 200, build frontend OK)
- [x] Tests de base exécutés (`pytest` : 1 test passé)

## Phase 2 — Interface
- [ ] Accueil
- [ ] Importation
- [ ] Prévisualisation
- [ ] Correction du texte
- [ ] Consentement
- [ ] Résultats
- [ ] Traduction éwé
- [ ] Lecteur audio
- [ ] États de chargement et d'erreur
- [ ] Responsive et accessibilité

## Phase 3 — Documents
- [ ] Extraction PDF
- [ ] Extraction DOCX
- [ ] OCR des images
- [ ] Gestion des erreurs
- [ ] Nettoyage des fichiers temporaires

## Phase 4 — Explication IA
- [ ] Configuration Gemini
- [ ] Endpoint d'explication
- [ ] Validation du consentement
- [ ] Gestion des erreurs
- [ ] Protection contre les injections de prompt
- [ ] Test réel Gemini

## Phase 5 — Traduction
- [ ] Licence vérifiée
- [ ] Modèle de base identifié
- [ ] Adaptateur LoRA vérifié
- [ ] Chargement réel du modèle
- [ ] Traduction réelle français-éwé
- [ ] Tests linguistiques
- [ ] Mesures de mémoire et de latence

## Phase 6 — Synthèse vocale
- [ ] Licence vérifiée
- [ ] MMS TTS installé
- [ ] Chargement réel du modèle
- [ ] Génération réelle d'un fichier audio
- [ ] Lecture audio dans le navigateur
- [ ] Nettoyage audio
- [ ] Mesures de mémoire et de latence

## Phase 7 — Sécurité et validation
- [ ] Tests backend
- [ ] Tests frontend
- [ ] Tests de confidentialité
- [ ] Tests de nettoyage
- [ ] Tests de sécurité
- [ ] Tests linguistiques
- [ ] Tests utilisateurs

## Phase 8 — Déploiement
- [ ] Hébergement choisi
- [ ] Variables d'environnement configurées
- [ ] Frontend déployé
- [ ] Backend déployé
- [ ] Modèles opérationnels sur le serveur
- [ ] Parcours complet testé en production
- [ ] Coûts documentés

## Dernière session de travail

### Travail effectué
- Initialisation de la structure du projet : `backend/` (FastAPI), `frontend/`
  (Vite + React, JavaScript sans TypeScript), `README.md`, `.gitignore`,
  `.env.example`.
- Mise en place de la configuration par variables d'environnement
  (`backend/app/config.py`, lecture via `python-dotenv`).
- Installation des dépendances backend : core (fastapi, uvicorn, pydantic,
  python-multipart, python-dotenv), dev (pytest, httpx) et ML (torch 2.15 CPU,
  transformers 4.57, accelerate, peft).
- Validation de compatibilité Python 3.14 : import réussi de
  `AutoModelForSeq2SeqLM`, `VitsModel`, `AutoModelForTextToWaveform`, `PeftModel`.
- Vérification du lancement local : `GET /api/health` → 200 ; build frontend OK.

### Fichiers modifiés
- `README.md` — présentation, installation, lancement (créé).
- `.gitignore`, `.env.example` — règles Git et variables d'environnement (créés).
- `backend/app/main.py` — app FastAPI + endpoint `/api/health` + CORS (créé).
- `backend/app/config.py` — `Settings` lu depuis l'environnement (créé).
- `backend/requirements*.txt`, `backend/pyproject.toml` — dépendances + config pytest (créés).
- `backend/tests/test_health.py` — test de l'endpoint de santé (créé).
- `frontend/*` — squelette Vite + React (package.json, vite.config.js, index.html, src) (créés).
- `AVANCEMENT.md` — suivi mis à jour.

### Tests exécutés
- `backend/.venv/bin/python -m pytest -q` → **1 passed** (endpoint `/api/health`).
- `npm run build` (frontend) → **succès** (27 modules, build en ~11 s).
- Test de fumée : `uvicorn app.main:app` + `curl /api/health` → `200 OK`.
- Import des classes ML sur Python 3.14 → **succès** (~60 s).

### Fonctionnalités réellement validées
- Endpoint `/api/health` (réel, réponse 200 vérifiée).
- Compatibilité des dépendances ML avec Python 3.14 (imports réels).
- Build et démarrage du frontend Vite/React.
- **Aucun** modèle de traduction ou TTS exécuté (non téléchargé).

### Problèmes rencontrés
- Import `torch` très lent sur cette machine : **~40 s** (pression mémoire / swap).
  Impact : les modèles devront être chargés une fois puis réutilisés, jamais
  rechargés à chaque requête.
- `FutureWarning` : `torch.jit.script` non supporté en Python 3.14+ (sans impact
  attendu sur l'inférence seq2seq/VITS, à surveiller).
- `StarletteDeprecationWarning` : `httpx`/`TestClient` déprécié au profit de
  `httpx2` (avertissement sans effet sur les tests).
- `npm` signale `esbuild` dont le script postinstall n'est pas approuvé ; le
  build fonctionne néanmoins.

### Limites restantes
- Besoins mémoire et latence des modèles **estimés**, non mesurés.
- Licences non commerciales : exploitation commerciale bloquée sans autorisation.
- Modèles non encore téléchargés (≈ 2,3 Go + ≈ 150 Mo).

### Prochaine étape
Phase 2 — Interface : réaliser les écrans du parcours (accueil, importation,
prévisualisation, correction, consentement, résultats, traduction éwé, lecteur
audio) en mobile-first, avec états de chargement/erreur et accessibilité.
Critère de validation : navigation complète du parcours en local, sans appels
réels aux modèles (données simulées).

### Instructions pour reprendre
- Backend : `cd backend && source .venv/bin/activate && uvicorn app.main:app --reload`
- Frontend : `cd frontend && npm run dev`
- Tests : `cd backend && .venv/bin/python -m pytest`
- Ne pas télécharger les modèles (~2,3 Go + ~150 Mo) sans accord explicite (Règle 4).
