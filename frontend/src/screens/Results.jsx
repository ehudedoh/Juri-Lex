import Button from '../components/Button.jsx'

const SOURCE_LABELS = {
  document: 'Dans le document',
  ia: 'Explication',
  incertain: 'À vérifier',
}

function Section({ title, items }) {
  if (!items || items.length === 0) return null
  return (
    <section className="result-section">
      <h2>{title}</h2>
      <ul className="result-list">
        {items.map((it, i) => (
          <li key={i} className="result-item">
            <span className={`badge badge--${it.source}`}>{SOURCE_LABELS[it.source] || it.source}</span>
            {it.text}
          </li>
        ))}
      </ul>
    </section>
  )
}

export default function Results({ explanation, onTranslate, onBack }) {
  return (
    <div className="screen">
      <h1>Résultats</h1>
      <p className="lede">{explanation.document_nature}</p>

      <section className="result-section">
        <h2>Résumé général</h2>
        <p>{explanation.summary}</p>
      </section>

      <Section title="Obligations et responsabilités" items={explanation.obligations} />
      <Section title="Droits mentionnés" items={explanation.rights} />
      <Section title="Montants et paiements" items={explanation.amounts_payments} />
      <Section title="Dates et délais" items={explanation.dates_deadlines} />
      <Section title="Conditions et exceptions" items={explanation.conditions_exceptions} />
      <Section title="Conséquences" items={explanation.consequences} />
      <Section title="Points à vérifier" items={explanation.ambiguities} />
      <Section title="Questions à poser" items={explanation.questions} />

      <p className="notice">
        Cette explication peut contenir des erreurs. Pour une situation
        importante ou ambiguë, consultez un professionnel du droit.
      </p>

      <div className="actions">
        <Button variant="secondary" onClick={onBack}>
          Retour
        </Button>
        <Button onClick={onTranslate}>Traduire en éwé</Button>
      </div>
    </div>
  )
}
