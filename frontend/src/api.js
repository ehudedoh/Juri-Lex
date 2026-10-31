// Client HTTP vers le backend JuriLex.
// En développement, le proxy Vite redirige `/api` vers http://localhost:8000.

const API_BASE = '/api'

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

// Envoie les fichiers sélectionnés pour extraction du texte.
export function extractDocument(files) {
  const form = new FormData()
  files.forEach(({ file }) => form.append('files', file, file.name))
  return request('/documents/extract', { method: 'POST', body: form })
}
