import { render, screen, fireEvent } from '@testing-library/react'
import App from './App.jsx'

test("affiche l'écran d'accueil", () => {
  render(<App />)
  expect(screen.getByRole('heading', { level: 1, name: 'JuriLex' })).toBeInTheDocument()
  expect(screen.getByText('Comprendre avant de signer.')).toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'Comprendre un document' })).toBeInTheDocument()
})

test("navigue vers l'importation", () => {
  render(<App />)
  fireEvent.click(screen.getByRole('button', { name: 'Comprendre un document' }))
  expect(screen.getByRole('heading', { name: 'Importez votre document' })).toBeInTheDocument()
})
