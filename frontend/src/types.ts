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
