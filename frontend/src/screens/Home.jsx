import Button from '../components/Button.jsx'

export default function Home({ onStart }) {
  return (
    <div className="screen">
      <section className="hero">
        <h1 className="hero__title">JuriLex</h1>
        <p className="hero__signature">Comprendre avant de signer.</p>
        <p className="hero__intro">
          Importez un document, comprenez-le en français simple, puis écoutez son
          explication en éwé.
        </p>
        <Button className="hero__cta" onClick={onStart}>
          Comprendre un document
        </Button>
      </section>

      <section className="how">
        <h2>Comment ça marche ?</h2>
        <ol>
          <li>Importez ou photographiez votre document.</li>
          <li>Vérifiez le texte reconnu.</li>
          <li>Recevez une explication en français simple.</li>
          <li>Écoutez la traduction en éwé.</li>
        </ol>
      </section>

      <section className="limits">
        <h2>À savoir</h2>
        <ul>
          <li>Formats acceptés : PDF, DOCX, image (photo ou scan).</li>
          <li>L'explication est produite par une intelligence artificielle et peut contenir des erreurs.</li>
          <li>JuriLex ne conserve pas votre document dans un historique personnel.</li>
        </ul>
      </section>

      <section className="legal" id="confidentialite">
        <h2>Confidentialité</h2>
        <p>
          Votre document est traité de manière temporaire. JuriLex ne crée pas
          d'historique de vos documents ni de vos textes. Les données sont
          supprimées après le traitement.
        </p>
      </section>

      <section className="legal" id="conditions">
        <h2>Limites du service</h2>
        <p>
          JuriLex est un outil d'aide à la compréhension. Il ne remplace pas
          l'avis d'un professionnel du droit et ne fournit pas de traduction
          certifiée.
        </p>
      </section>
    </div>
  )
}
