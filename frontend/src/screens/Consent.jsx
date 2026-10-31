import Button from '../components/Button.jsx'

export default function Consent({ onAccept, onCancel }) {
  return (
    <div className="screen">
      <h1>Avant l'analyse</h1>
      <p className="lede">Nous avons besoin de votre accord pour envoyer votre texte à un service d'intelligence artificielle.</p>

      <ul className="consent-list">
        <li>Le texte corrigé sera transmis au service d'IA pour produire l'explication.</li>
        <li>Le texte peut contenir des informations personnelles.</li>
        <li>JuriLex ne conserve pas votre document dans un historique.</li>
      </ul>

      <div className="actions">
        <Button variant="secondary" onClick={onCancel}>
          Annuler
        </Button>
        <Button onClick={onAccept}>J'accepte et je continue</Button>
      </div>
    </div>
  )
}
