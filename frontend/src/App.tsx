import { useState } from 'react'
import './App.css'
import Home from './pages/Home'
import LevelView from './pages/LevelView'

function App() {
  const [activeLevel, setActiveLevel] = useState<number | null>(null)

  return (
    <main className="app">
      {activeLevel === null ? (
        <Home onStart={setActiveLevel} />
      ) : (
        <LevelView levelId={activeLevel} onExit={() => setActiveLevel(null)} />
      )}
    </main>
  )
}

export default App
