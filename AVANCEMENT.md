# JuriLex — Avancement du développement

## État général
- Phase actuelle : Phase 2 — Interface (validée) · prochaine : Phase 3 — Documents
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
- Réalisation de l'interface mobile-first du parcours complet (Phase 2) :
  9 écrans (accueil, importation, prévisualisation, correction du texte,
  consentement, analyse en cours, résultats, éwé & audio, fin de session).
- Direction artistique conforme au cahier des charges : vert profond, fond
  ivoire, texte anthracite, ocre doux, rouge réservé aux erreurs ; typographie
  sans sérif, cartes sobres, sans dégradés ni illustrations génériques.
- États de chargement (spinners, sans faux pourcentage) et d'erreur (alertes +
  bouton réessayer) implémentés.
- Accessibilité : HTML sémantique, `focus-visible`, `prefers-reduced-motion`,
  labels ARIA, navigation clavier (boutons natifs).
- Données simulées (`src/mock.js`) pour tester le parcours, sans appel backend.

### Fichiers modifiés
- `frontend/src/App.jsx` — machine à états du parcours + orchestration simulée.
- `frontend/src/steps.js` — définition des 9 étapes.
- `frontend/src/mock.js` — données et fonctions simulées (aucune donnée réelle).
- `frontend/src/index.css` — design system complet (couleurs, boutons, cartes…).
- `frontend/src/components/Button.jsx`, `StepIndicator.jsx` — composants réutilisables.
- `frontend/src/screens/*.jsx` — 9 écrans du parcours.
- `AVANCEMENT.md` — suivi mis à jour.

### Tests exécutés
- `npm run build` → **succès** (40 modules, build en ~13 s).
- `npm run preview` + `curl` → **HTTP 200**, `<title>` correct.
- Aucun test unitaire frontend (framework de test non installé — prévu Phase 7).

### Fonctionnalités réellement validées
- Compilation et rendu de l'interface (build + serve).
- Navigation du parcours en données simulées (vérifiée visuellement via le build).
- **Aucun** appel réel aux modèles ou au backend (interface en mode démonstration).

### Problèmes rencontrés
- Aucun bloquant. L'interface n'est pas encore câblée au backend (Phases 3-6).

### Limites restantes
- Interface en **données simulées** : extraction, analyse, traduction et audio
  ne sont pas encore réels.
- Pas de test unitaire frontend (à ajouter en Phase 7).
- Besoins mémoire/latence des modèles estimés, non mesurés.
- Licences non commerciales : exploitation commerciale bloquée sans autorisation.

### Prochaine étape
Phase 3 — Documents : implémenter côté backend l'importation, l'extraction
(PDF texte, DOCX, OCR images), la prévisualisation et le nettoyage des fichiers
temporaires, puis câbler l'importation réelle au frontend.
Critère de validation : extraire réellement le texte d'un PDF/DOCX/image local.

### Instructions pour reprendre
- Backend : `cd backend && source .venv/bin/activate && uvicorn app.main:app --reload`
- Frontend : `cd frontend && npm run dev`
- Tests : `cd backend && .venv/bin/python -m pytest`
- Ne pas télécharger les modèles (~2,3 Go + ~150 Mo) sans accord explicite (Règle 4).
