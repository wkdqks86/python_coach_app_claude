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

const NICKNAME_KEY = 'pycoach_nickname'

export function getNickname(): string | null {
  return localStorage.getItem(NICKNAME_KEY)
}

export function setNickname(nickname: string): void {
  localStorage.setItem(NICKNAME_KEY, nickname)
}

export function clearNickname(): void {
  localStorage.removeItem(NICKNAME_KEY)
}

/** Appends the active nickname as a query param — every endpoint that reads
 * or writes a learner's own data needs it to know whose data that is. */
function withNickname(path: string): string {
  const nickname = getNickname()
  if (!nickname) return path
  const sep = path.includes('?') ? '&' : '?'
  return `${path}${sep}nickname=${encodeURIComponent(nickname)}`
}

async function handle<T>(res: Response): Promise<T> {
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json() as Promise<T>
}

async function handleWithDetail<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const body = await res.json().catch(() => null)
    throw new Error(body?.detail || `HTTP ${res.status}`)
  }
  return res.json() as Promise<T>
}

export function createProfile(nickname: string): Promise<{ nickname: string }> {
  return fetch('/api/profile/new', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nickname }),
  }).then(handleWithDetail<{ nickname: string }>)
}

export function resumeProfile(nickname: string): Promise<{ nickname: string }> {
  return fetch('/api/profile/resume', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nickname }),
  }).then(handleWithDetail<{ nickname: string }>)
}

export function getLevels(): Promise<LevelSummary[]> {
  return fetch('/api/levels').then(handle<LevelSummary[]>)
}

export function getLevel(id: number): Promise<Level> {
  return fetch(`/api/levels/${id}`).then(handle<Level>)
}

export function runCode(
  code: string,
  stdin = '',
): Promise<{ stdout: string; stderr: string; timed_out: boolean }> {
  return fetch('/api/run', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code, stdin }),
  }).then(handle<{ stdout: string; stderr: string; timed_out: boolean }>)
}

export function submitCode(problemId: string, code: string): Promise<SubmitResult> {
  return fetch(withNickname('/api/submit'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ problem_id: problemId, code }),
  }).then(handle<SubmitResult>)
}

export function getReview(): Promise<ReviewItem[]> {
  return fetch(withNickname('/api/review')).then(handle<ReviewItem[]>)
}

export function getDueReviews(): Promise<DueReview[]> {
  return fetch(withNickname('/api/review/due')).then(handle<DueReview[]>)
}

export function getProgress(): Promise<ProgressSummary> {
  return fetch(withNickname('/api/progress')).then(handle<ProgressSummary>)
}

export function getSolvedProblemIds(): Promise<string[]> {
  return fetch(withNickname('/api/solved'))
    .then(handle<{ problem_ids: string[] }>)
    .then((res) => res.problem_ids)
}

export function getReport(): Promise<LearningReport> {
  return fetch(withNickname('/api/report')).then(handle<LearningReport>)
}

export function askCoach(problemId: string, code: string, question: string): Promise<CoachResponse> {
  return fetch('/api/coach', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ problem_id: problemId, code, question }),
  }).then(handle<CoachResponse>)
}
