export interface ConceptCard {
  id: string
  title: string
  explanation: string
  example_code: string
  example_output: string
}

export interface Problem {
  id: string
  concept_id: string
  prompt: string
  starter_code: string
  hints: string[]
  input_hint: string | null
}

export interface Level {
  id: number
  title: string
  goal: string
  concepts: ConceptCard[]
  problems: Problem[]
}

export interface LevelSummary {
  id: number
  title: string
  goal: string
  concept_count: number
  problem_count: number
}

export interface SubmitResult {
  passed: boolean
  stdout: string
  stderr: string
  expected_stdout: string
  feedback: string
}

export interface ReviewItem {
  problem_id: string
  level_id: number
  attempt_count: number
  fail_count: number
  resolved: boolean
  last_code: string
  last_attempt_at: string
}

export interface LevelProgress {
  level_id: number
  title: string
  total_problems: number
  solved_problems: number
  completion_rate: number
}

export interface WeakConcept {
  concept_id: string
  concept_title: string
  fail_count: number
}

export interface ProgressSummary {
  levels: LevelProgress[]
  total_problems: number
  total_solved: number
  overall_completion_rate: number
  total_attempts: number
  passed_attempts: number
  success_rate: number
  weak_concepts: WeakConcept[]
  streak_days: number
  active_days: number
}

export interface CoachResponse {
  reply: string
  source: 'ai' | 'fallback'
}

export interface DueReview {
  problem_id: string
  level_id: number
}

export interface LearningReport {
  period_start: string
  period_end: string
  period_length_days: number
  active_days: number
  problems_solved: number
  new_concepts: number
  total_attempts: number
  success_rate: number
  reviews_advanced: number
  reviews_graduated: number
  reviews_missed: number
  weak_concepts: WeakConcept[]
  streak_days: number
  highlight_message: string
}
