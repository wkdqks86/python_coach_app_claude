import { useEffect, useState } from 'react'
import { getReport } from '../api'
import type { LearningReport } from '../types'

function formatDate(iso: string): string {
  const [, month, day] = iso.split('-')
  return `${parseInt(month, 10)}월 ${parseInt(day, 10)}일`
}

function pct(rate: number): string {
  return `${Math.round(rate * 100)}%`
}

export default function Report() {
  const [report, setReport] = useState<LearningReport | null>(null)

  useEffect(() => {
    getReport().then(setReport)
  }, [])

  if (report === null) {
    return <p className="status">불러오는 중...</p>
  }

  const reviewsCompleted = report.reviews_advanced + report.reviews_graduated

  return (
    <div>
      <h1>주간 리포트</h1>
      <p className="muted">
        {formatDate(report.period_start)} ~ {formatDate(report.period_end)}
      </p>

      <div className="highlight-banner">{report.highlight_message}</div>

      <div className="stat-row">
        <div className="stat-card">
          <p className="stat-value">
            {report.active_days} / {report.period_length_days}
          </p>
          <p className="stat-label">학습한 날</p>
        </div>
        <div className="stat-card">
          <p className="stat-value">{report.problems_solved}</p>
          <p className="stat-label">새로 푼 문제</p>
        </div>
        <div className="stat-card">
          <p className="stat-value">{report.new_concepts}</p>
          <p className="stat-label">새로 배운 개념</p>
        </div>
      </div>

      <div className="stat-row">
        <div className="stat-card">
          <p className="stat-value">{reviewsCompleted}</p>
          <p className="stat-label">복습 완료 ({report.reviews_graduated}개 완전히 익힘)</p>
        </div>
        <div className="stat-card">
          <p className="stat-value">{pct(report.success_rate)}</p>
          <p className="stat-label">제출 성공률 ({report.total_attempts}회 시도)</p>
        </div>
        <div className="stat-card">
          <p className="stat-value">{report.streak_days}일</p>
          <p className="stat-label">현재 연속 학습일</p>
        </div>
      </div>

      <h2>이번 주 자주 막힌 개념</h2>
      {report.weak_concepts.length === 0 ? (
        <p className="muted">이번 주에는 눈에 띄게 막힌 개념이 없었어요.</p>
      ) : (
        <ul className="weak-concept-list">
          {report.weak_concepts.map((concept) => (
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
