import { useEffect, useState } from 'react'
import { getLevels } from '../api'
import type { LevelSummary } from '../types'

interface Props {
  onStart: (levelId: number) => void
}

export default function Home({ onStart }: Props) {
  const [levels, setLevels] = useState<LevelSummary[] | null>(null)

  useEffect(() => {
    getLevels().then(setLevels)
  }, [])

  return (
    <div>
      <h1>오늘의 학습</h1>
      {levels === null && <p className="status">불러오는 중...</p>}
      {levels?.map((level) => (
        <div key={level.id} className="level-card">
          <h3>레벨 {level.id}. {level.title}</h3>
          <p>{level.goal}</p>
          <p className="muted">
            개념 카드 {level.concept_count}개 · 문제 {level.problem_count}개
          </p>
          <button type="button" className="primary" onClick={() => onStart(level.id)}>
            시작하기
          </button>
        </div>
      ))}
    </div>
  )
}
