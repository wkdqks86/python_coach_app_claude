import { useEffect, useState } from 'react'
import { getLevel, getReview } from '../api'
import ProblemPanel from '../components/ProblemPanel'
import type { Level, ReviewItem } from '../types'

export default function ReviewNote() {
  const [items, setItems] = useState<ReviewItem[] | null>(null)
  const [levels, setLevels] = useState<Record<number, Level>>({})
  const [retryingId, setRetryingId] = useState<string | null>(null)

  async function refresh() {
    const data = await getReview()
    setItems(data)

    const missingLevelIds = [...new Set(data.map((item) => item.level_id))].filter(
      (id) => !(id in levels),
    )
    if (missingLevelIds.length > 0) {
      const fetched = await Promise.all(missingLevelIds.map((id) => getLevel(id)))
      setLevels((prev) => {
        const next = { ...prev }
        fetched.forEach((level) => {
          next[level.id] = level
        })
        return next
      })
    }
  }

  useEffect(() => {
    refresh()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  if (items === null) {
    return <p className="status">불러오는 중...</p>
  }

  if (items.length === 0) {
    return (
      <div>
        <h1>오답노트</h1>
        <p className="muted">아직 틀린 문제가 없어요. 실습을 계속 진행해보세요!</p>
      </div>
    )
  }

  return (
    <div>
      <h1>오답노트</h1>
      <p className="muted">틀렸던 문제만 모아뒀어요. 정답을 바로 보여주지 않으니, 힌트를 다시 활용해보세요.</p>

      {items.map((item) => {
        const level = levels[item.level_id]
        const problem = level?.problems.find((p) => p.id === item.problem_id)
        const isRetrying = retryingId === item.problem_id

        return (
          <div key={item.problem_id} className="review-card">
            <div className="review-header">
              <span className={item.resolved ? 'badge resolved' : 'badge pending'}>
                {item.resolved ? '해결됨' : '복습 필요'}
              </span>
              <span className="muted">오답 {item.fail_count}회 · 총 시도 {item.attempt_count}회</span>
            </div>

            {problem ? (
              <p className="prompt">{problem.prompt}</p>
            ) : (
              <p className="muted">문제 정보를 불러오는 중...</p>
            )}

            {!isRetrying && (
              <>
                <pre className="output">{item.last_code}</pre>
                {problem && (
                  <button type="button" className="primary" onClick={() => setRetryingId(item.problem_id)}>
                    다시 풀기
                  </button>
                )}
              </>
            )}

            {isRetrying && problem && (
              <ProblemPanel
                problem={problem}
                initialCode={item.last_code}
                solvedLabel="완료"
                onSolved={() => {
                  setRetryingId(null)
                  refresh()
                }}
              />
            )}
          </div>
        )
      })}
    </div>
  )
}
