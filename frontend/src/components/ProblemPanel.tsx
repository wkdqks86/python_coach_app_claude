import { useState } from 'react'
import { runCode, submitCode } from '../api'
import type { Problem, SubmitResult } from '../types'

interface Props {
  problem: Problem
  index?: number
  total?: number
  initialCode?: string
  solvedLabel?: string
  onSolved: () => void
}

export default function ProblemPanel({
  problem,
  index,
  total,
  initialCode,
  solvedLabel,
  onSolved,
}: Props) {
  const [code, setCode] = useState(initialCode ?? problem.starter_code)
  const [output, setOutput] = useState<{ stdout: string; stderr: string } | null>(null)
  const [result, setResult] = useState<SubmitResult | null>(null)
  const [hintsShown, setHintsShown] = useState(0)
  const [busy, setBusy] = useState(false)

  async function handleRun() {
    setBusy(true)
    try {
      const res = await runCode(code)
      setOutput(res)
      setResult(null)
    } finally {
      setBusy(false)
    }
  }

  async function handleSubmit() {
    setBusy(true)
    try {
      const res = await submitCode(problem.id, code)
      setResult(res)
      setOutput({ stdout: res.stdout, stderr: res.stderr })
    } finally {
      setBusy(false)
    }
  }

  const hasProgress = typeof index === 'number' && typeof total === 'number'

  return (
    <div className="panel">
      {hasProgress && (
        <p className="progress">문제 {index! + 1} / {total}</p>
      )}
      <p className="prompt">{problem.prompt}</p>

      <textarea
        className="code-editor"
        value={code}
        onChange={(e) => setCode(e.target.value)}
        spellCheck={false}
        rows={6}
      />

      <div className="button-row">
        <button type="button" onClick={handleRun} disabled={busy}>
          실행
        </button>
        <button type="button" onClick={handleSubmit} disabled={busy} className="primary">
          채점
        </button>
      </div>

      {output && (
        <pre className="output">
          {output.stdout || <span className="muted">(출력 없음)</span>}
          {output.stderr && <span className="stderr">{'\n' + output.stderr}</span>}
        </pre>
      )}

      {result && (
        <p className={result.passed ? 'feedback pass' : 'feedback fail'}>{result.feedback}</p>
      )}

      <div className="hints">
        {hintsShown < problem.hints.length && (
          <button type="button" className="hint-btn" onClick={() => setHintsShown((n) => n + 1)}>
            힌트 보기 ({hintsShown}/{problem.hints.length})
          </button>
        )}
        {problem.hints.slice(0, hintsShown).map((hint, i) => (
          <p key={i} className="hint">
            힌트 {i + 1}: {hint}
          </p>
        ))}
      </div>

      {result?.passed && (
        <button type="button" className="next-btn" onClick={onSolved}>
          {solvedLabel ?? (hasProgress && index! + 1 < total! ? '다음 문제 →' : '레벨 완료 →')}
        </button>
      )}
    </div>
  )
}
