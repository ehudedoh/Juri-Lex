# JuriLex — Avancement du développement

## État général
- Phase actuelle : Phase 5 — Traduction (validée) · prochaine : Phase 6 — Synthèse vocale
- Dernière mise à jour : 2026-10-31
- État global : EN COURS
- Blocage principal : licences non commerciales (CC-BY-NC(-SA)) à trancher pour
  toute exploitation commerciale ; modèle TTS non encore exécuté.

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
- Intégration de la traduction locale français → éwé (Phase 5) :
  - Module `translation.py` : chargement **une seule fois** (singleton) du modèle
    de base NLLB-600M + adaptateur LoRA éwé, avec verrou d'inférence.
  - Endpoint `POST /api/translations`.
  - Câblage du frontend (le bouton « Traduire en éwé » appelle le backend réel).
- Mesures réelles : mémoire ~2,4 Go (pic ~2,5 Go), latence 9–46 s/phrase,
  chargement initial ~6 min (une seule fois par processus).

### Fichiers modifiés
- `backend/app/translation.py` — traduction NLLB-éwé (créé).
- `backend/app/routers/translations.py` — endpoint de traduction (créé).
- `backend/app/schemas.py` — modèles `TranslationRequest/Response`.
- `backend/app/main.py` — inclusion du routeur translations.
- `backend/tests/test_translations.py` — tests (créé, avec mocks).
- `frontend/src/api.js`, `frontend/src/App.jsx` — traduction câblée au backend.
- `AVANCEMENT.md` — suivi mis à jour.

### Tests exécutés
- `python -m pytest -q` → **20 passed** (tests traductions avec mocks).
- `npm run build` → **succès** (41 modules).
- **Test réel de traduction** (script) : 4 phrases traduites réellement en éwé —
  obligation, montant (« cent mille » → « akpe alafa ɖeka »), durée (« douze » →
  « wuieve »), interdiction (« interdit » → négation « … o »). Nombres et
  négations conservés.

### Fonctionnalités réellement validées
- Chargement réel du modèle NLLB-éwé (base + LoRA).
- Traduction réelle français → éwé (vérifiée sur plusieurs types de phrases).
- Conservation des nombres et des négations (vérifiée réellement).

### Problèmes rencontrés
- Le tokenizer de l'adaptateur LoRA a un `tokenizer_config.json` incompatible
  avec transformers 4.57 (`AttributeError`). Résolu en utilisant le tokenizer
  standard du modèle de base NLLB.
- Latence CPU élevée (9–46 s/phrase) : acceptable pour le MVP, à optimiser
  ultérieurement (quantification, segmentation).

### Limites restantes
- Traduction limitée au résumé de l'explication (pas au document complet).
- Audio (MMS TTS) encore simulé.
- Licences non commerciales : exploitation commerciale bloquée sans autorisation.

### Prochaine étape
Phase 6 — Synthèse vocale locale : charger MMS TTS éwé (déjà en cache, ~145 Mo),
implémenter l'endpoint de génération audio, produire un vrai fichier WAV, le
servir au frontend et le lire dans le navigateur. Attention : coexistence mémoire
NLLB (~2,4 Go) + TTS (~0,5 Go) à valider.

### Instructions pour reprendre
- Backend : `cd backend && source .venv/bin/activate && uvicorn app.main:app --reload`
- Frontend : `cd frontend && npm run dev`
- Tests : `cd backend && .venv/bin/python -m pytest`
- Les modèles NLLB et MMS TTS sont déjà en cache local (~/.cache/huggingface).
