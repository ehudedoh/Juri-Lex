# JuriLex — Avancement du développement

## État général
- Phase actuelle : Phase 6 — Synthèse vocale (validée) · prochaine : Phase 7 — Sécurité et qualité
- Dernière mise à jour : 2026-10-31
- État global : EN COURS
- Blocage principal : licences non commerciales (CC-BY-NC(-SA)) à trancher pour
  toute exploitation commerciale ; déploiement et tests finaux à réaliser.

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
- Intégration de la synthèse vocale éwé (Phase 6) :
  - Module `speech.py` : chargement MMS TTS (VITS) à la demande, génération d'un
    WAV 16 kHz en mémoire (aucun fichier temporaire sur disque).
  - Endpoint `POST /api/speech` : libère le traducteur (~2,4 Go) avant de charger
    le TTS (~0,5 Go) pour respecter les limites mémoire (Règle 4), retourne le WAV
    avec `Cache-Control: no-store`.
  - Endpoints lourds (explication, traduction, audio) passés en `def` (thread
    pool) pour ne pas bloquer la boucle d'événements FastAPI.
  - Frontend : génération audio réelle + lecture via balise `<audio>`, révocation
    des URL objet.
- Mesures réelles TTS : mémoire ~546 Mo (pic ~617 Mo), génération ~68 s
  (chargement inclus).

### Fichiers modifiés
- `backend/app/speech.py` — synthèse vocale MMS TTS (créé).
- `backend/app/translation.py` — ajout `unload()`.
- `backend/app/routers/speech.py` — endpoint audio (créé).
- `backend/app/routers/{explanations,translations}.py` — passage en `def`.
- `backend/app/schemas.py` — modèle `SpeechRequest`.
- `backend/app/main.py` — inclusion du routeur speech.
- `backend/tests/test_speech.py` — tests (créé, avec mocks).
- `frontend/src/api.js` — `speakToEwe` (blob audio).
- `frontend/src/App.jsx`, `screens/Ewe.jsx` — lecture audio réelle.
- `AVANCEMENT.md` — suivi mis à jour.

### Tests exécutés
- `python -m pytest -q` → **23 passed**.
- `npm run build` → **succès** (40 modules).
- **Test réel TTS** : génération d'un WAV valide (1 canal, 16 kHz, ~4,6 s).
- **Test HTTP réel** : `POST /api/speech` → **200**, `audio/wav`, 142 Ko, WAV valide.

### Fonctionnalités réellement validées
- Génération audio éwé réelle (MMS TTS).
- Serveur HTTP : WAV servi avec le bon type MIME, lisible par un navigateur.
- Stratégie mémoire : déchargement du traducteur avant chargement du TTS.

### Problèmes rencontrés
- Aucun bloquant. L'avertissement `torch.jit.script` non supporté en Python 3.14
  persiste (sans impact sur l'inférence VITS/NLLB).

### Limites restantes
- Le parcours complet (extraction → analyse → traduction → audio) n'a pas encore
  été testé de bout en bout dans un navigateur réel.
- Tests de sécurité/confidentialité et tests utilisateurs à réaliser (Phase 7).
- Licences non commerciales : exploitation commerciale bloquée sans autorisation.

### Prochaine étape
Phase 7 — Sécurité et validation : tests backend/frontend, confidentialité,
nettoyage, sécurité (injections de prompt, limites), tests linguistiques, et
vérification du parcours complet. En complément, mettre en place le PWA
(manifest + service worker sans mise en cache des données sensibles).

### Instructions pour reprendre
- Backend : `cd backend && source .venv/bin/activate && uvicorn app.main:app --reload`
- Frontend : `cd frontend && npm run dev`
- Tests : `cd backend && .venv/bin/python -m pytest`
- Les modèles NLLB et MMS TTS sont déjà en cache local (~/.cache/huggingface).
