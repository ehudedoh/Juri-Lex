import { useEffect, useRef, useState } from 'react'
import Button from '../components/Button.jsx'

function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} o`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} Ko`
  return `${(bytes / (1024 * 1024)).toFixed(1)} Mo`
}

function extensionOf(name) {
  const i = name.lastIndexOf('.')
  return i >= 0 ? name.slice(i + 1).toUpperCase() : 'DOC'
}

function ImageThumb({ file }) {
  const [url, setUrl] = useState(null)
  useEffect(() => {
    const u = URL.createObjectURL(file)
    setUrl(u)
    return () => URL.revokeObjectURL(u)
  }, [file])

  if (!url) return <div className="page__thumb page__thumb--doc">…</div>
  return <img className="page__thumb" src={url} alt="" />
}

export default function Preview({ files, error, busy, onMove, onRemove, onReplace, onExtract, onBack }) {
  const replaceRefs = useRef({})

  const handleReplace = (id) => (e) => {
    const f = e.target.files?.[0]
    if (f) onReplace(id, f)
    e.target.value = ''
  }

  return (
    <div className="screen">
      <h1>Vérifiez vos pages</h1>
      <p className="lede">Supprimez, remplacez ou réorganisez les pages avant l'extraction.</p>

      {error && (
        <div className="alert alert--error">
          <p>{error}</p>
        </div>
      )}

      <ul className="pages">
        {files.map((item, i) => (
          <li className="page" key={item.id}>
            {item.file.type.startsWith('image/') ? (
              <ImageThumb file={item.file} />
            ) : (
              <div className="page__thumb page__thumb--doc" aria-hidden="true">
                {extensionOf(item.file.name)}
              </div>
            )}
            <div className="page__info">
              <span className="page__name">{item.file.name}</span>
              <span className="page__size">{formatSize(item.file.size)}</span>
            </div>
            <div className="page__controls">
              <button type="button" className="icon-btn" onClick={() => onMove(i, -1)} disabled={i === 0} aria-label="Monter cette page">↑</button>
              <button type="button" className="icon-btn" onClick={() => onMove(i, 1)} disabled={i === files.length - 1} aria-label="Descendre cette page">↓</button>
              <button type="button" className="icon-btn" onClick={() => onRemove(i)} aria-label="Supprimer cette page">✕</button>
              <button type="button" className="link-btn" onClick={() => replaceRefs.current[item.id]?.click()}>
                Remplacer
              </button>
              <input
                ref={(el) => (replaceRefs.current[item.id] = el)}
                type="file"
                accept=".pdf,.docx,.doc,image/*"
                className="visually-hidden"
                onChange={handleReplace(item.id)}
              />
            </div>
          </li>
        ))}
      </ul>

      {files.length === 0 && (
        <p className="alert alert--info">Aucune page. Revenez à l'importation pour ajouter un document.</p>
      )}

      <div className="actions">
        <Button variant="secondary" onClick={onBack}>
          Retour
        </Button>
        <Button onClick={onExtract} disabled={files.length === 0 || busy}>
          {busy ? 'Extraction en cours…' : 'Extraire le texte'}
        </Button>
      </div>
    </div>
  )
}
