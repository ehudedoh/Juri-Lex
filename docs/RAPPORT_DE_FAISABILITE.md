# JURILEX — Rapport de faisabilité (Phase 0)

**Date :** 2026-10-31
**Statut :** document de faisabilité — les modèles n'ont **pas encore été
exécutés localement**. Les tailles et licences ci-dessous sont vérifiées depuis
les fiches officielles Hugging Face ; les estimations de mémoire et de latence
sont des **ordres de grandeur à confirmer par mesure réelle**.

---

## 1. Verdict de faisabilité

| Dimension | Verdict |
| --- | --- |
| Faisabilité technique (dev, CPU seul) | **Faisable, sous conditions** |
| Faisabilité mémoire (7 Go RAM) | Faisable **un modèle à la fois** (stratégie chargement/déchargement) |
| Exploitation commerciale | **BLOQUÉE** par les licences non commerciales (voir §4) |

**Conclusion :** le MVP de démonstration est techniquement réalisable sur la
machine de développement et sur un serveur CPU doté de 8 Go de RAM. En revanche,
une mise en production **commerciale** est impossible sans autorisation distincte
des ayants droit, les trois modèles étant sous licence **non commerciale**.

---

## 2. Environnement de développement (mesuré)

| Élément | Valeur |
| --- | --- |
| CPU | Intel Core i5-8250U, 4 cœurs / 8 threads (base 1,60 GHz) |
| RAM | 7,0 Go (≈ 2,4 Go disponibles au moment de la mesure) |
| Swap | 4,0 Go (≈ 1,5 Go utilisés) |
| GPU | Intel UHD Graphics 620 — **aucun support CUDA** → inférence **CPU uniquement** |
| Disque | 185 Go libres (suffisant pour les modèles) |
| Python | 3.14.8 (`python3` uniquement, pas d'alias `python`) |
| pip | 26.1.2 — `venv` fonctionnel |
| Node / npm | v24.19.0 / 11.16.0 |
| Git | 2.55.0 (le dossier n'est pas encore un dépôt) |
| torch / transformers | **non installés** |

---

## 3. Modèle de traduction — français ↔ éwé

### 3.1. Identité

- **Adaptateur :** `cheriftenga/nllb-200-distilled-600M-ewe-lora-v2`
  (LoRA uniquement, bidirectionnel FR↔EWE).
- **Modèle de base :** `facebook/nllb-200-distilled-600M`.

### 3.2. Tailles (mesurées sur les dépôts)

| Fichier | Taille |
| --- | --- |
| `pytorch_model.bin` (base NLLB-600M, fp32) | **≈ 2,29 Go** |
| `tokenizer.json` (base) | 17,3 Mo |
| `sentencepiece.bpe.model` (base) | 4,85 Mo |
| `adapter_model.safetensors` (LoRA éwé) | **≈ 9,4 Mo** |
| `tokenizer.json` (adaptateur) | 32 Mo |

### 3.3. Licence

- Adaptateur : **CC-BY-NC-SA-4.0** (héritée de NLLB, **non commerciale** +
  partage à l'identique).
- Modèle de base : **CC-BY-NC-4.0** (non commerciale).
- Données : domaine public (Bible 1913 / Segond 1910) + **ODC-By** (OPUS/NLLB,
  attribution requise).

### 3.4. Codes de langue

- `fra_Latn` (français) et `ewe_Latn` (éwé). Le sens requis par le MVP est
  **FR → EWE**.

### 3.5. Dépendances

- `torch`, `transformers` (ou `transformers<5`, voir §5), `peft`.
- Chargement : `AutoModelForSeq2SeqLM` + `PeftModel.from_pretrained(...)`.

### 3.6. Contraintes connues (fiche NLLB-200)

- Modèle de **recherche**, « not released for production deployment ».
- Entraîné sur des séquences ≤ **512 tokens** → traduire par segments courts.
- Domaine généraliste ; **le domaine juridique n'est pas couvert**.
- Ne peut pas produire de traduction **certifiée**.

### 3.7. Estimation mémoire et latence (à mesurer)

| Grandeur | Estimation |
| --- | --- |
| RAM (poids fp32) | ≈ 2,4 Go + surcoût d'inférence → **≈ 3 Go** au total |
| RAM (si int8 quantifié) | ≈ 600 Mo (variantes quantifiées existent sur le Hub) |
| Téléchargement initial | ≈ 2,3 Go |
| Latence CPU (i5-8250U) | de l'ordre de **10–60 s** selon la longueur du texte |

---

## 4. Modèle de synthèse vocale — éwé

### 4.1. Identité

- `facebook/mms-tts-ewe` — checkpoint **VITS** (TTS), 36,3 M paramètres, F32.

### 4.2. Taille et mémoire

| Grandeur | Valeur |
| --- | --- |
| Poids (F32) | ≈ **145 Mo** |
| RAM d'inférence | ≈ **300–500 Mo** |
| Dépendances | `torch`, `transformers` (≥ 4.33), `accelerate`, `scipy` (écriture WAV) |
| Chargement | `VitsModel.from_pretrained(...)` + `AutoTokenizer` |

### 4.3. Licence

- **CC-BY-NC-4.0** (non commerciale).

### 4.4. Contraintes

- Génération **non déterministe** (durée stochastique) → figer une graine si la
  reproductibilité est requise pour les tests.
- Échantillonnage retourné par `model.config.sampling_rate` (à reporter dans le
  fichier WAV).

---

## 5. Compatibilité des dépendances (vérifiée sur PyPI)

| Paquet | Version | Python 3.14 |
| --- | --- | --- |
| `torch` | 2.15.0 | ✅ supporté (classifier 3.14) |
| `transformers` | **5.22.1** | ✅ (≥ 3.11) |
| `accelerate` | 1.15.0 | ✅ (≥ 3.10) |
| `peft` | 0.21.2 | ✅ (≥ 3.10) |

### ⚠️ Risque `transformers` v5

La fiche NLLB-200 signale : **la pipeline `translation` n'existe plus en
transformers v5** ; l'exemple officiel de l'adaptateur utilise néanmoins
`AutoModelForSeq2SeqLM` + `PeftModel` directement (indépendant de la pipeline).

**Recommandation :** épingler initialement `transformers<5.0.0` pour coller aux
exemples documentés, puis valider la compatibilité v5 (en particulier `VitsModel`
et `AutoModelForSeq2SeqLM`) avant toute montée de version. Cette validation
constitue la première tâche de la Phase 1.

---

## 6. Bilan mémoire (CPU uniquement)

| Composant | RAM estimée |
| --- | --- |
| FastAPI + extraction/OCR | ≈ 0,5–1 Go |
| NLLB-600M (fp32) | ≈ 3 Go |
| MMS-TTS (F32) | ≈ 0,5 Go |
| **Total simultané (fp32)** | **≈ 4,5–5 Go** → trop juste sur 7 Go |

**Stratégie retenue :** chargement **à la demande** (traduction puis TTS, jamais
les deux gros modèles résidant en mémoire en même temps), et/ou variante
quantifiée int8 du NLLB si la RAM l'exige. Le choix entre « garder en mémoire » et
« charger/décharger » devra être tranché sur des **mesures réelles** (§4.4 du
cahier des charges), pas sur des suppositions.

---

## 7. Options d'hébergement (comparaison préliminaire)

| Option | Avantages | Inconvénients |
| --- | --- | --- |
| **Serveur CPU dédié/VPS (≥ 8 Go RAM)** | Modèles exécutés localement, pas de coût par requête, maîtrise des données | Serveur payant ; latence CPU pour NLLB ; RAM à provisionner |
| **Inférence distante gérée** | Pas de charge modèle locale | Aucun des deux modèles n'est proposé par un *Inference Provider* → nécessiterait un déploiement auto-hébergé ou un modèle de substitution |
| **API de traduction tierce** | Simple, scalable | Google Translate supporte l'éwé mais contredit l'exigence « vrai modèle NLLB local » ; coût par volume ; envoi de données à un tiers |

**Recommandation :** serveur CPU local (option 1), conformément à l'esprit du
cahier des charges (modèles chargés côté backend, pas par le navigateur). La
décision définitive reste soumise à l'évaluation du §12 du cahier des charges.

---

## 8. Risques techniques et financiers

| # | Risque | Impact | Atténuation |
| --- | --- | --- | --- |
| R1 | **Licences non commerciales** (CC-BY-NC(-SA)) des trois modèles | Bloquant pour toute exploitation commerciale | Obtenir une autorisation des ayants droit, ou remplacer par un modèle à licence permissive ; documenter clairement |
| R2 | **RAM insuffisante** en chargement simultané | Crash / OOM | Chargement à la demande + quantification int8 + mesures réelles |
| R3 | **Latence CPU** du NLLB-600M sur i5-8250U | Expérience utilisateur dégradée | Traduire uniquement l'explication (pas le document), segmentation ≤ 512 tokens, file d'attente / timeout |
| R4 | **`transformers` v5** (changements d'API) | Exemples obsolètes, incompatibilité | Épingler `transformers<5` puis valider la montée de version |
| R5 | **Qualité juridique** du domaine (non couvert par l'entraînement) | Traductions inexactes sur clauses juridiques | Corpus de test juridique (≥ 30 phrases), validation par locuteurs éwé, avertissement « non certifié » |
| R6 | **Coût d'hébergement** d'un serveur capable de faire tourner les modèles | Budget mensuel | Mesurer taille/mémoire/latence avant de choisir (§7.2) |
| R7 | **Dépendance aux données externes** (ODC-By) | Obligation d'attribution | Documenter l'attribution OPUS/NLLB |
| R8 | **Non-reproductibilité TTS** | Tests audio instables | Figer la graine (`torch.manual_seed`) dans les tests |

---

## 9. Décisions à valider avant la production

Reprise du §12 du cahier des charges, complétée par la Phase 0 :

1. Hébergement CPU ou service d'inférence distant.
2. Faisabilité des deux modèles sur un même serveur (RAM réelle à mesurer).
3. Budget mensuel maximal.
4. Limite de taille et de pages des documents.
5. Temps maximal accepté pour chaque opération.
6. Politique de conservation chez les fournisseurs externes.
7. **Licences et autorisations commerciales** (bloquant — R1).
8. Qualité linguistique minimale acceptable.
9. Modalités de validation par des locuteurs éwé.
10. Procédure de suppression des ressources temporaires.

---

## 10. Statut de validation (honnête)

| Élément | Statut |
| --- | --- |
| Licences des modèles | ✅ Vérifié sur les fiches officielles |
| Tailles des poids | ✅ Mesuré via l'API Hugging Face |
| Versions de dépendances / compat. Python 3.14 | ✅ Vérifié sur PyPI |
| Besoins mémoire | ⚠️ **Estimé, non mesuré** |
| Latence d'inférence | ⚠️ **Estimé, non mesuré** |
| Chargement réel des modèles | ❌ **Non testé** (nécessite téléchargement ≈ 2,3 Go) |
| Traduction réelle FR→EWE | ❌ Non testé |
| Génération audio réelle | ❌ Non testé |

**Aucune réussite n'est déclarée tant que les modèles n'ont pas été exécutés**
(Règle 3 du protocole).

---

## 11. Prochaine étape

Créer l'environnement backend (`backend/`, venv Python), épingler les dépendances
(`torch`, `transformers<5`, `accelerate`, `peft`), et valider **l'import** des
classes requises sur Python 3.14 **avant** tout téléchargement des poids. Le
téléchargement des modèles (~2,3 Go + ~150 Mo) sera proposé séparément, après
accord explicite, conformément à la Règle 4.
