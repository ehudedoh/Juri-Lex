// Client HTTP vers le backend JuriLex.
// - En développement, le proxy Vite redirige `/api` vers http://localhost:8000.
// - En production, définir VITE_API_URL (ex. https://backend.onrender.com/api)
//   lors du build pour pointer vers le backend déployé.

const API_BASE = import.meta.env.VITE_API_URL || '/api'

async function request(path, options) {
  const res = await fetch(`${API_BASE}${path}`, options)
  if (!res.ok) {
    let message = 'Une erreur est survenue.'
    try {
      const data = await res.json()
      if (data && data.detail) message = data.detail
    } catch {
      // réponse non JSON : conserver le message par défaut
    }
    throw new Error(message)
  }
  return res.json()
}

async function requestBlob(path, options) {
  const res = await fetch(`${API_BASE}${path}`, options)
  if (!res.ok) {
    let message = 'Une erreur est survenue.'
    try {
      const data = await res.json()
      if (data && data.detail) message = data.detail
    } catch {
      // réponse non JSON : conserver le message par défaut
    }
    throw new Error(message)
  }
  return res.blob()
}

// Envoie les fichiers sélectionnés pour extraction du texte.
export function extractDocument(files) {
  const form = new FormData()
  files.forEach(({ file }) => form.append('files', file, file.name))
  return request('/documents/extract', { method: 'POST', body: form })
}

// Demande l'explication du texte (avec consentement explicite).
export function explainDocument(text, consent) {
  return request('/explanations', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, consent }),
  })
}

// Traduit un texte français en éwé.
export function translateToEwe(text) {
  return request('/translations', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  })
}

// Génère l'audio éwé (renvoie un Blob audio/wav).
export function speakToEwe(text) {
  return requestBlob('/speech', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  })
}
