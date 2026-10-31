// Données simulées pour la Phase 2 (interface uniquement).
//
// IMPORTANT : aucune donnée personnelle réelle n'est utilisée ici.
// Ces valeurs seront remplacées par les appels réels au backend
// (extraction, Gemini, NLLB, MMS TTS) aux Phases 3 à 6.

export const MOCK_EXTRACTED_TEXT = `CONTRAT DE LOCATION D'HABITATION

Entre le bailleur et le locataire, il est convenu ce qui suit.

Article 1 — Objet. Le bailleur loue au locataire un logement situé dans la commune.

Article 2 — Durée. Le bail est conclu pour une durée de douze (12) mois, renouvelable.

Article 3 — Loyer. Le loyer mensuel est fixé à cent mille (100 000) francs CFA, payable au plus tard le 5 de chaque mois.

Article 4 — Dépôt de garantie. Le locataire verse un dépôt de garantie de deux (2) mois de loyer à la signature.

Article 5 — Obligations. Le locataire s'engage à occuper paisiblement les lieux et à les entretenir. Le bailleur s'engage à assurer la jouissance paisible du logement.

Article 6 — Résiliation. En cas de non-paiement du loyer pendant deux mois consécutifs, le bail peut être résilié de plein droit.`

export const MOCK_EXPLANATION = {
  document_nature: "Contrat de location d'habitation",
  objective:
    "Définir les conditions de location d'un logement entre un bailleur et un locataire.",
  summary:
    "Ce document est un contrat de location. Il fixe un loyer de 100 000 francs CFA par mois, payable avant le 5 de chaque mois, avec un dépôt de garantie de deux mois de loyer. Le bail dure douze mois et peut être résilié en cas de deux mois de loyer impayés.",
  obligations: [
    { text: "Le locataire doit occuper paisiblement les lieux et les entretenir.", source: 'document' },
    { text: "Le locataire doit payer le loyer avant le 5 de chaque mois.", source: 'document' },
    { text: "Le bailleur doit assurer la jouissance paisible du logement.", source: 'document' },
  ],
  rights: [
    { text: "Le locataire a droit à la jouissance paisible du logement.", source: 'ia' },
  ],
  amounts_payments: [
    { text: "Loyer mensuel : 100 000 francs CFA, payable au plus tard le 5 de chaque mois.", source: 'document' },
    { text: "Dépôt de garantie : deux (2) mois de loyer, soit 200 000 francs CFA, à la signature.", source: 'document' },
  ],
  dates_deadlines: [
    { text: "Durée du bail : douze (12) mois, renouvelable.", source: 'document' },
    { text: "Échéance de paiement du loyer : le 5 de chaque mois.", source: 'document' },
  ],
  conditions_exceptions: [
    { text: "Les conditions de renouvellement du bail ne sont pas détaillées.", source: 'incertain' },
  ],
  consequences: [
    { text: "Résiliation possible en cas de deux mois de loyer impayés consécutifs.", source: 'document' },
  ],
  ambiguities: [
    { text: "Les dates exactes de début et de fin du bail ne sont pas indiquées.", source: 'incertain' },
    { text: "Le logement n'est pas décrit avec précision (adresse, surface).", source: 'incertain' },
  ],
  questions: [
    { text: "Quelles sont les dates exactes de début et de fin du bail ?", source: 'ia' },
    { text: "Qui paie les charges (eau, électricité) ? Le contrat ne le précise pas.", source: 'ia' },
  ],
}

export const MOCK_TRANSLATION =
  "Traduction éwé de démonstration. Le texte réel sera produit par le modèle NLLB adapté à l'éwé (Phase 5)."

export const MOCK_AUDIO = {
  simulated: true,
  label: 'Audio éwé de démonstration',
  durationSec: 42,
}

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

export function simulateExtraction() {
  return wait(1200).then(() => MOCK_EXTRACTED_TEXT)
}

export function simulateAnalysis() {
  return wait(2000).then(() => MOCK_EXPLANATION)
}

export function simulateTranslation() {
  return wait(1500).then(() => MOCK_TRANSLATION)
}

export function simulateSpeech() {
  return wait(1500).then(() => MOCK_AUDIO)
}
