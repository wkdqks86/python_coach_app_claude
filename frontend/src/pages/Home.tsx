import { useEffect, useMemo, useState } from 'react'
import { getLevels, getProgress } from '../api'
import type { LevelProgress, LevelSummary } from '../types'

interface Props {
  onStart: (levelId: number) => void
}

interface Phase {
  id: number
  label: string
  goal: string
  minLevel: number
  maxLevel: number
}

const PHASES: Phase[] = [
  { id: 1, label: 'Phase 1 · 파이썬 기초', goal: '변수부터 클래스·예외처리까지', minLevel: 1, maxLevel: 16 },
  { id: 2, label: 'Phase 2 · numpy & pandas', goal: '배열과 데이터프레임으로 데이터 다루기', minLevel: 17, maxLevel: 23 },
  { id: 3, label: 'Phase 3 · Kaggle 준비', goal: '실전 워크플로와 베이스라인 모델링', minLevel: 24, maxLevel: 28 },
]

function phaseFor(levelId: number): Phase | undefined {
  return PHASES.find((p) => levelId >= p.minLevel && levelId <= p.maxLevel)
}

export default function Home({ onStart }: Props) {
  const [levels, setLevels] = useState<LevelSummary[] | null>(null)
  const [progressByLevel, setProgressByLevel] = useState<Record<number, LevelProgress>>({})
  const [openPhaseId, setOpenPhaseId] = useState<number | null>(null)

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

  const nextLevel = useMemo(() => {
    if (!levels) return undefined
    return levels.find((level) => {
      const p = progressByLevel[level.id]
      return !p || p.solved_problems < p.total_problems
    })
  }, [levels, progressByLevel])

  // Default-open whichever phase the learner is currently in, once progress
  // has loaded — before that (or once every phase is done), start on Phase 1.
  useEffect(() => {
    if (openPhaseId !== null) return
    if (Object.keys(progressByLevel).length === 0) return
    const current = nextLevel ? phaseFor(nextLevel.id) : PHASES[0]
    setOpenPhaseId(current?.id ?? PHASES[0].id)
  }, [nextLevel, progressByLevel, openPhaseId])

  if (levels === null) {
    return <p className="status">불러오는 중...</p>
  }

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

      {PHASES.map((phase) => {
        const phaseLevels = levels.filter((l) => l.id >= phase.minLevel && l.id <= phase.maxLevel)
        if (phaseLevels.length === 0) return null

        const solved = phaseLevels.reduce((sum, l) => sum + (progressByLevel[l.id]?.solved_problems ?? 0), 0)
        const total = phaseLevels.reduce((sum, l) => sum + l.problem_count, 0)
        const phaseDone = total > 0 && solved === total
        const isOpen = openPhaseId === phase.id

        return (
          <div key={phase.id} className="phase-section">
            <button
              type="button"
              className="phase-header"
              onClick={() => setOpenPhaseId(isOpen ? null : phase.id)}
              aria-expanded={isOpen}
            >
              <span className="phase-header-text">
                <span className="phase-title">{phase.label}</span>
                <span className="muted">{phase.goal}</span>
              </span>
              <span className={phaseDone ? 'badge resolved' : 'badge pending'}>
                {phaseDone ? '완료' : `${solved}/${total}`}
              </span>
              <span className={isOpen ? 'phase-chevron open' : 'phase-chevron'} />
            </button>

            {isOpen && (
              <div className="phase-body">
                {phaseLevels.map((level) => {
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
            )}
          </div>
        )
      })}
    </div>
  )
}
