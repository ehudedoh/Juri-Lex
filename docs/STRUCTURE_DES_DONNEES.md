# JURILEX — Structure des données

**Version 1.0**

Ce document décrit la structure de données du MVP JuriLex, conformément au
`CAHIER_DES_CHARGES.md` et au `PROTOCOLE_DE_DEVELOPPEMENT.md`.

---

## 1. Décision de principe : absence de base de données persistante

Le cahier des charges impose explicitement l'**absence de base de données**
pour le MVP (cf. §4.6 « Absence de base de données », §6.1 « Principe de
minimisation », §3.8 « Fin de session », et Règle 6 du protocole).

Sont donc **interdits** :

- une base de comptes utilisateurs ;
- un historique de documents ou de contrats ;
- le stockage durable de textes extraits, corrigés, d'explications, de
  traductions ou de fichiers audio.

Toutes les données liées à un document sont **temporaires** et supprimées :

- après une opération terminée ;
- après une erreur ;
- lors d'un abandon de session ;
- après expiration du délai maximal prévu.

La structure de données décrite ci-dessous est donc de **deux natures** :

1. **Un état de session éphémère**, conservé en mémoire vive (RAM) le temps du
   traitement, sans persistance sur disque au-delà du cycle de vie de la
   session.
2. **Des fichiers temporaires** sur disque, dans un répertoire dédié, avec des
   noms non prédictibles et une durée de vie bornée.

> **Note de passage à l'échelle** : un état en mémoire vive convient à un MVP
> monoposte. Si un déploiement multi-processus devient nécessaire, un stockage
> d'état à durée de vie courte (ex. Redis avec TTL, sans contenu documentaire)
> pourrait être envisagé **uniquement après justification**, sans jamais y
> stocker le contenu des documents. Ce point n'est pas requis pour le MVP.

---

## 2. Modèle de session éphémère (en mémoire)

Une session représente le parcours complet d'un document par un utilisateur,
depuis l'importation jusqu'à la génération audio. Elle est identifiée par un
`session_id` **aléatoire et non prédictible** (UUID v4), généré côté backend.

### 2.1. Champs de la session

| Champ | Type | Description |
| --- | --- | --- |
| `session_id` | `UUID` | Identifiant unique, aléatoire, non prédictible. |
| `created_at` | `datetime` | Horodatage de création (début de session). |
| `last_activity_at` | `datetime` | Dernière activité (sert au calcul d'expiration). |
| `expires_at` | `datetime` | Date d'expiration (TTL = `REQUEST_TIMEOUT_SECONDS` ou borne dédiée). |
| `stage` | `enum` | Étape courante du pipeline (voir §2.2). |
| `temp_files` | `list[Path]` | Liste des fichiers temporaires créés pour cette session, à nettoyer. |

### 2.2. Étapes du pipeline (`stage`)

```
AWAITING_UPLOAD       → attente d'un document
PREVIEW               → prévisualisation / suppression / remplacement / réordonnancement des pages
EXTRACTION            → extraction ou OCR en cours
TEXT_VERIFICATION     → texte affiché à l'utilisateur pour correction
CONSENT               → consentement explicite requis avant envoi à Gemini
ANALYSIS              → appel à Gemini, génération de l'explication
RESULTS               → explication française affichée
TRANSLATION           → traduction français-éwé
SPEECH                → synthèse vocale éwé
FINISHED              → fin de session, nettoyage déclenché
ERROR                 → erreur survenue, nettoyage à prévoir
```

### 2.3. Bloc « document importé »

| Champ | Type | Description |
| --- | --- | --- |
| `original_filename` | `str` | Nom d'origine (à usage d'affichage uniquement, jamais utilisé comme chemin). |
| `document_type` | `enum` | `PDF` / `DOCX` / `IMAGE` / `MIXED`. |
| `mime_type` | `str` | Type MIME réel vérifié côté backend. |
| `size_bytes` | `int` | Taille réelle (contrôlée par `MAX_UPLOAD_SIZE_MB`). |
| `page_count` | `int` | Nombre de pages (contrôlé par `MAX_DOCUMENT_PAGES`). |
| `pages` | `list[Page]` | Références aux pages importées/prévisualisées (voir §3.2). |

### 2.4. Bloc « extraction et correction »

| Champ | Type | Description |
| --- | --- | --- |
| `extracted_text` | `str` | Texte brut extrait (PDF texte, DOCX, OCR). |
| `extraction_method` | `enum` | `PDF_TEXT` / `DOCX_TEXT` / `OCR` / `MIXED`. |
| `ocr_warnings` | `list[str]` | Zones signalées comme fragiles (noms propres, montants, dates…). |
| `corrected_text` | `str` | Texte modifié par l'utilisateur. |
| `text_version` | `int` | Compteur incrémenté à **chaque modification** du texte. |

> **Règle d'invalidation** (§3.3) : toute modification de `corrected_text`
> incrémente `text_version` et invalide l'explication, la traduction et l'audio
> déjà produits. Un résultat ne peut jamais être présenté pour une version de
> texte différente de la version courante.

### 2.5. Bloc « consentement »

| Champ | Type | Description |
| --- | --- | --- |
| `consent_granted` | `bool` | `true` uniquement après action explicite de l'utilisateur. |
| `consent_timestamp` | `datetime` | Horodatage du consentement. |
| `consent_scope` | `str` | Périmètre strict : envoi du texte corrigé au seul service d'IA pour l'explication. |

> **Règle** (§3.4) : le consentement est vérifié **côté backend**, jamais par une
> simple case à cocher React. Aucun appel à Gemini n'est réalisé sans
> `consent_granted == true`.

### 2.6. Bloc « explication (Gemini) »

`analysis_status` : `PENDING` / `RUNNING` / `SUCCESS` / `FAILED`.

| Champ | Type | Description |
| --- | --- | --- |
| `analysis_request_id` | `UUID` | Identifiant de requête aléatoire (pour les logs, sans contenu). |
| `explanation` | `Explanation` | Résultat structuré (voir §4). |
| `source_text_version` | `int` | Version de `corrected_text` ayant produit l'explication. |
| `analysis_timestamp` | `datetime` | Horodatage de la réponse. |
| `error_message` | `str` | Message technique interne (jamais renvoyé tel quel au frontend). |

### 2.7. Bloc « traduction éwé »

`translation_status` : `PENDING` / `RUNNING` / `SUCCESS` / `FAILED`.

| Champ | Type | Description |
| --- | --- | --- |
| `translation_ewe` | `str` | Traduction éwé de l'**explication** (pas du document intégral). |
| `translation_model` | `str` | Identifiant du modèle (ex. `cheriftenga/nllb-200-distilled-600M-ewe-lora-v2`). |
| `source_text_version` | `int` | Version du texte à l'origine de la traduction. |
| `translation_timestamp` | `datetime` | Horodatage. |

### 2.8. Bloc « synthèse vocale éwé »

`speech_status` : `PENDING` / `RUNNING` / `SUCCESS` / `FAILED`.

| Champ | Type | Description |
| --- | --- | --- |
| `audio_path` | `Path` | Chemin du fichier audio temporaire généré. |
| `audio_format` | `str` | Format et type MIME (ex. `audio/wav`). |
| `tts_model` | `str` | Identifiant du modèle (ex. `facebook/mms-tts-ewe`). |
| `source_text_version` | `int` | Version du texte éwé à l'origine de l'audio. |
| `speech_timestamp` | `datetime` | Horodatage. |

---

## 3. Fichiers temporaires

### 3.1. Arborescence

Tous les fichiers temporaires vivent sous `TEMP_DIR`, dans un sous-répertoire
propre à chaque session :

```
TEMP_DIR/
└── <session_id>/
    ├── upload/                  # fichiers importés (PDF, DOCX, images)
    │   └── <nonce>.<ext>
    ├── pages/                   # pages individuelles (prévisualisation, OCR)
    │   ├── <nonce>_page_001.<ext>
    │   └── <nonce>_page_002.<ext>
    ├── text/                    # texte extrait/corrigé si persisté temporairement
    │   └── <nonce>.txt
    └── audio/                   # fichier audio éwé généré
        └── <nonce>.wav
```

### 3.2. Règles de nommage et de sécurité

- Les noms de fichiers sont **générés aléatoirement** (UUID ou
  `secrets.token_hex`), jamais à partir du nom fourni par l'utilisateur.
- Le nom d'origine n'est conservé que comme **métadonnée d'affichage**, jamais
  utilisé pour construire un chemin (prévention de *path traversal*).
- Aucun chemin fourni par l'utilisateur ne doit pouvoir accéder à un fichier
  hors du répertoire de session.
- Les types réels sont vérifiés (extension + contenu), pas seulement les
  extensions déclarées.

### 3.3. Limites

| Paramètre | Rôle |
| --- | --- |
| `MAX_UPLOAD_SIZE_MB` | Taille maximale d'un fichier importé. |
| `MAX_DOCUMENT_PAGES` | Nombre maximal de pages. |
| `REQUEST_TIMEOUT_SECONDS` | Délai maximal d'une opération (borne d'expiration). |

---

## 4. Structure de l'explication (`Explanation`)

L'explication produite par Gemini doit être **structurée** (§3.5) et distinguer
trois sources d'information :

- `document` : élément explicitement présent dans le document ;
- `ia` : explication produite par l'IA ;
- `incertain` : information incertaine ou nécessitant vérification.

### 4.1. Sections de l'explication

| Champ | Type | Description |
| --- | --- | --- |
| `document_nature` | `str` | Nature apparente du document. |
| `objective` | `str` | Objectif général. |
| `obligations` | `list[Item]` | Principales obligations de chaque partie. |
| `rights` | `list[Item]` | Droits explicitement mentionnés. |
| `amounts_payments` | `list[Item]` | Montants et modalités de paiement. |
| `dates_deadlines` | `list[Item]` | Dates et délais. |
| `conditions_exceptions` | `list[Item]` | Conditions et exceptions. |
| `consequences` | `list[Item]` | Conséquences prévues en cas de manquement. |
| `ambiguities` | `list[Item]` | Passages ambigus, incomplets ou difficiles. |
| `questions` | `list[Item]` | Questions à poser avant de signer. |
| `summary` | `str` | Résumé général (français simple). |

### 4.2. Élément (`Item`)

| Champ | Type | Description |
| --- | --- | --- |
| `text` | `str` | Libellé de l'élément. |
| `source` | `enum` | `document` / `ia` / `incertain`. |

> **Règle anti-hallucination** (§3.5) : l'IA ne doit pas inventer de clause, de
> référence légale, d'obligation ou de sanction absente du document. Si une
> information n'est pas déterminable, `source = incertain` et le système doit le
> dire clairement.

---

## 5. Nettoyage des données temporaires

### 5.1. Déclencheurs

Le nettoyage doit avoir lieu (§3.8, §6.1, §7.1) :

- après une opération terminée ;
- en cas d'erreur ;
- lors d'un abandon de session ;
- après expiration du délai maximal.

### 5.2. Mécanismes

1. **Nettoyage à la fin de session** : suppression récursive du répertoire
   `TEMP_DIR/<session_id>` et libération de l'état en mémoire.
2. **Endpoint dédié** : `DELETE /api/sessions/{session_id}`.
3. **Nettoyage périodique des fichiers orphelins** : tâche qui parcourt
   `TEMP_DIR` et supprime tout répertoire plus ancien que le TTL (couvre les
   crashs et interruptions).

### 5.3. Limite documentée

La suppression des fichiers côté JuriLex ne garantit pas la suppression
immédiate chez les fournisseurs externes (Gemini). Ce point doit être documenté
dans la politique de confidentialité (§6.5).

---

## 6. Suivi technique autorisé (logs, hors contenu)

Conformément au §6.4, les logs **peuvent** contenir :

| Champ | Type | Description |
| --- | --- | --- |
| `timestamp` | `datetime` | Heure de l'opération. |
| `request_id` | `UUID` | Identifiant de requête aléatoire. |
| `operation` | `str` | Type d'opération (`extract`, `explain`, `translate`, `tts`…). |
| `status` | `str` | Statut technique (`success`, `failed`, `timeout`…). |
| `duration_ms` | `int` | Durée de l'opération. |

Les logs ne doivent **jamais** contenir : le texte des contrats, les textes
extraits, les traductions complètes, les réponses détaillées de Gemini, les clés
API, ni les données personnelles inutiles.

> Ces métriques peuvent être écrites dans des journaux applicatifs. Aucune base
> de données n'est nécessaire pour cela au stade du MVP.

---

## 7. Synthèse

| Type de donnée | Stockage | Persistance | Nettoyage |
| --- | --- | --- | --- |
| État de session | Mémoire vive | Aucune | Fin de session / TTL |
| Documents importés | Disque (`TEMP_DIR`) | Aucune | Fin de session / TTL / orphelins |
| Texte extrait/corrigé | Mémoire (+ éventuel fichier temporaire) | Aucune | Fin de session |
| Explication FR | Mémoire | Aucune | Fin de session |
| Traduction éwé | Mémoire | Aucune | Fin de session |
| Audio éwé | Disque (`TEMP_DIR/audio`) | Aucune | Fin de session / TTL |
| Logs techniques | Journaux (sans contenu) | Bornée, hors contenu | Politique de rétention des logs |

**Aucune base de données persistante n'est créée pour le MVP.**
