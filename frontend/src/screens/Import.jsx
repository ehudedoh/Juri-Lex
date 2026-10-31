import { useRef } from 'react'
import Button from '../components/Button.jsx'

const MAX_SIZE_MB = 20
const MAX_PAGES = 20

export default function Import({ onFilesSelected, onBack }) {
  const fileRef = useRef(null)
  const cameraRef = useRef(null)

  const handleFiles = (list) => {
    if (!list || list.length === 0) return
    const files = Array.from(list).filter((f) => f && f.size > 0)
    if (files.length) onFilesSelected(files)
  }

  return (
    <div className="screen">
      <h1>Importez votre document</h1>
      <p className="lede">Choisissez un fichier ou prenez une photo.</p>

      <div className="dropzone">
        <input
          ref={fileRef}
          type="file"
          accept=".pdf,.docx,.doc,image/*"
          multiple
          className="visually-hidden"
          onChange={(e) => handleFiles(e.target.files)}
        />
        <input
          ref={cameraRef}
          type="file"
          accept="image/*"
          capture="environment"
          className="visually-hidden"
          onChange={(e) => handleFiles(e.target.files)}
        />
        <Button onClick={() => fileRef.current?.click()}>Choisir un fichier</Button>
        <Button variant="secondary" onClick={() => cameraRef.current?.click()}>
          Prendre une photo
        </Button>
      </div>

      <ul className="meta">
        <li>Formats : PDF, DOCX, images</li>
        <li>Taille max : {MAX_SIZE_MB} Mo</li>
        <li>Jusqu'à {MAX_PAGES} pages</li>
      </ul>

      <div className="actions">
        <Button variant="ghost" onClick={onBack}>
          Retour
        </Button>
      </div>
    </div>
  )
}
