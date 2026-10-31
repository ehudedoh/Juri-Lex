# JuriLex — Avancement du développement

## État général
- Phase actuelle : Phase 7 — Sécurité et validation (en cours) · prochaine : Phase 8 — Déploiement
- Dernière mise à jour : 2026-10-31
- État global : EN COURS
- Blocage principal : licences non commerciales (CC-BY-NC(-SA)) à trancher pour
  toute exploitation commerciale ; tests utilisateurs et déploiement à réaliser.

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
- [x] Licence vérifiée (CC-BY-NC-SA-4.0, non commerciale)
- [x] Modèle de base identifié (facebook/nllb-200-distilled-600M)
- [x] Adaptateur LoRA vérifié (cheriftenga/nllb-200-distilled-600M-ewe-lora-v2)
- [x] Chargement réel du modèle (base + LoRA, ~2,4 Go RAM)
- [x] Traduction réelle français-éwé (vérifiée : obligations, montants, dates, négation)
- [x] Tests linguistiques (nombres et négations conservés)
- [x] Mesures de mémoire et de latence (pic ~2,5 Go ; 9–46 s/phrase ; chargement ~6 min)

## Phase 6 — Synthèse vocale
- [x] Licence vérifiée (CC-BY-NC-4.0, non commerciale)
- [x] MMS TTS installé (modèle déjà en cache local)
- [x] Chargement réel du modèle (VITS 36,3 M params)
- [x] Génération réelle d'un fichier audio (WAV 16 kHz valide, ~4,5 s)
- [x] Lecture audio dans le navigateur (endpoint `audio/wav` + balise `<audio>`)
- [x] Nettoyage audio (génération en mémoire, `unload` TTS, `Cache-Control: no-store`, révocation des URL objet)
- [x] Mesures de mémoire et de latence (546 Mo, pic 617 Mo ; ~68 s chargement inclus)

## Phase 7 — Sécurité et validation
- [x] Tests backend (29 tests, dont sécurité/confidentialité/nettoyage)
- [x] Tests frontend (Vitest + Testing Library, 2 tests)
- [x] Tests de confidentialité (aucune base de données persistante — test dédié)
- [x] Tests de nettoyage (répertoire temporaire + fichiers orphelins)
- [x] Tests de sécurité (anti-injection de prompt, chemins sûrs, limites taille/format)
- [x] Tests linguistiques (corpus 36 phrases + script d'évaluation ; relecture éwé à faire)
- [ ] Tests utilisateurs (protocole rédigé dans `docs/TESTS_UTILISATEURS.md` — à réaliser)

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
- Phase 7 — Sécurité et validation :
  - Nettoyage des fichiers orphelins (`storage.cleanup_orphans`, §6.1).
  - Tests de sécurité : anti-injection de prompt (instructions système + document
    délimité), chemins sûrs (noms aléatoires), limites taille/format (déjà couverts).
  - Tests de confidentialité : absence de base de données persistante (test dédié).
  - Tests de nettoyage : répertoire temporaire vidé après extraction + orphelins.
  - Tests frontend : Vitest + Testing Library (2 tests de navigation).
  - PWA : `manifest.webmanifest`, service worker (cache statique uniquement,
    jamais `/api/*`), icônes générées, enregistrement en production.
  - Corpus linguistique : 36 phrases (`corpus_fr_ewe.py`) + script
    `eval_translation.py`.
  - Plan de tests utilisateurs (`docs/TESTS_UTILISATEURS.md`).

### Fichiers modifiés
- `backend/app/storage.py` — ajout `cleanup_orphans`.
- `backend/tests/test_security.py` — tests sécurité/confidentialité/nettoyage (créé).
- `backend/corpus_fr_ewe.py`, `backend/eval_translation.py` — corpus + évaluation (créés).
- `docs/TESTS_UTILISATEURS.md` — protocole de tests utilisateurs (créé).
- `frontend/public/` — manifest, service worker, icônes (créés).
- `frontend/index.html`, `src/main.jsx` — PWA (manifest + enregistrement SW).
- `frontend/vitest.config.js`, `src/test-setup.js`, `src/App.test.jsx` — tests frontend (créés).
- `frontend/package.json`, `package-lock.json` — dépendances de test.
- `README.md`, `AVANCEMENT.md` — documentation mise à jour.

### Tests exécutés
- `python -m pytest -q` → **29 passed** (dont sécurité/confidentialité/nettoyage).
- `npm test` → **2 passed** (Vitest).
- `npm run build` → **succès** (40 modules, PWA incluse).
- Évaluation linguistique : script validé ; l'exécution du corpus d'exemple a été
  interrompue (redémarrage du serveur) — à relancer.

### Fonctionnalités réellement validées
- Nettoyage des fichiers temporaires et orphelins (réel, testé).
- Anti-injection de prompt (structure du prompt vérifiée).
- PWA installable (manifest + service worker, cache statique uniquement).
- Tests frontend (réels).

### Problèmes rencontrés
- L'évaluation du corpus a été interrompue par un redémarrage du serveur ; à
  relancer (`python eval_translation.py`).

### Limites restantes
- Tests utilisateurs non réalisés (protocole prêt, nécessite de vrais testeurs).
- Relecture des traductions éwé par des locuteurs compétents à faire.
- Parcours complet non testé de bout en bout dans un navigateur réel.
- Licences non commerciales : exploitation commerciale bloquée sans autorisation.

### Prochaine étape
Phase 8 — Déploiement : choisir l'hébergement (à partir des mesures), configurer
les secrets, déployer frontend + backend, tester en production et documenter les
coûts et limites.

### Instructions pour reprendre
- Backend : `cd backend && source .venv/bin/activate && uvicorn app.main:app --reload`
- Frontend : `cd frontend && npm run dev`
- Tests backend : `cd backend && .venv/bin/python -m pytest`
- Tests frontend : `cd frontend && npm test`
- Évaluation linguistique : `cd backend && .venv/bin/python eval_translation.py`
- Les modèles NLLB et MMS TTS sont déjà en cache local (~/.cache/huggingface).
