import Button from '../components/Button.jsx'

export default function Analyzing({ error, onRetry, onCancel }) {
  return (
    <div className="screen">
      <h1>Analyse en cours</h1>

      {error ? (
        <div className="alert alert--error">
          <p>{error}</p>
          <div className="actions">
            <Button variant="secondary" onClick={onCancel}>
              Annuler
            </Button>
            <Button onClick={onRetry}>Réessayer</Button>
          </div>
        </div>
      ) : (
        <>
          <div className="spinner" role="status" aria-live="polite" aria-label="Analyse en cours" />
          <ol className="progress">
            <li className="progress__item is-active">Extraction du texte</li>
            <li className="progress__item is-active">Analyse par l'intelligence artificielle</li>
            <li className="progress__item">Préparation de la traduction</li>
          </ol>
          <p className="muted">Cette opération peut prendre un moment.</p>
        </>
      )}
    </div>
  )
}
