import Button from '../components/Button.jsx'

export default function Finish({ onRestart }) {
  return (
    <div className="screen">
      <h1>Terminé</h1>
      <p className="lede">Votre document a été traité.</p>
      <p>Les fichiers temporaires ont été supprimés. JuriLex ne conserve pas d'historique de vos documents.</p>
      <div className="actions">
        <Button onClick={onRestart}>Analyser un autre document</Button>
      </div>
    </div>
  )
}
