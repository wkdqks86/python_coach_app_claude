import { useEffect, useState } from 'react'
import { getLevels, getProgress } from '../api'
import type { LevelProgress, LevelSummary } from '../types'

interface Props {
  onStart: (levelId: number) => void
}

export default function Home({ onStart }: Props) {
  const [levels, setLevels] = useState<LevelSummary[] | null>(null)
  const [progressByLevel, setProgressByLevel] = useState<Record<number, LevelProgress>>({})

  useEffect(() => {
    getLevels().then(setLevels)
    getProgress().then((summary) => {
      const map: Record<number, LevelProgress> = {}
      summary.levels.forEach((l) => {
        map[l.level_id] = l
      })
      setProgressByLevel(map)
    })
  }, [])

  if (levels === null) {
    return <p className="status">불러오는 중...</p>
  }

  const nextLevel = levels.find((level) => {
    const p = progressByLevel[level.id]
    return !p || p.solved_problems < p.total_problems
  })
  const allComplete = levels.length > 0 && !nextLevel

  return (
    <div>
      <h1>오늘의 학습</h1>

      {nextLevel && (
        <div className="continue-card">
          <p className="continue-label">이어서 학습하기</p>
          <h3>레벨 {nextLevel.id}. {nextLevel.title}</h3>
          <p className="muted">{nextLevel.goal}</p>
          <button type="button" className="primary" onClick={() => onStart(nextLevel.id)}>
            계속하기 →
          </button>
        </div>
      )}

      {allComplete && (
        <div className="continue-card">
          <p className="continue-label">🎉 모든 레벨 완료</p>
          <p className="muted">아래에서 원하는 레벨을 다시 풀어볼 수 있어요.</p>
        </div>
      )}

      <h2>전체 커리큘럼</h2>
      {levels.map((level) => {
        const p = progressByLevel[level.id]
        const done = p && p.solved_problems === p.total_problems && p.total_problems > 0
        return (
          <div key={level.id} className="level-card">
            <div className="level-card-header">
              <h3>레벨 {level.id}. {level.title}</h3>
              {p && (
                <span className={done ? 'badge resolved' : 'badge pending'}>
                  {done ? '완료' : `${p.solved_problems}/${p.total_problems}`}
                </span>
              )}
            </div>
            <p>{level.goal}</p>
            <p className="muted">
              개념 카드 {level.concept_count}개 · 문제 {level.problem_count}개
            </p>
            <button type="button" className="primary" onClick={() => onStart(level.id)}>
              {p && p.solved_problems > 0 ? '이어서 하기' : '시작하기'}
            </button>
          </div>
        )
      })}
    </div>
  )
}
