# JURILEX
## Cahier des charges fonctionnel et technique
**Version 1.0 — Projet d'assistance à la compréhension des documents juridiques au Togo**

**Signature :** Comprendre avant de signer.

---

# 1. PRÉSENTATION DU PROJET

## 1.1. Contexte et problématique

Au Togo, de nombreux documents administratifs et juridiques sont rédigés dans un français qui peut être difficile à comprendre pour les personnes qui ne maîtrisent pas le vocabulaire juridique.

Un contrat de travail, un contrat de location ou un autre document engageant peut contenir des obligations, des délais, des conditions, des pénalités et des conséquences que son signataire ne comprend pas entièrement.

Les difficultés sont encore plus importantes pour les personnes qui comprennent mieux une langue locale que le français.

Cette situation peut empêcher certaines personnes de prendre des décisions suffisamment éclairées avant de signer un document.

JuriLex vise à réduire cette difficulté en rendant les informations contenues dans les documents plus accessibles, grâce à une interface simple et à des outils d'intelligence artificielle.

## 1.2. Solution proposée

JuriLex est une application web progressive (PWA) qui permet à un utilisateur de transmettre un document, d'en extraire le texte, d'obtenir une explication en français simple, puis de consulter une traduction en éwé et de l'écouter lorsqu'une génération audio est disponible.

L'application doit permettre à l'utilisateur de mieux comprendre ce qu'il lit, sans lui demander de maîtriser des outils informatiques complexes.

La solution associe :
- L'extraction de texte depuis des documents.
- La reconnaissance optique de caractères (OCR) pour les documents photographiés ou numérisés.
- Un modèle d'IA générative pour expliquer le contenu.
- Un modèle de traduction français-éwé.
- Un modèle de synthèse vocale en éwé.
- Une interface web accessible sur téléphone, tablette et ordinateur.

## 1.3. Objectifs

Les objectifs principaux sont les suivants :

1. Permettre à un utilisateur de soumettre un document facilement.
2. Extraire le texte de manière fiable.
3. Expliquer le contenu dans un français accessible.
4. Faire ressortir les obligations, les droits mentionnés, les montants, les dates, les délais, les conditions et les risques apparents.
5. Traduire l'explication en éwé à l'aide d'un véritable modèle de traduction.
6. Générer une véritable sortie audio en éwé avec un modèle de synthèse vocale.
7. Réduire la collecte et la conservation de données personnelles.
8. Proposer une expérience adaptée au public togolais, y compris aux personnes peu familières avec les applications numériques.
9. Concevoir une architecture déployable et maintenable, dont les coûts peuvent être évalués avant une mise en production.

## 1.4. Public cible

Le public prioritaire comprend :
- Les travailleurs qui souhaitent mieux comprendre un contrat de travail.
- Les locataires et les personnes qui s'apprêtent à louer un logement.
- Les personnes qui ont des difficultés avec le français administratif ou juridique.
- Les personnes qui préfèrent écouter une explication plutôt que lire un long texte.
- Les utilisateurs de smartphones disposant d'une connexion Internet parfois limitée.

L'interface doit être compréhensible sans connaissances techniques ou juridiques préalables.

---

# 2. PÉRIMÈTRE FONCTIONNEL

## 2.1. Fonctionnalités prioritaires du MVP

La première version utilisable doit proposer les fonctions suivantes :

1. Importer un document PDF ou DOCX.
2. Photographier un document ou importer une image.
3. Prévisualiser les pages et supprimer ou remplacer une page avant traitement.
4. Extraire le texte du document.
5. Permettre à l'utilisateur de corriger le texte extrait.
6. Demander un consentement explicite avant l'envoi du texte au service d'IA externe.
7. Produire une explication en français simple.
8. Afficher les éléments importants du document.
9. Traduire l'explication en éwé à l'aide du modèle prévu.
10. Générer un fichier audio en éwé à l'aide du modèle de synthèse vocale.
11. Lire, mettre en pause et relancer l'audio.
12. Permettre à l'utilisateur de recommencer avec un autre document.
13. Gérer les erreurs sans perdre inutilement le texte que l'utilisateur est en train de corriger.
14. Nettoyer les fichiers temporaires après le traitement.

Ces fonctionnalités doivent être considérées comme des objectifs à réaliser, et non comme des fonctionnalités déjà opérationnelles.

## 2.2. Fonctionnalités envisagées pour des versions ultérieures

L'architecture pourra être préparée pour accueillir ultérieurement :
- Une fonctionnalité permettant de décrire une situation personnelle pour mieux comprendre le problème rencontré.
- Une consultation guidée des droits applicables.
- Des explications plus avancées selon le type de document.
- D'autres langues locales, après validation des modèles disponibles.
- Une orientation vers des professionnels compétents lorsque la situation le nécessite.

Ces fonctionnalités ne doivent pas encombrer le MVP ni être présentées comme disponibles avant leur implémentation et leurs tests.

---

# 3. PARCOURS UTILISATEUR

## 3.1. Accueil

L'utilisateur arrive sur une page simple présentant clairement l'utilité de JuriLex.

Le message principal doit expliquer la fonction du service en termes compréhensibles.

Action principale :
**« Comprendre un document »**

L'accueil doit aussi comporter :
- Une explication courte du fonctionnement.
- Les formats de documents acceptés.
- Une mention claire des limites de l'IA.
- Une indication précisant que le document n'est pas conservé dans un historique personnel.
- Un accès aux informations de confidentialité et aux conditions d'utilisation.

Ne pas placer un tableau de bord complexe, des statistiques inutiles ou plusieurs fonctionnalités secondaires au premier plan.

## 3.2. Importation du document

L'utilisateur doit pouvoir :
- Choisir un fichier PDF.
- Choisir un fichier DOCX.
- Photographier un document depuis un appareil compatible.
- Importer une ou plusieurs images de pages.

L'interface doit préciser les formats, la taille maximale et les éventuelles limites de pages.

Avant de commencer le traitement, l'utilisateur doit pouvoir :
- Prévisualiser les pages.
- Supprimer une page.
- Remplacer une page.
- Modifier l'ordre des pages, si plusieurs pages sont importées.
- Annuler et recommencer.

Le système doit vérifier le type et la taille du fichier côté frontend et côté backend. Le contrôle effectué dans le navigateur ne suffit pas à garantir la sécurité.

## 3.3. Extraction et correction du texte

Le backend doit choisir une méthode adaptée au document :

- PDF contenant du texte : extraction directe.
- DOCX : extraction du texte du document.
- PDF scanné ou photographie : OCR.
- Document mixte : extraction directe lorsque possible, puis OCR des pages qui le nécessitent.

Le système ne doit pas envoyer automatiquement à l'IA un texte manifestement vide ou inutilisable.

Après l'extraction, l'utilisateur doit voir le texte reconnu dans une zone modifiable.

L'interface doit signaler que l'OCR peut produire des erreurs, notamment sur :
- Les noms propres.
- Les montants.
- Les dates.
- Les numéros.
- Les caractères peu lisibles.
- Les tableaux et les mises en page complexes.

L'utilisateur doit pouvoir corriger le texte avant l'analyse.

Une fois le texte modifié, tout résultat précédent qui dépendait de l'ancienne version doit être invalidé. Une ancienne traduction ne doit jamais être présentée comme si elle correspondait au nouveau texte.

## 3.4. Consentement avant analyse

Avant tout envoi à Gemini ou à un autre service externe, afficher un message compréhensible précisant :
- Que le texte corrigé sera transmis au service d'IA utilisé pour produire l'explication.
- Que le texte peut contenir des informations personnelles.
- Que l'utilisateur doit vérifier qu'il accepte ce traitement.
- Que JuriLex ne doit pas conserver volontairement le contenu du document dans un historique personnel.

L'utilisateur doit effectuer une action explicite pour consentir.

Sans consentement, aucun appel au service d'IA externe ne doit être réalisé.

Ce consentement doit être vérifié par le backend, et pas uniquement représenté par une case à cocher dans React.

Le consentement donné à l'analyse ne doit pas être interprété comme une autorisation illimitée pour d'autres utilisations.

## 3.5. Analyse et explication

Après consentement, le backend transmet le texte à Gemini à l'aide d'une clé conservée exclusivement côté serveur.

Le système doit demander une explication structurée en français simple.

L'explication doit chercher à présenter :
1. La nature apparente du document.
2. Son objectif général.
3. Les principales obligations de chaque partie, lorsqu'elles sont identifiables.
4. Les droits explicitement mentionnés.
5. Les montants et les modalités de paiement.
6. Les dates et les délais.
7. Les conditions et les exceptions.
8. Les conséquences explicitement prévues en cas de manquement.
9. Les passages ambigus, incomplets ou difficiles à interpréter.
10. Les questions que l'utilisateur pourrait devoir poser avant de signer.

L'application doit distinguer :
- Les éléments explicitement présents dans le document.
- Les explications produites par l'IA.
- Les informations qui restent incertaines ou qui nécessitent une vérification.

L'IA ne doit pas inventer une clause absente du document, une référence légale, une obligation ou une sanction.

Si une information n'est pas présente ou ne peut pas être déterminée avec suffisamment de confiance, le système doit le dire clairement.

L'explication doit être structurée et lisible, plutôt que présentée comme un long bloc de texte.

## 3.6. Traduction français-éwé

Après la génération de l'explication française, le backend doit pouvoir la transmettre au modèle de traduction retenu.

Modèle à étudier :
`cheriftenga/nllb-200-distilled-600M-ewe-lora-v2`

Le développeur doit vérifier :
- Les conditions de téléchargement.
- Le modèle de base nécessaire.
- La compatibilité de l'adaptateur LoRA.
- Les codes de langue utilisés par le modèle.
- Les dépendances et leurs versions.
- La licence et les conditions d'utilisation.
- Les besoins réels en mémoire.
- La qualité sur des phrases synthétiques et des textes juridiques.

Le modèle doit être chargé et exécuté côté backend, et non dans le navigateur.

La traduction doit porter sur l'explication produite, et non nécessairement sur l'intégralité du document original.

Les montants, dates, délais, négations, interdictions et conditions doivent faire partie des tests prioritaires.

La traduction automatique doit être présentée comme telle. Elle ne doit pas être qualifiée de traduction juridique certifiée.

Une validation par des personnes compétentes en éwé est indispensable avant de revendiquer une qualité linguistique élevée.

## 3.7. Synthèse vocale en éwé

Modèle à étudier :
`facebook/mms-tts-ewe`

Le backend doit charger le modèle et générer un fichier audio à partir du texte éwé.

Le fonctionnement attendu est le suivant :
1. Vérifier que le texte à prononcer n'est pas vide.
2. Préparer le texte pour l'inférence.
3. Générer l'audio.
4. Vérifier que le fichier produit est valide.
5. Retourner l'audio au frontend.
6. Permettre sa lecture dans le navigateur.
7. Supprimer le fichier temporaire lorsqu'il n'est plus nécessaire, selon une stratégie documentée.

L'interface doit proposer :
- Un bouton « Écouter en éwé ».
- Un état de chargement pendant la génération.
- Des commandes de lecture et de pause.
- Un message compréhensible si la génération échoue.
- Une possibilité de réessayer.

L'API SpeechSynthesis du navigateur ne doit pas être considérée comme le moteur principal de synthèse en éwé. Elle ne garantit pas qu'une voix éwé soit disponible.

Un mécanisme de secours pour la lecture française peut être envisagé, mais il doit rester clairement distinct du modèle MMS TTS.

## 3.8. Fin de session

L'utilisateur doit pouvoir terminer le traitement et recommencer avec un autre document.

Le système doit supprimer les données temporaires dont il a la maîtrise, notamment :
- Les fichiers importés.
- Les images intermédiaires.
- Les textes temporaires.
- Les résultats d'analyse conservés temporairement.
- Les fichiers audio générés.

Le nettoyage doit également être prévu en cas d'erreur, d'abandon ou d'interruption de traitement.

Le backend ne doit pas créer d'historique des contrats ni de base de données contenant les documents analysés.

Les modalités de suppression et les limites liées aux services tiers doivent être documentées avec précision.

---

# 4. ARCHITECTURE TECHNIQUE

## 4.1. Principes

Le projet doit être développé depuis zéro avec une séparation claire entre frontend et backend.

La stack proposée est :

### Frontend
- HTML.
- CSS.
- JavaScript moderne, sans TypeScript.
- React.
- Vite.
- PWA avec manifeste et service worker.

### Backend
- Python.
- FastAPI.
- Pydantic pour la validation des données.
- Un client Python adapté à l'API Gemini.
- PyTorch et Transformers pour les modèles de traduction et de synthèse vocale.
- Une bibliothèque d'extraction de texte adaptée aux formats acceptés.
- Un moteur OCR choisi après évaluation de sa compatibilité et de ses performances.

Le développeur peut proposer une alternative uniquement si un obstacle technique concret la justifie. Toute modification importante de la stack doit être expliquée avant son adoption.

## 4.2. Schéma logique

Le frontend React communique avec le backend Python.

Le backend orchestre les opérations :

**Document → Extraction/OCR → Correction par l'utilisateur → Consentement → Gemini → Explication française → Modèle de traduction → Texte éwé → Modèle TTS → Audio.**

Les responsabilités doivent rester séparées :
- Le frontend gère l'interface, les interactions et la lecture audio.
- Le backend gère la validation, l'extraction, les appels aux modèles et le nettoyage.
- Gemini produit l'explication.
- NLLB adapté à l'éwé produit la traduction.
- MMS TTS génère la voix éwé.

Le navigateur ne doit jamais recevoir la clé API Gemini.

## 4.3. Endpoints à prévoir

Les routes suivantes sont indicatives. Elles doivent être adaptées à l'implémentation réelle.

- `GET /api/health` : vérifier l'état général du service.
- `POST /api/documents/extract` : extraire le texte d'un document.
- `POST /api/explanations` : produire une explication après vérification du consentement.
- `POST /api/translations` : traduire un texte en éwé.
- `POST /api/speech` : générer l'audio éwé.
- `DELETE /api/sessions/{session_id}` : supprimer les ressources temporaires d'une session, si cette architecture de session est retenue.

Les endpoints ne doivent pas accepter aveuglément toutes les données reçues.

Les réponses d'erreur doivent être structurées et ne pas révéler de détails internes sensibles.

La génération audio doit utiliser un format de réponse adapté au navigateur, avec un type MIME correct et une gestion claire des erreurs.

## 4.4. Gestion des modèles

Les modèles lourds ne doivent pas être chargés dans le navigateur.

Le backend doit éviter de recharger inutilement un modèle à chaque requête.

Le développeur doit comparer deux stratégies :
- Charger un modèle en mémoire et le réutiliser.
- Charger et décharger les modèles selon les besoins lorsque les ressources sont limitées.

La décision doit reposer sur des mesures réelles de mémoire, de latence et de concurrence.

Le service doit gérer les cas où :
- Le modèle n'est pas encore téléchargé.
- Le modèle ne peut pas être chargé.
- La mémoire disponible est insuffisante.
- Une requête arrive pendant une génération audio.
- L'inférence échoue.
- Une requête dépasse le délai maximal autorisé.

Le démarrage du serveur ne doit pas être considéré comme une preuve que les modèles sont opérationnels. Leur état doit être vérifié explicitement.

## 4.5. Configuration et secrets

Prévoir un fichier `.env.example` contenant uniquement des noms de variables et des valeurs fictives.

Exemples de variables :
- `GEMINI_API_KEY`
- `GEMINI_MODEL`
- `MAX_UPLOAD_SIZE_MB`
- `MAX_DOCUMENT_PAGES`
- `MODEL_CACHE_DIR`
- `TEMP_DIR`
- `REQUEST_TIMEOUT_SECONDS`
- `ALLOWED_ORIGINS`

Les valeurs définitives doivent être configurées dans l'environnement d'exécution.

Le fichier `.env` ne doit jamais être commité.

Les secrets ne doivent apparaître ni dans le code frontend, ni dans les logs, ni dans les messages d'erreur retournés aux utilisateurs.

## 4.6. Absence de base de données

Le MVP ne nécessite pas de base de données pour les comptes utilisateurs, l'historique ou le stockage des documents.

Les fichiers et résultats doivent être traités temporairement.

Une éventuelle base de données de suivi technique ne pourrait être ajoutée qu'après justification, en excluant les documents, les textes personnels et les contenus d'analyse.

Aucun historique de contrats ne doit être introduit par commodité.

---

# 5. DESIGN ET EXPÉRIENCE UTILISATEUR

## 5.1. Principes visuels

L'identité visuelle doit être professionnelle, chaleureuse, rassurante et accessible.

JuriLex s'adresse à des personnes qui peuvent être peu à l'aise avec les interfaces numériques ou le vocabulaire juridique. L'interface doit donc inspirer confiance sans donner l'impression d'un logiciel réservé aux experts.

Éviter :
- Les interfaces cyberpunk.
- Les dégradés fluorescents bleu-cyan-violet.
- Les illustrations génériques de robots ou de cerveaux artificiels.
- Les tableaux de bord surchargés.
- Les petits textes gris peu lisibles.
- Les animations excessives.
- Les termes techniques non expliqués.
- Les alertes dramatiques ou les couleurs évoquant systématiquement le danger.

L'interface ne doit pas ressembler à un générateur de maquettes IA standard.

## 5.2. Direction artistique proposée

Adopter une identité sobre, contemporaine et humaine.

Palette de départ à tester :
- Vert profond pour les éléments de confiance et les actions principales.
- Fond ivoire ou blanc cassé pour réduire la dureté visuelle.
- Texte anthracite pour garantir une bonne lisibilité.
- Ocre ou ambre doux pour attirer l'attention sur les informations importantes.
- Rouge réservé aux erreurs ou aux situations nécessitant une attention particulière.

Ces couleurs sont des propositions initiales. Leur contraste doit être vérifié et elles ne doivent pas être utilisées seules pour transmettre une information.

Utiliser :
- Une typographie sans sérif très lisible.
- Des titres courts et explicites.
- Des espaces généreux.
- Des cartes simples lorsque cela facilite la lecture.
- Des icônes cohérentes et compréhensibles.
- Des illustrations sobres, uniquement lorsqu'elles apportent une réelle valeur.

## 5.3. Adaptation aux téléphones

Le mobile est le support prioritaire.

L'interface doit :
- Fonctionner à partir de petites largeurs d'écran.
- Présenter un bouton principal facilement repérable.
- Éviter les formulaires interminables.
- Utiliser des zones tactiles suffisamment grandes.
- Permettre la sélection et la photographie de documents sur les appareils compatibles.
- Ne pas obliger l'utilisateur à faire défiler horizontalement.
- Conserver une hiérarchie visuelle claire.
- Afficher correctement les textes longs et les résultats traduits.

Le rendu doit aussi être testé sur ordinateur et tablette.

## 5.4. Écrans à concevoir

### Écran 1 : Accueil
- Logo et nom JuriLex.
- Signature « Comprendre avant de signer ».
- Une phrase simple expliquant le service.
- Bouton principal « Comprendre un document ».
- Courte présentation des étapes.
- Accès à la confidentialité et aux limites du service.

### Écran 2 : Importation
- Zone d'importation visible.
- Bouton pour choisir un fichier.
- Action pour prendre une photo sur un appareil compatible.
- Formats acceptés.
- Taille et nombre de pages autorisés.
- Instructions simples.

### Écran 3 : Prévisualisation
- Affichage des pages.
- Suppression, remplacement et réorganisation.
- Bouton pour lancer l'extraction.
- Retour simple vers l'importation.

### Écran 4 : Vérification du texte
- Texte extrait dans une zone modifiable.
- Indication des erreurs possibles de reconnaissance.
- Bouton pour poursuivre.
- Possibilité de revenir en arrière.

### Écran 5 : Consentement
- Explication concise du traitement.
- Information sur le service d'IA externe.
- Action explicite pour accepter.
- Action claire pour annuler.

### Écran 6 : Analyse en cours
- Étapes de progression compréhensibles.
- Indication de l'opération en cours.
- Aucun pourcentage artificiel si la progression réelle n'est pas mesurable.
- Possibilité de gérer une erreur ou une interruption.

### Écran 7 : Résultats
Organiser les résultats en sections distinctes :
- Résumé général.
- Obligations et responsabilités.
- Montants et paiements.
- Dates et délais.
- Conditions et exceptions.
- Points à vérifier.
- Explication complète.

Les sections doivent être affichées seulement lorsque des informations pertinentes existent.

### Écran 8 : Éwé et audio
- Texte français clairement identifié.
- Traduction éwé clairement identifiée.
- Bouton de génération ou de lecture audio.
- État de génération.
- Commandes audio.
- Message indiquant que la traduction est automatique.

### Écran 9 : Fin de session
- Action « Analyser un autre document ».
- Confirmation claire du nettoyage lorsque celui-ci a été effectué.
- Aucune proposition d'historique des documents.

## 5.5. Accessibilité et simplicité

Respecter les principes suivants :
- Contraste suffisant.
- Taille de texte confortable.
- Navigation au clavier.
- Focus visible.
- Libellés explicites pour les champs.
- Messages d'erreur rédigés en langage simple.
- Structure cohérente des titres.
- États de chargement accessibles.
- Boutons identifiables sans devoir deviner leur fonction.
- Respect des préférences de réduction des animations.

Éviter les animations qui ralentissent le parcours ou consomment inutilement les ressources du téléphone.

## 5.6. Ton rédactionnel

Utiliser un français simple, poli et direct.

Exemple :
« Votre document a été lu. Vérifiez le texte ci-dessous avant de continuer. »

Éviter :
« Le pipeline OCR a terminé la normalisation du contenu. »

Les messages doivent expliquer ce qui se passe et, si nécessaire, comment continuer.

---

# 6. CONFIDENTIALITÉ ET SÉCURITÉ

## 6.1. Principe de minimisation

Le système doit traiter uniquement les données nécessaires au service demandé.

Il ne doit pas conserver de documents, de textes extraits, de traductions ou de fichiers audio dans un historique utilisateur.

Les fichiers temporaires doivent être supprimés :
- Après une opération terminée.
- Après une erreur.
- Lorsqu'une session est abandonnée.
- Après expiration du délai maximal prévu.

Prévoir un mécanisme périodique de nettoyage pour les fichiers orphelins.

## 6.2. Sécurité des documents

Le backend doit :
- Limiter la taille des fichiers.
- Limiter le nombre de pages.
- Vérifier les formats réels.
- Générer des noms de fichiers temporaires non prévisibles.
- Empêcher les chemins fournis par les utilisateurs d'accéder à d'autres fichiers.
- Ne pas exécuter le contenu d'un document.
- Limiter les ressources consommées par l'extraction et l'OCR.
- Gérer les fichiers malformés.
- Empêcher les accès non autorisés aux ressources temporaires.

## 6.3. Protection contre les injections de prompt

Un document peut contenir des phrases qui ressemblent à des instructions destinées à une IA.

Le système doit traiter son contenu comme des données à analyser, jamais comme des instructions capables de modifier le comportement du système.

Les instructions du modèle doivent préciser :
- Que le contenu du document est non fiable.
- Qu'il ne doit pas remplacer les instructions système.
- Qu'aucune instruction contenue dans le document ne doit autoriser une divulgation de secrets ou une opération non prévue.
- Que les informations absentes du document ne doivent pas être inventées.

Ajouter des tests spécifiques pour ce risque.

## 6.4. Logs

Les logs peuvent contenir :
- L'heure et la durée des opérations.
- Le type d'opération.
- Le statut technique.
- Un identifiant de requête aléatoire.

Ils ne doivent pas contenir :
- Le texte des contrats.
- Les textes extraits.
- Les traductions complètes.
- Les réponses détaillées de Gemini.
- Les clés API.
- Les données personnelles inutiles.

## 6.5. Services externes

Le fait de supprimer les fichiers du serveur JuriLex ne garantit pas automatiquement la suppression immédiate des données chez les fournisseurs externes.

Les conditions de traitement, de conservation et d'utilisation des données des services externes doivent être examinées avant la mise en production.

La politique de confidentialité doit décrire honnêtement le fonctionnement réel de l'application.

## 6.6. PWA et cache

Le service worker peut mettre en cache les ressources statiques nécessaires à l'interface.

Il ne doit pas mettre en cache :
- Les documents importés.
- Les textes extraits.
- Les explications personnalisées.
- Les traductions.
- Les fichiers audio générés.
- Les réponses contenant des informations personnelles.

Les réponses sensibles doivent recevoir des en-têtes HTTP adaptés, notamment une politique de cache appropriée.

L'application ne doit pas prétendre offrir une analyse juridique complète hors ligne si le backend et Gemini sont inaccessibles.

---

# 7. DÉPLOIEMENT ET EXPLOITATION

## 7.1. Architecture de production envisagée

Le déploiement comprendra :
- Le frontend PWA.
- Le backend Python.
- Le modèle de traduction et son modèle de base.
- Le modèle de synthèse vocale.
- Les dépendances nécessaires à l'extraction et à l'OCR.
- La configuration sécurisée de Gemini.
- Un mécanisme de nettoyage des ressources temporaires.

Les modèles doivent être installés ou téléchargés sur le serveur et exécutés par le backend, et non téléchargés par chaque utilisateur.

## 7.2. Évaluation de l'hébergement

Avant de choisir un hébergeur, mesurer :
- La taille réelle des fichiers de modèles.
- La mémoire maximale consommée par chaque modèle.
- Le temps de chargement.
- La latence d'inférence sur CPU.
- La latence de génération audio.
- La consommation disque.
- Le comportement en cas de requêtes simultanées.
- Les coûts mensuels et les limites du fournisseur.

Comparer au minimum :
1. Un serveur CPU avec les modèles hébergés localement sur ce serveur.
2. Une solution d'inférence distante, si elle est nécessaire ou économiquement plus adaptée.

La décision doit être documentée.

Un hébergement web gratuit classique ne doit pas être supposé capable d'exécuter des modèles lourds. Il faut vérifier ses limites de mémoire, de durée d'exécution, de disque, de réseau et d'utilisation commerciale.

## 7.3. Coûts

Établir un budget prévisionnel comprenant :
- L'hébergement du frontend.
- L'hébergement du backend.
- Le stockage des modèles.
- La mémoire et la puissance de calcul.
- Les éventuels coûts de l'API Gemini.
- La bande passante.
- Les sauvegardes techniques nécessaires.
- La surveillance et la maintenance.

Les modèles exécutés localement sur le serveur évitent de payer une API d'inférence par requête, mais le serveur lui-même reste payant ou limité par les conditions de l'offre choisie.

## 7.4. Disponibilité

L'application doit afficher un message compréhensible lorsque :
- Le backend est indisponible.
- Gemini ne répond pas.
- Le modèle de traduction est indisponible.
- Le modèle TTS n'est pas chargé.
- Le serveur est temporairement surchargé.

Ne pas afficher un faux résultat pour donner l'impression que le service fonctionne.

La disponibilité de chaque composant doit pouvoir être vérifiée séparément.

---

# 8. TESTS ET VALIDATION

## 8.1. Tests techniques

Prévoir des tests automatisés pour :
- La validation des fichiers.
- L'extraction de texte.
- L'OCR.
- Le consentement.
- La génération de l'explication.
- La traduction.
- La synthèse vocale.
- Le nettoyage.
- La gestion des erreurs.
- Les limites de taille.
- La sécurité des endpoints.
- Les changements de texte après une première analyse.

Les tests doivent distinguer les résultats simulés des appels réels aux modèles.

## 8.2. Tests linguistiques

Créer un corpus synthétique d'au moins 30 phrases françaises couvrant :
- Les obligations.
- Les interdictions.
- Les montants.
- Les dates.
- Les délais.
- Les conditions.
- Les exceptions.
- Les pénalités.
- La résiliation.
- Les ambiguïtés.

Évaluer :
- La fidélité de la traduction.
- La conservation des nombres.
- La conservation des négations.
- La conservation des relations entre les parties.
- La qualité de la prononciation.
- L'intelligibilité de l'audio.

Faire relire les traductions et écouter les audios par des personnes compétentes en éwé.

Ne pas présenter une mesure automatique comme une preuve suffisante de qualité juridique.

## 8.3. Tests utilisateurs

Faire tester le prototype par un petit groupe de personnes correspondant au public cible.

Observer :
- La facilité d'importation.
- La compréhension des instructions.
- La facilité de correction du texte.
- La compréhension de l'explication française.
- La compréhension de la traduction éwé.
- La facilité d'écoute de l'audio.
- La confiance accordée au résultat.
- Les difficultés rencontrées.

Les retours doivent permettre d'améliorer l'interface et de repérer les incompréhensions.

## 8.4. Tests de performance

Mesurer séparément :
- Le temps d'extraction.
- Le temps de réponse de Gemini.
- Le temps de traduction.
- Le temps de génération audio.
- La mémoire utilisée par chaque modèle.
- La mémoire utilisée lorsque plusieurs opérations s'enchaînent.

Définir des seuils cibles après les premiers essais. Ne pas inventer des performances qui n'ont pas été mesurées.

## 8.5. Critères de validation du MVP

Le MVP est validé lorsque :
- Un utilisateur peut importer un document pris en charge.
- Le texte extrait peut être corrigé.
- Aucun appel à Gemini n'est réalisé sans consentement.
- L'explication est réellement produite par le service configuré.
- La traduction utilise réellement le modèle sélectionné.
- L'audio éwé est réellement généré par MMS TTS.
- L'audio peut être écouté dans le navigateur.
- Les erreurs sont gérées proprement.
- Les fichiers temporaires sont nettoyés.
- Aucun historique de documents n'est conservé.
- Les tests automatisés passent.
- Les limites linguistiques et techniques sont documentées.
- Le déploiement réel est testé sur un environnement cible.

---

# 9. LIMITES JURIDIQUES ET LINGUISTIQUES

JuriLex est un outil d'aide à la compréhension, et non un cabinet juridique automatisé.

L'application ne doit pas :
- Garantir qu'un contrat est légal ou illégal.
- Remplacer l'avis d'un professionnel compétent.
- Inventer des références juridiques.
- Présenter une interprétation incertaine comme une certitude.
- Promettre que toutes les clauses risquées seront détectées.
- Présenter une traduction automatique comme certifiée.

Les résultats doivent indiquer que l'explication peut comporter des erreurs et que les situations importantes ou ambiguës nécessitent une vérification auprès d'un professionnel.

Le modèle de traduction et le modèle de synthèse vocale doivent être soumis à un examen de licence avant tout déploiement commercial.

Les licences connues des modèles envisagés comportent des restrictions non commerciales :
- Adaptateur de traduction : CC BY-NC-SA 4.0, selon la fiche du modèle.
- MMS TTS : CC BY-NC 4.0, selon la fiche du modèle.

Il faut vérifier les versions exactes des modèles, les conditions des composants associés et les éventuelles autorisations nécessaires. Ne pas supposer qu'un modèle public est automatiquement autorisé pour une exploitation commerciale.

---

# 10. DOCUMENTATION ET LIVRABLES

Le dépôt final doit contenir au minimum :

- `README.md` : présentation, installation et lancement.
- `CAHIER_DES_CHARGES.md` : cahier des charges de référence.
- `AVANCEMENT.md` : état réel de l'implémentation.
- `.env.example` : variables nécessaires, sans secrets.
- `frontend/` : application React/PWA.
- `backend/` : application Python.
- Les tests frontend et backend.
- Les instructions de déploiement.
- Les procédures de chargement des modèles.
- Les résultats des tests de performance.
- Les limites connues.
- La documentation des endpoints.
- Une procédure de nettoyage des ressources temporaires.

Ne pas inclure les poids des modèles dans Git sans justification. Prévoir une procédure documentée de téléchargement et de vérification de leur présence.

Ne jamais commiter de clé API, de contrat réel ou de donnée personnelle.

---

# 11. ORDRE DE DÉVELOPPEMENT

Le projet doit être réalisé par étapes contrôlables.

### Phase 0 — Faisabilité
- Examiner les licences et les dépendances.
- Évaluer la faisabilité de NLLB adapté à l'éwé.
- Évaluer MMS TTS.
- Tester les besoins mémoire.
- Étudier les options d'hébergement.
- Documenter les risques et décisions.

### Phase 1 — Structure
- Créer les dossiers frontend et backend.
- Installer les dépendances minimales.
- Mettre en place la configuration.
- Créer les tests de base.
- Documenter le lancement local.

### Phase 2 — Interface
- Réaliser les écrans principaux.
- Mettre en place le design mobile-first.
- Gérer les états de chargement et d'erreur.
- Vérifier l'accessibilité.

### Phase 3 — Documents
- Implémenter l'importation.
- Implémenter l'extraction et l'OCR.
- Ajouter la prévisualisation.
- Ajouter la correction du texte.
- Ajouter le nettoyage.

### Phase 4 — Explication IA
- Intégrer Gemini côté backend.
- Imposer le consentement.
- Structurer les réponses.
- Tester les erreurs et les injections de prompt.

### Phase 5 — Traduction locale
- Installer et charger le modèle.
- Vérifier le modèle de base et l'adaptateur.
- Tester les traductions.
- Mesurer les performances.

### Phase 6 — Synthèse vocale locale
- Installer et charger MMS TTS.
- Générer un véritable fichier audio.
- Intégrer la lecture dans le frontend.
- Mesurer les performances et tester les erreurs.

### Phase 7 — Sécurité et qualité
- Tester la confidentialité.
- Vérifier le nettoyage.
- Exécuter les tests automatisés.
- Effectuer des tests linguistiques et utilisateurs.

### Phase 8 — Déploiement
- Choisir l'hébergement à partir des mesures.
- Configurer les secrets.
- Déployer frontend et backend.
- Vérifier le fonctionnement réel.
- Documenter les coûts et limites.

Ne pas passer à une phase suivante si une dépendance critique de la phase actuelle n'est pas comprise ou validée.

---

# 12. DÉCISIONS À VALIDER AVANT LA PRODUCTION

Les éléments suivants nécessitent une décision documentée :

1. Hébergement CPU ou service d'inférence distant.
2. Faisabilité des deux modèles sur un même serveur.
3. Budget mensuel maximal.
4. Limite de taille et de pages des documents.
5. Temps maximal accepté pour chaque opération.
6. Politique exacte de conservation des données chez les fournisseurs externes.
7. Licences et éventuelles autorisations commerciales.
8. Qualité linguistique minimale acceptable.
9. Modalités de validation par des locuteurs éwé.
10. Procédure de suppression des ressources temporaires.

**Principe final : la priorité n'est pas d'avoir beaucoup de fonctionnalités, mais de fournir un parcours réellement utilisable, compréhensible, confidentiel et techniquement vérifié.**