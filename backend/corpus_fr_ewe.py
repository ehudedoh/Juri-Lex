"""Corpus synthétique français → éwé (≥ 30 phrases) pour les tests linguistiques.

Couvre les catégories prioritaires du §8.2 du cahier des charges : obligations,
interdictions, montants, dates, délais, conditions, exceptions, pénalités,
résiliation et ambiguïtés.

Aucune donnée personnelle réelle n'est utilisée.
"""

CORPUS = [
    # Obligations
    {"category": "obligation", "fr": "Vous devez payer le loyer avant le 5 de chaque mois."},
    {"category": "obligation", "fr": "Le locataire doit entretenir le logement."},
    {"category": "obligation", "fr": "Chaque partie doit respecter les clauses du contrat."},
    {"category": "obligation", "fr": "Le bailleur doit remettre un logement en bon état."},
    # Interdictions
    {"category": "interdiction", "fr": "Il est interdit de sous-louer le logement sans accord écrit."},
    {"category": "interdiction", "fr": "Le locataire ne doit pas modifier les lieux sans autorisation."},
    {"category": "interdiction", "fr": "Il est interdit de résilier le contrat avant son terme."},
    {"category": "interdiction", "fr": "Nul ne peut percevoir un loyer supérieur au montant convenu."},
    # Montants
    {"category": "montant", "fr": "Le loyer mensuel est de cent mille francs CFA."},
    {"category": "montant", "fr": "Le dépôt de garantie s'élève à deux mois de loyer."},
    {"category": "montant", "fr": "Une pénalité de dix mille francs CFA sera appliquée."},
    {"category": "montant", "fr": "Le montant total à payer est de cinq cent mille francs CFA."},
    # Dates
    {"category": "date", "fr": "Le contrat prend effet le premier janvier."},
    {"category": "date", "fr": "La réunion est prévue le quinze mars."},
    {"category": "date", "fr": "Le bail commence le premier jour du mois."},
    {"category": "date", "fr": "La date limite de paiement est le trente du mois."},
    # Délais
    {"category": "délai", "fr": "Le préavis est de trois mois."},
    {"category": "délai", "fr": "Le paiement doit intervenir sous trente jours."},
    {"category": "délai", "fr": "Le locataire dispose de quinze jours pour répondre."},
    {"category": "délai", "fr": "La durée du bail est de douze mois."},
    # Conditions
    {"category": "condition", "fr": "La location est accordée à condition de payer le dépôt de garantie."},
    {"category": "condition", "fr": "Le contrat est renouvelé si les deux parties sont d'accord."},
    {"category": "condition", "fr": "Le bail est valable sous réserve de signature."},
    {"category": "condition", "fr": "Le remboursement intervient si le logement est restitué en bon état."},
    # Exceptions
    {"category": "exception", "fr": "Le locataire peut résilier en cas de force majeure, sauf disposition contraire."},
    {"category": "exception", "fr": "Aucune pénalité n'est due, à l'exception des retards de paiement."},
    {"category": "exception", "fr": "Le bailleur ne peut entrer dans le logement, sauf urgence."},
    # Pénalités
    {"category": "pénalité", "fr": "Tout retard de paiement entraîne une pénalité de dix pour cent."},
    {"category": "pénalité", "fr": "Une amende de vingt mille francs CFA est prévue en cas de non-respect."},
    {"category": "pénalité", "fr": "Le défaut d'entretien engage la responsabilité du locataire."},
    # Résiliation
    {"category": "résiliation", "fr": "Le contrat peut être résilié en cas de non-paiement."},
    {"category": "résiliation", "fr": "La résiliation prend effet à la fin du préavis."},
    {"category": "résiliation", "fr": "Chaque partie peut mettre fin au contrat par écrit."},
    # Ambiguïtés
    {"category": "ambiguïté", "fr": "La durée exacte du bail n'est pas précisée."},
    {"category": "ambiguïté", "fr": "Le montant des charges n'est pas clairement indiqué."},
    {"category": "ambiguïté", "fr": "Les conditions de renouvellement restent à préciser."},
]
