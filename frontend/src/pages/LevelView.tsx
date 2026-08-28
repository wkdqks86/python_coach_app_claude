import { useEffect, useState } from 'react'
import { getLevel } from '../api'
import ProblemPanel from '../components/ProblemPanel'
import type { Level } from '../types'

interface Props {
  levelId: number
  onExit: () => void
}

type Stage = 'loading' | 'concepts' | 'problems' | 'done'

export default function LevelView({ levelId, onExit }: Props) {
  const [level, setLevel] = useState<Level | null>(null)
  const [stage, setStage] = useState<Stage>('loading')
  const [problemIndex, setProblemIndex] = useState(0)

  useEffect(() => {
    getLevel(levelId).then((data) => {
      setLevel(data)
      setStage('concepts')
    })
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
        <button type="button" className="primary start-practice-btn" onClick={() => setStage('problems')}>
          실습 시작하기
        </button>
      </div>
    )
  }

  if (stage === 'problems') {
    const problem = level.problems[problemIndex]
    return (
      <ProblemPanel
        key={problem.id}
        problem={problem}
        index={problemIndex}
        total={level.problems.length}
        onSolved={() => {
          if (problemIndex + 1 < level.problems.length) {
            setProblemIndex((i) => i + 1)
          } else {
            setStage('done')
          }
        }}
      />
    )
  }

  return (
    <div>
      <h2>레벨 {level.id} 완료!</h2>
      <p>{level.title}의 문제 {level.problems.length}개를 모두 풀었습니다.</p>
      <button type="button" className="primary" onClick={onExit}>
        오늘의 학습으로 돌아가기
      </button>
    </div>
  )
}
