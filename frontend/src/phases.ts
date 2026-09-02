export interface Phase {
  id: number
  label: string
  goal: string
  minLevel: number
  maxLevel: number
}

export const PHASES: Phase[] = [
  { id: 1, label: 'Phase 1 · 파이썬 기초', goal: '변수부터 클래스·예외처리까지', minLevel: 1, maxLevel: 16 },
  { id: 2, label: 'Phase 2 · numpy & pandas', goal: '배열과 데이터프레임으로 데이터 다루기', minLevel: 17, maxLevel: 23 },
  { id: 3, label: 'Phase 3 · Kaggle 준비', goal: '실전 워크플로와 베이스라인 모델링', minLevel: 24, maxLevel: 28 },
]

export function phaseFor(levelId: number): Phase | undefined {
  return PHASES.find((p) => levelId >= p.minLevel && levelId <= p.maxLevel)
}
