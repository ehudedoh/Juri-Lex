import Button from '../components/Button.jsx'

export default function Ewe({ french, translation, audio, busy, onTranslate, onSpeak, onBack, onFinish }) {
  return (
    <div className="screen">
      <h1>Éwé & audio</h1>

      <section className="lang-block">
        <h2>Français</h2>
        <p>{french}</p>
      </section>

      <section className="lang-block">
        <h2>Éwé</h2>
        {translation ? (
          <>
            <p>{translation}</p>
            <p className="notice">Traduction automatique — elle n'est pas certifiée.</p>
          </>
        ) : (
          <>
            <p className="muted">Traduction non encore générée.</p>
            <Button onClick={onTranslate} disabled={busy}>
              {busy ? 'Traduction en cours…' : 'Traduire en éwé'}
            </Button>
          </>
        )}
      </section>

      <section className="lang-block">
        <h2>Écouter en éwé</h2>
        {audio ? (
          <div className="player" role="group" aria-label="Lecteur audio">
            <span className="player__label">
              {audio.label} · {audio.durationSec} s
            </span>
            <div className="player__controls">
              <Button disabled aria-label="Lecture indisponible en démonstration">
                ▶ Écouter
              </Button>
            </div>
            <p className="notice">
              La lecture audio sera disponible après intégration du modèle MMS TTS
              (démonstration).
            </p>
          </div>
        ) : (
          <Button onClick={onSpeak} disabled={busy || !translation}>
            {busy ? 'Génération en cours…' : "Générer l'audio"}
          </Button>
        )}
      </section>

      <div className="actions">
        <Button variant="secondary" onClick={onBack}>
          Retour
        </Button>
        <Button variant="ghost" onClick={onFinish}>
          Terminer
        </Button>
      </div>
    </div>
  )
}
