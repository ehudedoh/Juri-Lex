# JuriLex — Déploiement du backend sur Render

Ce document décrit le déploiement du backend JuriLex (FastAPI + modèles NLLB et
MMS TTS) sur [Render](https://render.com).

---

## 1. Prérequis matériels (importants)

| Élément | Recommandation |
| --- | --- |
| RAM | **≥ 4 Go, idéalement 8 Go** (le traducteur NLLB occupe ~2,4 Go en mémoire) |
| Disque persistant | ~10 Go (cache des modèles ≈ 2,5 Go) |
| CPU | CPU suffisant (les modèles tournent sur CPU, pas de GPU requis) |
| Python | ≥ 3.11 (testé sur 3.14.8 ; `3.13` recommandé pour Render) |

> Le plan « Starter » (512 Mo) est **insuffisant**. Utiliser au minimum
> « Standard » et vérifier la RAM dans le tableau de bord Render.

---

## 2. Déploiement via le blueprint (`render.yaml`)

Le dépôt contient un fichier `render.yaml` prêt à l'emploi.

1. Sur Render : **New → Blueprint**.
2. Connecter le dépôt GitHub `ehudedoh/Juri-Lex`.
3. Render détecte `render.yaml` et crée le service `jurilex-api`.
4. Renseigner la variable `GEMINI_API_KEY` (demandée comme secret, `sync: false`).
5. Ajuster `ALLOWED_ORIGINS` à l'URL réelle du frontend.
6. Vérifier le plan/la RAM du service (≥ 4 Go).

Le blueprint configure :
- `buildCommand` : installe `torch` (CPU uniquement, via l'index PyTorch) puis
  les dépendances de `requirements.txt`.
- `startCommand` : `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
- `healthCheckPath` : `/api/health`.
- Un **disque persistant** monté sur `/var/data` (cache des modèles).

## 3. Téléchargement des modèles (une seule fois)

Les poids (~2,5 Go) doivent être préchargés sur le disque persistant pour éviter
un téléchargement au premier appel.

Depuis l'onglet **Shell** du service Render (le disque est monté) :

```bash
cd backend
python download_models.py
```

Le script respecte `MODEL_CACHE_DIR=/var/data/models` et télécharge :
- `facebook/nllb-200-distilled-600M` (~2,3 Go)
- `cheriftenga/nllb-200-distilled-600M-ewe-lora-v2` (~42 Mo)
- `facebook/mms-tts-ewe` (~145 Mo)

## 4. Variables d'environnement

| Variable | Valeur | Secret |
| --- | --- | --- |
| `GEMINI_API_KEY` | clé Gemini | ✅ oui |
| `GEMINI_MODEL` | `gemini-3.5-flash` | non |
| `MODEL_CACHE_DIR` | `/var/data/models` | non |
| `ALLOWED_ORIGINS` | URL du frontend | non |
| `MAX_UPLOAD_SIZE_MB` | `20` | non |
| `MAX_DOCUMENT_PAGES` | `20` | non |
| `REQUEST_TIMEOUT_SECONDS` | `300` | non |

## 5. Vérification

```bash
curl https://<service>.onrender.com/api/health
# → {"status":"ok","request_id":"..."}
```

## 6. Déploiement du frontend (PWA)

Le blueprint `render.yaml` inclut un **static site** (`jurilex`) qui
construit l'application Vite/React et publie `frontend/dist`.

### 6.1. URL de l'API (`VITE_API_URL`)

Le frontend lit l'URL du backend via la variable `VITE_API_URL` (définie **au
build**). Exemple :

```
VITE_API_URL=https://jurilex-api.onrender.com/api
```

Sans cette variable, le frontend utilise `/api` (proxy Vite, développement
uniquement).

### 6.2. CORS (`ALLOWED_ORIGINS`)

Le backend doit autoriser l'origine du frontend. Vérifier que `ALLOWED_ORIGINS`
sur le service backend contient bien l'URL du frontend (ex.
`https://jurilex.onrender.com`).

### 6.3. Service worker / PWA

Le service worker met en cache **uniquement les ressources statiques** et ignore
toute requête `/api/*` (documents, textes, explications, traductions, audio ne
sont jamais mis en cache). La PWA nécessite d'être servie en **HTTPS**
(assuré par Render).

## 7. Points d'attention

- **Démarrage à froid** : le chargement du traducteur NLLB en mémoire prend
  plusieurs minutes (≈ 3–6 min sur CPU). Le premier appel de traduction après un
  redémarrage peut donc dépasser les délais d'attente habituels. Le modèle est
  ensuite réutilisé (singleton).
- **Mémoire** : le traducteur (~2,4 Go) est **déchargé** avant de charger le TTS
  (~0,5 Go), et inversement, pour rester dans les limites.
- **Licences** : les modèles NLLB (CC-BY-NC-SA-4.0) et MMS TTS (CC-BY-NC-4.0)
  sont **non commerciaux**. Un déploiement commercial nécessite une autorisation
  distincte des ayants droit.
- **Taille des fichiers** : les documents importés sont limités
  (`MAX_UPLOAD_SIZE_MB`, `MAX_DOCUMENT_PAGES`) et supprimés après traitement.
