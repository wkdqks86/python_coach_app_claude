import { useState } from 'react'
import './App.css'
import Home from './pages/Home'
import LevelView from './pages/LevelView'
import ReviewNote from './pages/ReviewNote'

type View = { name: 'home' } | { name: 'review' } | { name: 'level'; levelId: number }

function App() {
  const [view, setView] = useState<View>({ name: 'home' })

  return (
    <>
      <nav className="nav">
        <button
          type="button"
          className={view.name === 'home' ? 'nav-link active' : 'nav-link'}
          onClick={() => setView({ name: 'home' })}
        >
          오늘의 학습
        </button>
        <button
          type="button"
          className={view.name === 'review' ? 'nav-link active' : 'nav-link'}
          onClick={() => setView({ name: 'review' })}
        >
          오답노트
        </button>
      </nav>
      <main className="app">
        {view.name === 'home' && (
          <Home onStart={(levelId) => setView({ name: 'level', levelId })} />
        )}
        {view.name === 'review' && <ReviewNote />}
        {view.name === 'level' && (
          <LevelView levelId={view.levelId} onExit={() => setView({ name: 'home' })} />
        )}
      </main>
    </>
  )
}

export default App
