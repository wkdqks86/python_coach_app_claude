"""레벨 콘텐츠(level_N.json) 생성 스크립트.

문제마다 손으로 예상 출력을 계산해서 적으면 실수하기 쉽다. 대신 각 문제에
"참조 코드"(reference_code)를 함께 적어두고, 이 스크립트가 실제로 그 코드를
실행해서 나온 결과를 expected_stdout으로 채워 넣는다. 콘셉트 카드의
example_output도 같은 방식으로 검증한다.

실제 레벨 데이터는 content_data/ 아래 phase별 파일에 있다 (파일 하나가
너무 커지는 것을 피하기 위해 나눴다):
    content_data/phase1_fundamentals.py   레벨 1~16  (파이썬 기초)
    content_data/phase2_data_analysis.py  레벨 17~23 (numpy/pandas)
    content_data/phase3_kaggle.py         레벨 24~28 (Kaggle 경진대회 준비)

사용법: backend 폴더에서 venv 파이썬으로 실행
    venv\\Scripts\\python.exe scripts\\generate_levels.py
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from content_data import phase1_fundamentals, phase2_data_analysis, phase3_kaggle  # noqa: E402

CONTENT_DIR = Path(__file__).parent.parent / "app" / "content"

LEVELS = [
    *phase1_fundamentals.LEVELS,
    *phase2_data_analysis.LEVELS,
    *phase3_kaggle.LEVELS,
]


def run(code: str, stdin: str = "") -> str:
    with tempfile.TemporaryDirectory(prefix="pycoach-gen-") as tmp_dir:
        proc = subprocess.run(
            [sys.executable, "-c", code],
            input=stdin,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=tmp_dir,
        )
    if proc.returncode != 0:
        raise RuntimeError(f"참조 코드 실행 실패:\n{code}\n---\n{proc.stderr}")
    return proc.stdout.rstrip("\n")


def build_level(level: dict) -> dict:
    concepts = []
    for c in level["concepts"]:
        stdin_for_example = c.pop("stdin_for_example", "")
        example_output = run(c["example_code"], stdin_for_example)
        concepts.append({**c, "example_output": example_output})

    problems = []
    for p in level["problems"]:
        stdin = p.get("stdin", "")
        expected_stdout = run(p["reference_code"], stdin)
        problem = {
            "id": p["id"],
            "concept_id": p["concept_id"],
            "prompt": p["prompt"],
            "starter_code": "",
            "expected_stdout": expected_stdout,
            "hints": p["hints"],
        }
        if stdin:
            problem["stdin"] = stdin
        if p.get("input_hint"):
            problem["input_hint"] = p["input_hint"]
        problems.append(problem)

    return {
        "id": level["id"],
        "title": level["title"],
        "goal": level["goal"],
        "concepts": concepts,
        "problems": problems,
    }


def main():
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)

    seen_level_ids = set()
    for level in LEVELS:
        if level["id"] in seen_level_ids:
            raise ValueError(f"중복된 레벨 id: {level['id']}")
        seen_level_ids.add(level["id"])

    # problem_id는 content_loader.py에서 레벨 전체를 통틀어 하나의 평평한
    # dict로 다뤄지므로, 레벨이 달라도 problem id가 겹치면 나중에 로드된
    # 레벨의 정답으로 조용히 덮어써져 채점이 엉뚱하게 통과/실패한다.
    # (실제로 레벨 1과 2가 둘 다 "p5-mini-self-intro"를 쓴 적이 있었다.)
    seen_problem_ids: dict[str, int] = {}
    for level in LEVELS:
        for p in level["problems"]:
            if p["id"] in seen_problem_ids:
                raise ValueError(
                    f"중복된 문제 id '{p['id']}': 레벨 {seen_problem_ids[p['id']]}와 "
                    f"레벨 {level['id']}에서 함께 사용됨. 문제 id는 전체 커리큘럼에서 유일해야 합니다."
                )
            seen_problem_ids[p["id"]] = level["id"]

    for level in LEVELS:
        data = build_level(level)
        out_path = CONTENT_DIR / f"level_{data['id']}.json"
        out_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"레벨 {data['id']} 생성 완료: {out_path} "
              f"(개념 {len(data['concepts'])}개, 문제 {len(data['problems'])}개)")


if __name__ == "__main__":
    main()
