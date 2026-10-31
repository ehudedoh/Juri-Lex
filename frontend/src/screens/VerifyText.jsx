import Button from '../components/Button.jsx'

export default function VerifyText({ value, onChange, onConfirm, onBack }) {
  return (
    <div className="screen">
      <h1>Vérifiez le texte reconnu</h1>
      <p className="lede">La reconnaissance peut contenir des erreurs. Corrigez le texte avant de continuer.</p>

      <div className="alert alert--info">
        Attention en particulier aux noms propres, montants, dates, numéros et tableaux.
      </div>

      <label className="field">
        <span className="field__label">Texte du document</span>
        <textarea
          className="textarea"
          rows={14}
          value={value}
          onChange={(e) => onChange(e.target.value)}
        />
      </label>

      <div className="actions">
        <Button variant="secondary" onClick={onBack}>
          Retour
        </Button>
        <Button onClick={onConfirm} disabled={!value.trim()}>
          Poursuivre
        </Button>
      </div>
    </div>
  )
}
