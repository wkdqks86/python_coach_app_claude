import { useEffect, useState } from 'react'
import { getDueReviews, getLevel, getSolvedProblemIds } from '../api'
import ProblemPanel from '../components/ProblemPanel'
import type { Level, Problem } from '../types'

interface Props {
  levelId: number
  onExit: () => void
}

type Stage = 'loading' | 'concepts' | 'problems' | 'done'

type QueueItem =
  | { kind: 'new'; problem: Problem; newIndex: number; newTotal: number }
  | { kind: 'review'; problem: Problem }

const MAX_INTERLEAVED_REVIEWS = 3

function shuffle<T>(items: T[]): T[] {
  const copy = [...items]
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[copy[i], copy[j]] = [copy[j], copy[i]]
  }
  return copy
}

// 복습 문제를 새 문제들 사이 무작위 위치에 끼워 넣는다 — 예고 없이 튀어나오는 게
// 목적이라 항상 맨 앞/맨 뒤가 아니라 매번 다른 자리에 섞여 들어가야 한다.
function buildQueue(newProblems: Problem[], reviewProblems: Problem[]): QueueItem[] {
  const queue: QueueItem[] = newProblems.map((problem, i) => ({
    kind: 'new',
    problem,
    newIndex: i,
    newTotal: newProblems.length,
  }))
  for (const problem of reviewProblems) {
    const at = Math.floor(Math.random() * (queue.length + 1))
    queue.splice(at, 0, { kind: 'review', problem })
  }
  return queue
}

export default function LevelView({ levelId, onExit }: Props) {
  const [level, setLevel] = useState<Level | null>(null)
  const [queue, setQueue] = useState<QueueItem[]>([])
  const [stage, setStage] = useState<Stage>('loading')
  const [queueIndex, setQueueIndex] = useState(0)
  const [resumeFrom, setResumeFrom] = useState<number | null>(null)

  useEffect(() => {
    let cancelled = false

    async function load() {
      const [data, solvedIds, dueReviews] = await Promise.all([
        getLevel(levelId),
        getSolvedProblemIds(),
        getDueReviews(),
      ])
      if (cancelled) return

      const solved = new Set(solvedIds)
      const firstUnsolved = data.problems.findIndex((p) => !solved.has(p.id))
      const startIndex = firstUnsolved === -1 ? 0 : firstUnsolved
      const newProblems = data.problems.slice(startIndex)

      const selectedReviews = shuffle(dueReviews).slice(0, MAX_INTERLEAVED_REVIEWS)
      const neededLevelIds = [...new Set(selectedReviews.map((r) => r.level_id))].filter(
        (id) => id !== levelId,
      )
      const otherLevels = await Promise.all(neededLevelIds.map((id) => getLevel(id)))
      if (cancelled) return

      const levelById = new Map<number, Level>([
        [levelId, data],
        ...otherLevels.map((l): [number, Level] => [l.id, l]),
      ])
      const reviewProblems = selectedReviews
        .map((r) => levelById.get(r.level_id)?.problems.find((p) => p.id === r.problem_id))
        .filter((p): p is Problem => Boolean(p))

      setLevel(data)
      setQueue(buildQueue(newProblems, reviewProblems))
      setResumeFrom(startIndex > 0 ? startIndex + 1 : null)
      setQueueIndex(0)
      setStage('concepts')
    }

    load()
    return () => {
      cancelled = true
    }
  }, [levelId])

  if (stage === 'loading' || !level) {
    return <p className="status">레벨을 불러오는 중...</p>
  }

  if (stage === 'concepts') {
    return (
      <div>
        <h2>{level.title}</h2>
        <p className="goal">목표: {level.goal}</p>
        {level.concepts.map((c, i) => (
          <div key={c.id} className="concept-card">
            <span className="concept-badge">{i + 1}</span>
            <div className="concept-body">
              <h3>{c.title}</h3>
              <p>{c.explanation}</p>
              <div className="concept-example">
                <code>{c.example_code}</code>
                <div className="concept-example-result">
                  <span className="arrow">→</span>
                  {c.example_output ? (
                    <code>{c.example_output}</code>
                  ) : (
                    <span className="muted">(화면 출력 없음)</span>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
        {resumeFrom !== null && (
          <p className="muted resume-note">이어서 학습하기: 문제 {resumeFrom}번부터 시작합니다.</p>
        )}
        <button
          type="button"
          className="primary start-practice-btn"
          onClick={() => setStage(queue.length > 0 ? 'problems' : 'done')}
        >
          {resumeFrom !== null ? '이어서 실습하기' : '실습 시작하기'}
        </button>
      </div>
    )
  }

  if (stage === 'problems') {
    const item = queue[queueIndex]
    const handleSolved = () => {
      if (queueIndex + 1 < queue.length) {
        setQueueIndex((i) => i + 1)
      } else {
        setStage('done')
      }
    }

    if (item.kind === 'review') {
      return (
        <ProblemPanel
          key={`review-${item.problem.id}`}
          problem={item.problem}
          badge="🔁 복습"
          solvedLabel="계속하기 →"
          onSolved={handleSolved}
        />
      )
    }
    return (
      <ProblemPanel
        key={item.problem.id}
        problem={item.problem}
        index={item.newIndex}
        total={item.newTotal}
        onSolved={handleSolved}
      />
    )
  }

  return (
    <div>
      <h2>레벨 {level.id} 완료!</h2>
      <p>{level.title} 학습을 모두 마쳤습니다.</p>
      <button type="button" className="primary" onClick={onExit}>
        오늘의 학습으로 돌아가기
      </button>
    </div>
  )
}
