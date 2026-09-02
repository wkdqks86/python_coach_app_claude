import { useState } from 'react'
import type { FormEvent } from 'react'
import { createProfile, resumeProfile, setNickname } from '../api'
import LoadingOverlay from './LoadingOverlay'

interface Props {
  onReady: (nickname: string) => void
}

export default function NicknameGate({ onReady }: Props) {
  const [mode, setMode] = useState<'new' | 'resume'>('new')
  const [value, setValue] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  function switchMode(next: 'new' | 'resume') {
    setMode(next)
    setError('')
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    const trimmed = value.trim()
    if (!trimmed) {
      setError('닉네임을 입력해주세요.')
      return
    }
    setBusy(true)
    setError('')
    try {
      const result = await (mode === 'new' ? createProfile(trimmed) : resumeProfile(trimmed))
      setNickname(result.nickname)
      onReady(result.nickname)
    } catch (err) {
      setError(err instanceof Error ? err.message : '문제가 발생했어요. 다시 시도해주세요.')
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="nickname-gate">
      {busy && (
        <LoadingOverlay message="서버 연결 중... 처음 접속이면 최대 1분 정도 걸릴 수 있어요." />
      )}
      <div className="nickname-gate-card">
        <h1>PyCoach</h1>
        <p className="nickname-gate-intro">닉네임으로 나만의 학습 진도를 저장해요.</p>

        <div className="nickname-gate-tabs">
          <button
            type="button"
            className={mode === 'new' ? 'active' : ''}
            onClick={() => switchMode('new')}
          >
            처음 시작하기
          </button>
          <button
            type="button"
            className={mode === 'resume' ? 'active' : ''}
            onClick={() => switchMode('resume')}
          >
            이어서 하기
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <input
            className="nickname-gate-input"
            value={value}
            onChange={(e) => setValue(e.target.value)}
            placeholder="닉네임 (공백 없이, 최대 20자)"
            maxLength={20}
            autoCapitalize="off"
            autoCorrect="off"
            autoComplete="off"
          />
          <button type="submit" className="primary nickname-gate-submit" disabled={busy}>
            {mode === 'new' ? '시작하기' : '이어서 하기'}
          </button>
        </form>

        {error && <p className="nickname-gate-error">{error}</p>}

        <p className="nickname-gate-hint">
          {mode === 'new'
            ? '이미 있는 닉네임은 사용할 수 없어요.'
            : '전에 쓰던 닉네임을 그대로 입력하면 진도를 이어갈 수 있어요.'}
        </p>
      </div>
    </div>
  )
}
