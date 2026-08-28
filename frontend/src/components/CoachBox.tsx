import { useState } from 'react'
import { askCoach } from '../api'

interface Props {
  problemId: string
  code: string
}

export default function CoachBox({ problemId, code }: Props) {
  const [open, setOpen] = useState(false)
  const [question, setQuestion] = useState('')
  const [reply, setReply] = useState<{ text: string; isFallback: boolean } | null>(null)
  const [asking, setAsking] = useState(false)

  async function handleAsk() {
    if (!question.trim()) return
    setAsking(true)
    try {
      const res = await askCoach(problemId, code, question)
      setReply({ text: res.reply, isFallback: res.source === 'fallback' })
    } finally {
      setAsking(false)
    }
  }

  if (!open) {
    return (
      <button type="button" className="coach-toggle" onClick={() => setOpen(true)}>
        AI 코치에게 질문하기
      </button>
    )
  }

  return (
    <div className="coach-box">
      <p className="coach-title">AI 코치</p>
      <textarea
        className="coach-input"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="어디서 막혔는지, 무엇이 궁금한지 적어보세요. (예: 왜 출력이 다르게 나올까요?)"
        rows={2}
      />
      <button type="button" className="primary" onClick={handleAsk} disabled={asking || !question.trim()}>
        {asking ? '생각하는 중...' : '질문하기'}
      </button>

      {reply && (
        <p className={reply.isFallback ? 'coach-reply fallback' : 'coach-reply'}>{reply.text}</p>
      )}
    </div>
  )
}
