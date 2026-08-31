import { useRef, useState } from 'react'
import type { KeyboardEvent } from 'react'
import { runCode, submitCode } from '../api'
import type { Problem, SubmitResult } from '../types'
import CoachBox from './CoachBox'

interface Props {
  problem: Problem
  index?: number
  total?: number
  initialCode?: string
  solvedLabel?: string
  badge?: string
  onSolved: () => void
}

export default function ProblemPanel({
  problem,
  index,
  total,
  initialCode,
  solvedLabel,
  badge,
  onSolved,
}: Props) {
  const [code, setCode] = useState(initialCode ?? problem.starter_code)
  const [stdin, setStdin] = useState('')
  const [output, setOutput] = useState<{ stdout: string; stderr: string } | null>(null)
  const [result, setResult] = useState<SubmitResult | null>(null)
  const [hintsShown, setHintsShown] = useState(0)
  const [busy, setBusy] = useState(false)
  const codeEditorRef = useRef<HTMLTextAreaElement>(null)

  async function handleRun() {
    setBusy(true)
    try {
      const res = await runCode(code, stdin)
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

  function insertIndent(target: HTMLTextAreaElement) {
    const start = target.selectionStart
    const end = target.selectionEnd
    setCode(code.slice(0, start) + '    ' + code.slice(end))
    requestAnimationFrame(() => {
      target.selectionStart = target.selectionEnd = start + 4
      target.focus()
    })
  }

  function handleCodeKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key !== 'Tab') return
    e.preventDefault()
    insertIndent(e.currentTarget)
  }

  function handleIndentButton() {
    if (codeEditorRef.current) insertIndent(codeEditorRef.current)
  }

  const hasProgress = typeof index === 'number' && typeof total === 'number'

  return (
    <div className="panel">
      {badge && <span className="badge review-badge">{badge}</span>}
      {hasProgress && (
        <>
          <div className="level-progress-track">
            <div
              className="level-progress-track-fill"
              style={{ width: `${((index! + 1) / total!) * 100}%` }}
            />
          </div>
          <p className="progress">문제 {index! + 1} / {total}</p>
        </>
      )}
      <p className="prompt">{problem.prompt}</p>

      <div className="code-toolbar">
        <button
          type="button"
          className="indent-btn"
          onPointerDown={(e) => {
            e.preventDefault()
            handleIndentButton()
          }}
        >
          ⇥ 들여쓰기
        </button>
      </div>
      <textarea
        ref={codeEditorRef}
        className="code-editor"
        value={code}
        onChange={(e) => setCode(e.target.value)}
        onKeyDown={handleCodeKeyDown}
        spellCheck={false}
        autoCapitalize="off"
        autoCorrect="off"
        autoComplete="off"
        rows={6}
      />

      {problem.input_hint && (
        <>
          <p className="stdin-hint">💡 {problem.input_hint}</p>
          <textarea
            className="stdin-editor"
            value={stdin}
            onChange={(e) => setStdin(e.target.value)}
            placeholder="input()에 전달할 값을 한 줄씩 입력 (실행 미리보기용)"
            spellCheck={false}
            autoCapitalize="off"
            autoCorrect="off"
            autoComplete="off"
            rows={2}
          />
        </>
      )}

      <div className="button-row">
        <button type="button" onClick={handleRun} disabled={busy}>
          실행
        </button>
        <button type="button" onClick={handleSubmit} disabled={busy} className="primary">
          채점
        </button>
      </div>

      {output && (
        <>
          <p className="output-label">출력</p>
          <pre className="output">
            {output.stdout || <span className="muted">(출력 없음)</span>}
            {output.stderr && <span className="stderr">{'\n' + output.stderr}</span>}
          </pre>
        </>
      )}

      {result && (
        <p className={result.passed ? 'feedback pass' : 'feedback fail'}>
          {result.passed ? '✓' : '!'} {result.feedback}
        </p>
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

      <CoachBox problemId={problem.id} code={code} />

      {result?.passed && (
        <button type="button" className="next-btn primary" onClick={onSolved}>
          {solvedLabel ?? (hasProgress && index! + 1 < total! ? '다음 문제 →' : '레벨 완료 →')}
        </button>
      )}
    </div>
  )
}
