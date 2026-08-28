import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [message, setMessage] = useState('백엔드에 연결하는 중...')
  const [isError, setIsError] = useState(false)

  useEffect(() => {
    fetch('/api/hello')
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        return res.json()
      })
      .then((data: { message: string }) => setMessage(data.message))
      .catch(() => {
        setIsError(true)
        setMessage('백엔드 연결에 실패했습니다. FastAPI 서버가 실행 중인지 확인하세요.')
      })
  }, [])

  return (
    <main className="app">
      <h1>PyCoach</h1>
      <p className={isError ? 'status error' : 'status'}>{message}</p>
    </main>
  )
}

export default App
