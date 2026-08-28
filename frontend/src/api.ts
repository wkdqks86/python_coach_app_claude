import type {
  CoachResponse,
  DueReview,
  Level,
  LevelSummary,
  LearningReport,
  ProgressSummary,
  ReviewItem,
  SubmitResult,
} from './types'

async function handle<T>(res: Response): Promise<T> {
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json() as Promise<T>
}

export function getLevels(): Promise<LevelSummary[]> {
  return fetch('/api/levels').then(handle)
}

export function getLevel(id: number): Promise<Level> {
  return fetch(`/api/levels/${id}`).then(handle)
}

export function runCode(
  code: string,
  stdin = '',
): Promise<{ stdout: string; stderr: string; timed_out: boolean }> {
  return fetch('/api/run', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code, stdin }),
  }).then(handle)
}

export function submitCode(problemId: string, code: string): Promise<SubmitResult> {
  return fetch('/api/submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ problem_id: problemId, code }),
  }).then(handle)
}

export function getReview(): Promise<ReviewItem[]> {
  return fetch('/api/review').then(handle)
}

export function getDueReviews(): Promise<DueReview[]> {
  return fetch('/api/review/due').then(handle)
}

export function getProgress(): Promise<ProgressSummary> {
  return fetch('/api/progress').then(handle)
}

export function getSolvedProblemIds(): Promise<string[]> {
  return fetch('/api/solved')
    .then(handle<{ problem_ids: string[] }>)
    .then((res) => res.problem_ids)
}

export function getReport(): Promise<LearningReport> {
  return fetch('/api/report').then(handle)
}

export function askCoach(problemId: string, code: string, question: string): Promise<CoachResponse> {
  return fetch('/api/coach', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ problem_id: problemId, code, question }),
  }).then(handle)
}
