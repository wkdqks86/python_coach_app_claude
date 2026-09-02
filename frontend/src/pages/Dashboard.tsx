import { useEffect, useState } from 'react'
import { getProgress } from '../api'
import { PHASES } from '../phases'
import type { ProgressSummary } from '../types'

function pct(rate: number): string {
  return `${Math.round(rate * 100)}%`
}

export default function Dashboard() {
  const [summary, setSummary] = useState<ProgressSummary | null>(null)

  useEffect(() => {
    getProgress().then(setSummary)
  }, [])

  if (summary === null) {
    return <p className="status">불러오는 중...</p>
  }

  return (
    <div>
      <h1>진도율</h1>

      <div className="stat-row">
        <div className="stat-card">
          <p className="stat-value">{summary.total_solved} / {summary.total_problems}</p>
          <p className="stat-label">전체 문제 완료</p>
        </div>
        <div className="stat-card">
          <p className="stat-value">{summary.streak_days}일</p>
          <p className="stat-label">연속 학습일</p>
        </div>
        <div className="stat-card">
          <p className="stat-value">{pct(summary.success_rate)}</p>
          <p className="stat-label">제출 성공률 ({summary.passed_attempts}/{summary.total_attempts})</p>
        </div>
      </div>

      <h2>레벨별 진도</h2>
      {PHASES.map((phase) => {
        const phaseLevels = summary.levels.filter(
          (l) => l.level_id >= phase.minLevel && l.level_id <= phase.maxLevel,
        )
        if (phaseLevels.length === 0) return null

        const solved = phaseLevels.reduce((sum, l) => sum + l.solved_problems, 0)
        const total = phaseLevels.reduce((sum, l) => sum + l.total_problems, 0)

        return (
          <div key={phase.id} className="phase-progress-group">
            <div className="phase-progress-heading">
              <span className="phase-title">{phase.label}</span>
              <span className="muted">{solved} / {total}</span>
            </div>
            {phaseLevels.map((level) => (
              <div key={level.level_id} className="level-progress">
                <div className="level-progress-header">
                  <span>레벨 {level.level_id}. {level.title}</span>
                  <span className="muted">{level.solved_problems} / {level.total_problems}</span>
                </div>
                <div className="progress-bar">
                  <div
                    className="progress-bar-fill"
                    style={{ width: pct(level.completion_rate) }}
                  />
                </div>
              </div>
            ))}
          </div>
        )
      })}

      <h2>자주 막힌 개념</h2>
      {summary.weak_concepts.length === 0 ? (
        <p className="muted">아직 데이터가 부족해요. 문제를 더 풀어보면 여기에 표시됩니다.</p>
      ) : (
        <ul className="weak-concept-list">
          {summary.weak_concepts.map((concept) => (
            <li key={concept.concept_id}>
              <span>{concept.concept_title}</span>
              <span className="muted">오답 {concept.fail_count}회</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
