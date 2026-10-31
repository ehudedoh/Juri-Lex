# JuriLex — Avancement du développement

## État général
- Phase actuelle : Phase 4 — Explication IA (validée) · prochaine : Phase 5 — Traduction
- Dernière mise à jour : 2026-10-31
- État global : EN COURS
- Blocage principal : licences non commerciales (CC-BY-NC(-SA)) à trancher pour
  toute exploitation commerciale ; modèles de traduction/TTS non encore exécutés.

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
- [x] Accueil
- [x] Importation
- [x] Prévisualisation
- [x] Correction du texte
- [x] Consentement
- [x] Résultats
- [x] Traduction éwé
- [x] Lecteur audio
- [x] États de chargement et d'erreur
- [x] Responsive et accessibilité

> Note : l'interface est fonctionnelle avec des **données simulées** (mock.js).
> Les appels réels au backend (extraction, Gemini, NLLB, MMS TTS) seront câblés
> aux Phases 3 à 6.

## Phase 3 — Documents
- [x] Extraction PDF (texte direct via pypdf ; pages sans texte → OCR)
- [x] Extraction DOCX (python-docx, paragraphes + tableaux)
- [x] OCR des images (Tesseract `fra`, vérifié réellement)
- [x] Gestion des erreurs (taille, format réel, pages, fichiers vides/malformés)
- [x] Nettoyage des fichiers temporaires (session `TEMP_DIR`, noms aléatoires, supprimés après traitement)

## Phase 4 — Explication IA
- [x] Configuration Gemini (SDK `google-genai`, clé serveur, modèle `gemini-3.5-flash`)
- [x] Endpoint d'explication (`POST /api/explanations`)
- [x] Validation du consentement (vérifiée côté backend → 403 sans consentement)
- [x] Gestion des erreurs (503 sans clé/indisponible, 400 vide/trop long, timeout)
- [x] Protection contre les injections de prompt (instructions système)
- [x] Test réel Gemini (explication réelle vérifiée, sources document/ia/incertain)

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
- Intégration de Gemini côté backend (Phase 4) :
  - SDK `google-genai` (nouvelle API « Interactions »), clé lue depuis `.env`.
  - Mise à jour du modèle : `gemini-1.5-flash` (obsolète, 404) → `gemini-3.5-flash`.
  - Endpoint `POST /api/explanations` : vérification du consentement **côté
    backend** (403 sans consentement), validation du texte, appel réel à Gemini.
  - Réponse structurée (nature, résumé, obligations, montants, dates, conditions,
    conséquences, ambiguïtés, questions) avec source `document`/`ia`/`incertain`.
  - Protection contre les injections de prompt (instructions système).
  - Gestion des erreurs : 503 sans clé/indisponible, 400 vide/trop long.
- Câblage du frontend : l'analyse appelle désormais le backend réel.

### Fichiers modifiés
- `backend/app/ai.py` — client Gemini + prompt système + normalisation (créé).
- `backend/app/routers/explanations.py` — endpoint d'explication (créé).
- `backend/app/schemas.py` — modèles `ExplanationRequest/Item/Response`.
- `backend/app/config.py`, `.env`, `.env.example` — modèle par défaut mis à jour.
- `backend/requirements.txt` — ajout `google-genai`.
- `backend/tests/test_explanations.py` — tests consentement/erreurs/mock (créé).
- `frontend/src/api.js`, `frontend/src/App.jsx` — analyse câblée au backend.
- `AVANCEMENT.md` — suivi mis à jour.

### Tests exécutés
- `python -m pytest -q` → **17 passed**.
- **Test réel Gemini** : `ai.explain()` sur un contrat d'exemple → explication
  structurée correcte (obligations, montants, conséquences, ambiguïtés, questions,
  sources bien distinguées).
- **Test HTTP réel** : `POST /api/explanations` → **403** sans consentement,
  **200** avec consentement (explication réelle de Gemini).

### Fonctionnalités réellement validées
- Explication produite par Gemini (réelle, clé valide, modèle `gemini-3.5-flash`).
- Vérification du consentement côté backend (réelle, 403).
- Refus sans clé API (503) et texte vide (400).
- Distinction des sources document/ia/incertain (réelle).

### Problèmes rencontrés
- `gemini-1.5-flash` et `gemini-2.5-*` ne sont plus disponibles (404) ; les
  modèles 3.x exigent la nouvelle API « Interactions ». Résolu en passant à
  `google-genai` (interactions) avec `gemini-3.5-flash`.

### Limites restantes
- Traduction (NLLB) et audio (MMS TTS) encore simulés.
- Modèles de traduction/TTS non téléchargés (~2,3 Go + ~150 Mo).
- Licences non commerciales : exploitation commerciale bloquée sans autorisation.

### Prochaine étape
Phase 5 — Traduction locale : installer/charger le modèle NLLB-éwé (base +
adaptateur LoRA), implémenter l'endpoint de traduction français→éwé, tester
réellement et mesurer mémoire/latence. Cette phase nécessite le téléchargement
des poids (~2,3 Go) — voir accord explicite requis.

### Instructions pour reprendre
- Backend : `cd backend && source .venv/bin/activate && uvicorn app.main:app --reload`
- Frontend : `cd frontend && npm run dev`
- Tests : `cd backend && .venv/bin/python -m pytest`
- Ne pas télécharger les modèles de traduction/TTS (~2,3 Go + ~150 Mo) sans accord explicite (Règle 4).
