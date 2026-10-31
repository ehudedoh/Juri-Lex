import { STEPS } from '../steps.js'

export default function StepIndicator({ current }) {
  const index = STEPS.findIndex((s) => s.id === current)
  const step = STEPS[index] || STEPS[0]
  const pct = Math.round(((index + 1) / STEPS.length) * 100)

  return (
    <nav className="stepper" aria-label="Progression du parcours">
      <div
        className="stepper__bar"
        role="progressbar"
        aria-valuenow={index + 1}
        aria-valuemin={1}
        aria-valuemax={STEPS.length}
        aria-label="Progression"
      >
        <span className="stepper__fill" style={{ width: `${pct}%` }} />
      </div>
      <p className="stepper__label">
        Étape {index + 1} sur {STEPS.length} — <strong>{step.label}</strong>
      </p>
    </nav>
  )
}
