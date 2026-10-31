import { useState } from 'react'
import { simulateTranslation, simulateSpeech } from './mock.js'
import { extractDocument, explainDocument } from './api.js'
import StepIndicator from './components/StepIndicator.jsx'
import Home from './screens/Home.jsx'
import Import from './screens/Import.jsx'
import Preview from './screens/Preview.jsx'
import VerifyText from './screens/VerifyText.jsx'
import Consent from './screens/Consent.jsx'
import Analyzing from './screens/Analyzing.jsx'
import Results from './screens/Results.jsx'
import Ewe from './screens/Ewe.jsx'
import Finish from './screens/Finish.jsx'

let idCounter = 0

const INITIAL_STATE = {
  step: 'home',
  files: [],
  extractedText: '',
  correctedText: '',
  textVersion: 0,
  consent: false,
  explanation: null,
  translation: null,
  audio: null,
  busy: false,
  error: null,
}

// Réinitialise tous les résultats qui dépendent du document/texte.
const resetResults = () => ({
  extractedText: '',
  correctedText: '',
  textVersion: 0,
  consent: false,
  explanation: null,
  translation: null,
  audio: null,
})

export default function App() {
  const [state, setState] = useState(INITIAL_STATE)

  const patch = (p) => setState((s) => ({ ...s, ...p }))

  const restart = () => setState(INITIAL_STATE)

  const addFiles = (files) => {
    const items = files.map((file) => ({ id: `f${++idCounter}`, file }))
    setState((s) => ({ ...s, ...resetResults(), files: [...s.files, ...items], step: 'preview', error: null }))
  }

  const move = (from, delta) =>
    setState((s) => {
      const to = from + delta
      if (to < 0 || to >= s.files.length) return s
      const files = [...s.files]
      const [it] = files.splice(from, 1)
      files.splice(to, 0, it)
      return { ...s, ...resetResults(), files }
    })

  const remove = (i) =>
    setState((s) => ({ ...s, ...resetResults(), files: s.files.filter((_, idx) => idx !== i) }))

  const replace = (id, file) =>
    setState((s) => ({
      ...s,
      ...resetResults(),
      files: s.files.map((it) => (it.id === id ? { ...it, file } : it)),
    }))

  const onExtract = async () => {
    patch({ busy: true, error: null })
    try {
      const result = await extractDocument(state.files)
      setState((s) => ({
        ...s,
        busy: false,
        extractedText: result.text,
        correctedText: result.text,
        textVersion: 1,
        step: 'verify',
      }))
    } catch (e) {
      patch({ busy: false, error: e.message || "L'extraction du texte a échoué. Veuillez réessayer." })
    }
  }

  const onTextChange = (value) =>
    setState((s) => ({
      ...s,
      correctedText: value,
      textVersion: s.textVersion + 1,
      explanation: null,
      translation: null,
      audio: null,
    }))

  const onAccept = async () => {
    setState((s) => ({ ...s, consent: true, busy: true, error: null, step: 'analyzing' }))
    try {
      const explanation = await explainDocument(state.correctedText, true)
      setState((s) => ({ ...s, busy: false, explanation, step: 'results' }))
    } catch (e) {
      setState((s) => ({
        ...s,
        busy: false,
        error: e.message || "L'analyse a échoué. Veuillez réessayer.",
        step: 'analyzing',
      }))
    }
  }

  const translate = async () => {
    patch({ busy: true, error: null })
    try {
      const translation = await simulateTranslation()
      setState((s) => ({ ...s, busy: false, translation }))
    } catch {
      patch({ busy: false, error: 'La traduction est momentanément indisponible.' })
    }
  }

  const speak = async () => {
    patch({ busy: true, error: null })
    try {
      const audio = await simulateSpeech()
      setState((s) => ({ ...s, busy: false, audio }))
    } catch {
      patch({ busy: false, error: "La génération audio a échoué. Veuillez réessayer." })
    }
  }

  const { step } = state

  return (
    <div className="app">
      <header className="app-header">
        <span className="brand">JuriLex</span>
        {step !== 'home' && <StepIndicator current={step} />}
      </header>

      <main className="app-main">
        {step === 'home' && <Home onStart={() => patch({ step: 'import' })} />}

        {step === 'import' && (
          <Import onFilesSelected={addFiles} onBack={() => patch({ step: 'home' })} />
        )}

        {step === 'preview' && (
          <Preview
            files={state.files}
            error={state.error}
            busy={state.busy}
            onMove={move}
            onRemove={remove}
            onReplace={replace}
            onExtract={onExtract}
            onBack={() => patch({ step: 'import' })}
          />
        )}

        {step === 'verify' && (
          <VerifyText
            value={state.correctedText}
            onChange={onTextChange}
            onConfirm={() => patch({ step: 'consent', error: null })}
            onBack={() => patch({ step: 'preview' })}
          />
        )}

        {step === 'consent' && (
          <Consent onAccept={onAccept} onCancel={() => patch({ step: 'verify' })} />
        )}

        {step === 'analyzing' && (
          <Analyzing
            error={state.error}
            onRetry={onAccept}
            onCancel={() => patch({ step: 'consent', busy: false, error: null })}
          />
        )}

        {step === 'results' && state.explanation && (
          <Results
            explanation={state.explanation}
            onTranslate={() => patch({ step: 'ewe', error: null })}
            onBack={() => patch({ step: 'consent' })}
          />
        )}

        {step === 'ewe' && (
          <Ewe
            french={state.explanation?.summary || ''}
            translation={state.translation}
            audio={state.audio}
            busy={state.busy}
            onTranslate={translate}
            onSpeak={speak}
            onBack={() => patch({ step: 'results', error: null })}
            onFinish={() => patch({ step: 'finish', error: null })}
          />
        )}

        {step === 'finish' && <Finish onRestart={restart} />}
      </main>

      <footer className="app-footer">
        <p>JuriLex — outil d'aide à la compréhension, pas un avis juridique.</p>
      </footer>
    </div>
  )
}
