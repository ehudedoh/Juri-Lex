# JuriLex — Avancement du développement

## État général
- Phase actuelle : Phase 3 — Documents (validée) · prochaine : Phase 4 — Explication IA
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
- Implémentation de l'extraction de texte côté backend (Phase 3) :
  - `POST /api/documents/extract` (multipart, plusieurs fichiers).
  - PDF avec texte (pypdf), PDF numérisé/mixte (rendu pdftoppm + OCR Tesseract).
  - DOCX (python-docx, paragraphes + tableaux).
  - Images (OCR Tesseract, langue française).
  - Détection du type **réel** (magic bytes), indépendamment de l'extension.
  - Validation : taille max, nombre de pages max, fichiers vides/malformés.
  - Fichiers temporaires en session (`TEMP_DIR/<session_id>/`), noms aléatoires,
    supprimés après traitement.
- Câblage du frontend : l'étape « Extraire le texte » appelle désormais le
  backend réel (au lieu des données simulées).

### Fichiers modifiés
- `backend/app/extraction.py` — détection de type + extraction PDF/DOCX/OCR (créé).
- `backend/app/storage.py` — gestion des fichiers temporaires (créé).
- `backend/app/routers/documents.py` — endpoint d'extraction (créé).
- `backend/app/schemas.py` — modèle de réponse `ExtractionResponse` (créé).
- `backend/app/main.py` — inclusion du routeur documents.
- `backend/requirements.txt` — ajout pypdf, python-docx, pillow, pytesseract.
- `backend/tests/test_extraction.py`, `test_documents.py` — tests (créés).
- `frontend/src/api.js` — client HTTP (créé).
- `frontend/src/App.jsx` — extraction câblée au backend réel.
- `README.md`, `AVANCEMENT.md` — documentation mise à jour.

### Tests exécutés
- `python -m pytest -q` → **12 passed** (dont OCR réel sur image générée).
- `npm run build` → **succès** (41 modules).
- Test de bout en bout : `POST /api/documents/extract` avec un vrai DOCX →
  **200**, texte extrait correct, `extraction_method=docx_text`.
- Vérification du nettoyage : `TEMP_DIR` vide après extraction.

### Fonctionnalités réellement validées
- Extraction DOCX (réelle, vérifiée via test et curl).
- OCR d'image (réel, Tesseract `fra`, test passé).
- Détection de type (réelle, magic bytes).
- Rejet des formats non pris en charge (415), fichiers vides (400), trop volumineux (413).
- Nettoyage des fichiers temporaires (réel, vérifié).
- Extraction PDF de texte : partiellement testée (détection + page sans texte) ;
  un PDF texte réel reste à vérifier manuellement.

### Problèmes rencontrés
- Aucun bloquant. Le rendu OCR des PDF scannés (pdftoppm) n'est pas encore
  couvert par un test automatisé (nécessite une fixture PDF numérisée).

### Limites restantes
- Analyse (Gemini), traduction (NLLB) et audio (MMS TTS) encore simulés.
- Modèles non téléchargés (~2,3 Go + ~150 Mo).
- Licences non commerciales : exploitation commerciale bloquée sans autorisation.

### Prochaine étape
Phase 4 — Explication IA : intégrer Gemini côté backend (clé serveur), imposer
le consentement côté backend, structurer la réponse, gérer les erreurs et
protéger contre les injections de prompt.
Critère de validation : sans `GEMINI_API_KEY`, l'endpoint refuse l'appel ; avec
une clé valide, l'explication est réellement produite par Gemini.

### Instructions pour reprendre
- Backend : `cd backend && source .venv/bin/activate && uvicorn app.main:app --reload`
- Frontend : `cd frontend && npm run dev`
- Tests : `cd backend && .venv/bin/python -m pytest`
- Ne pas télécharger les modèles (~2,3 Go + ~150 Mo) sans accord explicite (Règle 4).
