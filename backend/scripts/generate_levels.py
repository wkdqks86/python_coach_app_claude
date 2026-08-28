"""레벨 콘텐츠(level_N.json) 생성 스크립트.

문제마다 손으로 예상 출력을 계산해서 적으면 실수하기 쉽다. 대신 각 문제에
"참조 코드"(reference_code)를 함께 적어두고, 이 스크립트가 실제로 그 코드를
실행해서 나온 결과를 expected_stdout으로 채워 넣는다. 콘셉트 카드의
example_output도 같은 방식으로 검증한다.

사용법: backend 폴더에서 venv 파이썬으로 실행
    venv\\Scripts\\python.exe scripts\\generate_levels.py
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

CONTENT_DIR = Path(__file__).parent.parent / "app" / "content"


def run(code: str, stdin: str = "") -> str:
    with tempfile.TemporaryDirectory(prefix="pycoach-gen-") as tmp_dir:
        proc = subprocess.run(
            [sys.executable, "-c", code],
            input=stdin,
            capture_output=True,
            text=True,
            timeout=10,
            cwd=tmp_dir,
        )
    if proc.returncode != 0:
        raise RuntimeError(f"참조 코드 실행 실패:\n{code}\n---\n{proc.stderr}")
    return proc.stdout.rstrip("\n")


LEVELS = [
    {
        "id": 2,
        "title": "변수와 입력",
        "goal": "값을 저장하고 사용자 입력 받기",
        "concepts": [
            {
                "id": "variables",
                "title": "변수에 값 저장하기",
                "explanation": "변수는 값을 담아두는 상자입니다. '이름 = 값' 형태로 값을 저장하고, 이름만 써서 다시 꺼내 쓸 수 있습니다.",
                "example_code": 'name = "파이코치"\nprint(name)',
            },
            {
                "id": "input-basics",
                "title": "input()으로 사용자 입력받기",
                "explanation": "input()은 사용자가 키보드로 입력한 내용을 문자열로 돌려줍니다. 보통 변수에 저장해서 사용합니다.",
                "example_code": 'name = input()\nprint(name)',
                "stdin_for_example": "홍길동\n",
            },
            {
                "id": "string-concat",
                "title": "문자열끼리 합치기 (+)",
                "explanation": "문자열은 + 연산자로 이어 붙일 수 있습니다. 변수와 고정된 문자열을 합쳐서 문장을 만들 때 자주 씁니다.",
                "example_code": 'name = "파이코치"\nprint("안녕하세요, " + name + "님!")',
            },
        ],
        "problems": [
            {
                "id": "p1-store-variable",
                "concept_id": "variables",
                "prompt": 'name이라는 변수에 "파이코치"를 저장하고, name을 출력하세요.',
                "reference_code": 'name = "파이코치"\nprint(name)',
                "hints": [
                    "변수는 '이름 = 값' 형태로 만듭니다.",
                    "name = \"파이코치\" 로 저장한 뒤, print(name)으로 변수를 출력하세요.",
                    'name = "파이코치"\nprint(name)',
                ],
            },
            {
                "id": "p2-echo-input",
                "concept_id": "input-basics",
                "prompt": "input()으로 이름을 입력받아, 입력받은 값을 그대로 출력하세요.",
                "reference_code": "name = input()\nprint(name)",
                "stdin": "파이코치\n",
                "input_hint": "아무 이름이나 입력해보세요. 예: 홍길동",
                "hints": [
                    "input()의 결과를 변수에 저장한 다음 그 변수를 출력해보세요.",
                    "name = input() 처럼 저장하고, print(name)으로 출력합니다.",
                    "name = input()\nprint(name)",
                ],
            },
            {
                "id": "p3-greeting",
                "concept_id": "string-concat",
                "prompt": 'input()으로 이름을 입력받아, "안녕하세요, OOO님!" 형태로 인사말을 출력하세요. (OOO 자리에 입력한 이름)',
                "reference_code": 'name = input()\nprint("안녕하세요, " + name + "님!")',
                "stdin": "파이코치\n",
                "input_hint": "이름을 입력해보세요. 예: 홍길동",
                "hints": [
                    "먼저 입력값을 변수에 저장하세요.",
                    "문자열 + 변수 + 문자열 형태로 이어 붙이면 문장을 만들 수 있습니다.",
                    'name = input()\nprint("안녕하세요, " + name + "님!")',
                ],
            },
            {
                "id": "p4-two-variables",
                "concept_id": "variables",
                "prompt": 'city 변수에 "서울", hobby 변수에 "코딩"을 저장하고, 아래처럼 두 줄로 출력하세요.\n사는 곳: 서울\n취미: 코딩',
                "reference_code": 'city = "서울"\nhobby = "코딩"\nprint("사는 곳: " + city)\nprint("취미: " + hobby)',
                "hints": [
                    "변수를 두 개 만들어야 합니다. city와 hobby 각각에 값을 저장하세요.",
                    "print(\"사는 곳: \" + city) 처럼 고정 문구와 변수를 합쳐서 출력하세요.",
                    'city = "서울"\nhobby = "코딩"\nprint("사는 곳: " + city)\nprint("취미: " + hobby)',
                ],
            },
            {
                "id": "p5-self-intro",
                "concept_id": "string-concat",
                "prompt": 'input()으로 이름과 나이를 순서대로 입력받아 "OOO님은 OO살입니다." 형식으로 출력하세요.',
                "reference_code": 'name = input()\nage = input()\nprint(name + "님은 " + age + "살입니다.")',
                "stdin": "파이코치\n5\n",
                "input_hint": "첫 줄에 이름, 둘째 줄에 나이를 입력해보세요. 예: 홍길동 / 10",
                "hints": [
                    "input()을 두 번 호출해서 이름과 나이를 각각 저장하세요.",
                    "age도 input()의 결과라 이미 문자열이라서 그대로 + 로 이어 붙일 수 있습니다.",
                    'name = input()\nage = input()\nprint(name + "님은 " + age + "살입니다.")',
                ],
            },
        ],
    },
    {
        "id": 3,
        "title": "자료형과 연산",
        "goal": "문자열·숫자·불리언과 계산 이해하기",
        "concepts": [
            {
                "id": "numbers",
                "title": "정수와 실수, 사칙연산",
                "explanation": "파이썬 숫자는 정수(int)와 실수(float)가 있습니다. +, -, *, / 로 계산할 수 있고, /는 항상 실수(float) 결과를 돌려줍니다.",
                "example_code": "print(3 + 5)",
            },
            {
                "id": "type-conversion",
                "title": "input()은 항상 문자열",
                "explanation": "input()으로 받은 값은 계산 없이 그냥 쓰면 숫자가 아니라 문자열입니다. 계산하려면 int()나 float()로 바꿔야 합니다.",
                "example_code": 'n = int(input())\nprint(n + 1)',
                "stdin_for_example": "10\n",
            },
            {
                "id": "booleans",
                "title": "불리언과 비교 연산자",
                "explanation": "==, >, < 같은 비교 연산자의 결과는 True 또는 False(불리언)입니다.",
                "example_code": "print(7 > 10)",
            },
        ],
        "problems": [
            {
                "id": "p1-add",
                "concept_id": "numbers",
                "prompt": "3과 5를 더한 결과를 출력하세요.",
                "reference_code": "print(3 + 5)",
                "hints": [
                    "print 안에 계산식을 그대로 넣을 수 있습니다.",
                    "print(3 + 5) 처럼 써보세요.",
                    "print(3 + 5)",
                ],
            },
            {
                "id": "p2-input-add",
                "concept_id": "type-conversion",
                "prompt": "input()으로 숫자 두 개를 한 줄씩 입력받아 더한 값을 출력하세요.",
                "reference_code": "a = int(input())\nb = int(input())\nprint(a + b)",
                "stdin": "3\n5\n",
                "input_hint": "숫자를 한 줄씩 입력해보세요. 예: 3 / 5",
                "hints": [
                    "input()의 결과는 문자열이라 바로 더하면 오류가 납니다.",
                    "int()로 감싸서 숫자로 바꾼 다음 변수에 저장하세요.",
                    "a = int(input())\nb = int(input())\nprint(a + b)",
                ],
            },
            {
                "id": "p3-division",
                "concept_id": "numbers",
                "prompt": "10을 2로 나눈 값을 출력하세요.",
                "reference_code": "print(10 / 2)",
                "hints": [
                    "나눗셈 연산자를 떠올려 보세요.",
                    "/ 연산자는 결과를 항상 실수(float)로 돌려줍니다.",
                    "print(10 / 2)",
                ],
            },
            {
                "id": "p4-comparison",
                "concept_id": "booleans",
                "prompt": "7이 10보다 큰지 비교한 결과를 출력하세요.",
                "reference_code": "print(7 > 10)",
                "hints": [
                    "비교 연산자를 사용하면 결과가 True/False로 나옵니다.",
                    "> 연산자로 두 숫자를 비교해보세요.",
                    "print(7 > 10)",
                ],
            },
            {
                "id": "p5-mini-calculator",
                "concept_id": "type-conversion",
                "prompt": "input()으로 숫자 두 개를 입력받아 합, 차, 곱을 아래 형식으로 출력하는 간단한 계산기를 만드세요.\n합: N\n차: N\n곱: N",
                "reference_code": 'a = int(input())\nb = int(input())\nprint("합:", a + b)\nprint("차:", a - b)\nprint("곱:", a * b)',
                "stdin": "4\n2\n",
                "input_hint": "숫자를 한 줄씩 입력해보세요. 예: 4 / 2",
                "hints": [
                    "먼저 두 입력값을 int()로 변환해서 변수에 저장하세요.",
                    "print(\"합:\", a + b) 처럼 콤마로 이어서 출력하면 자동으로 띄어쓰기가 들어갑니다.",
                    'a = int(input())\nb = int(input())\nprint("합:", a + b)\nprint("차:", a - b)\nprint("곱:", a * b)',
                ],
            },
        ],
    },
    {
        "id": 4,
        "title": "조건문 if",
        "goal": "상황에 따라 다른 동작 만들기",
        "concepts": [
            {
                "id": "if-basics",
                "title": "if문 기본 구조",
                "explanation": "if 조건: 다음 줄에 들여쓰기한 코드는 조건이 참(True)일 때만 실행됩니다.",
                "example_code": "if 10 > 5:\n    print(\"10은 5보다 큽니다\")",
            },
            {
                "id": "if-else",
                "title": "if / else",
                "explanation": "else는 if 조건이 거짓일 때 실행할 코드를 정합니다. 둘 중 하나는 반드시 실행됩니다.",
                "example_code": 'n = 3\nif n % 2 == 0:\n    print("짝수")\nelse:\n    print("홀수")',
            },
            {
                "id": "elif",
                "title": "elif로 여러 조건 비교하기",
                "explanation": "elif를 쓰면 조건을 여러 개 순서대로 검사할 수 있습니다. 위에서부터 참인 조건 하나만 실행됩니다.",
                "example_code": 'score = 85\nif score >= 90:\n    print("A")\nelif score >= 80:\n    print("B")\nelse:\n    print("C")',
            },
        ],
        "problems": [
            {
                "id": "p1-if-basic",
                "concept_id": "if-basics",
                "prompt": '숫자 10이 5보다 크면 "10은 5보다 큽니다"를 출력하는 코드를 작성하세요.',
                "reference_code": 'if 10 > 5:\n    print("10은 5보다 큽니다")',
                "hints": [
                    "if 조건: 다음 줄을 들여쓰기해서 실행할 코드를 씁니다.",
                    "if 10 > 5: 다음 줄에 print를 들여써서 넣어보세요.",
                    'if 10 > 5:\n    print("10은 5보다 큽니다")',
                ],
            },
            {
                "id": "p2-odd-even",
                "concept_id": "if-else",
                "prompt": 'input()으로 숫자를 하나 입력받아, 짝수면 "짝수입니다", 홀수면 "홀수입니다"를 출력하세요.',
                "reference_code": 'n = int(input())\nif n % 2 == 0:\n    print("짝수입니다")\nelse:\n    print("홀수입니다")',
                "stdin": "4\n",
                "input_hint": "숫자를 입력해보세요. 예: 4",
                "hints": [
                    "짝수인지는 % 2 == 0으로 확인할 수 있습니다 (나머지가 0이면 짝수).",
                    "if로 짝수 조건을 검사하고, else로 나머지 경우를 처리하세요.",
                    'n = int(input())\nif n % 2 == 0:\n    print("짝수입니다")\nelse:\n    print("홀수입니다")',
                ],
            },
            {
                "id": "p3-adult-check",
                "concept_id": "if-else",
                "prompt": 'input()으로 나이를 입력받아, 19살 이상이면 "성인입니다", 아니면 "미성년자입니다"를 출력하세요.',
                "reference_code": 'age = int(input())\nif age >= 19:\n    print("성인입니다")\nelse:\n    print("미성년자입니다")',
                "stdin": "20\n",
                "input_hint": "나이를 입력해보세요. 예: 20",
                "hints": [
                    "'19살 이상'은 >= 연산자로 표현합니다.",
                    "if age >= 19: 조건이 참이면 성인, else면 미성년자를 출력하세요.",
                    'age = int(input())\nif age >= 19:\n    print("성인입니다")\nelse:\n    print("미성년자입니다")',
                ],
            },
            {
                "id": "p4-grade",
                "concept_id": "elif",
                "prompt": 'input()으로 점수를 입력받아 90 이상이면 "A", 80 이상이면 "B", 그 외에는 "C"를 출력하세요.',
                "reference_code": 'score = int(input())\nif score >= 90:\n    print("A")\nelif score >= 80:\n    print("B")\nelse:\n    print("C")',
                "stdin": "85\n",
                "input_hint": "점수를 입력해보세요. 예: 85",
                "hints": [
                    "조건이 세 가지(90 이상 / 80 이상 / 그 외)이므로 elif가 필요합니다.",
                    "if score >= 90, elif score >= 80, else 순서로 검사하세요. 순서가 중요합니다.",
                    'score = int(input())\nif score >= 90:\n    print("A")\nelif score >= 80:\n    print("B")\nelse:\n    print("C")',
                ],
            },
            {
                "id": "p5-mini-adult-checker",
                "concept_id": "elif",
                "prompt": 'input()으로 이름과 나이를 순서대로 입력받아, "OOO님은 성인입니다." 또는 "OOO님은 미성년자입니다."를 출력하세요. (19살 기준)',
                "reference_code": 'name = input()\nage = int(input())\nif age >= 19:\n    print(name + "님은 성인입니다.")\nelse:\n    print(name + "님은 미성년자입니다.")',
                "stdin": "파이코치\n17\n",
                "input_hint": "첫 줄에 이름, 둘째 줄에 나이를 입력해보세요. 예: 홍길동 / 17",
                "hints": [
                    "이름과 나이, 두 번 input()을 받아야 합니다. 나이는 숫자로 변환하세요.",
                    "문자열 이어붙이기(+)와 if/else를 함께 사용해보세요.",
                    'name = input()\nage = int(input())\nif age >= 19:\n    print(name + "님은 성인입니다.")\nelse:\n    print(name + "님은 미성년자입니다.")',
                ],
            },
        ],
    },
    {
        "id": 5,
        "title": "반복문 for",
        "goal": "정해진 횟수 또는 목록 반복하기",
        "concepts": [
            {
                "id": "for-range",
                "title": "for와 range()로 n번 반복하기",
                "explanation": "range(n)은 0부터 n-1까지의 숫자를 만들어냅니다. for 변수 in range(n): 으로 n번 반복할 수 있습니다.",
                "example_code": 'for i in range(3):\n    print(i)',
            },
            {
                "id": "for-range-start-stop",
                "title": "range(시작, 끝)으로 범위 지정하기",
                "explanation": "range(시작, 끝)은 시작부터 끝-1까지 반복합니다. 끝 숫자는 포함되지 않는다는 점에 주의하세요.",
                "example_code": 'for i in range(1, 4):\n    print(i)',
            },
            {
                "id": "for-loop-variable",
                "title": "반복 변수를 계산에 활용하기",
                "explanation": "반복할 때마다 바뀌는 변수(i)를 계산식에 그대로 사용할 수 있습니다.",
                "example_code": 'for i in range(1, 4):\n    print(i * 2)',
            },
        ],
        "problems": [
            {
                "id": "p1-repeat-n-times",
                "concept_id": "for-range",
                "prompt": '"Hi"를 5번, 한 줄에 하나씩 출력하세요.',
                "reference_code": 'for _ in range(5):\n    print("Hi")',
                "hints": [
                    "range(5)는 0,1,2,3,4로 다섯 번 반복하게 해줍니다.",
                    "for _ in range(5): 다음 줄에 print(\"Hi\")를 들여써서 넣으세요.",
                    'for _ in range(5):\n    print("Hi")',
                ],
            },
            {
                "id": "p2-one-to-five",
                "concept_id": "for-range-start-stop",
                "prompt": "1부터 5까지 숫자를 한 줄씩 출력하세요.",
                "reference_code": "for i in range(1, 6):\n    print(i)",
                "hints": [
                    "1부터 5까지 포함하려면 range의 끝 숫자를 6으로 써야 합니다 (끝은 포함 안 됨).",
                    "for i in range(1, 6): 다음 줄에 print(i)를 넣으세요.",
                    "for i in range(1, 6):\n    print(i)",
                ],
            },
            {
                "id": "p3-double",
                "concept_id": "for-loop-variable",
                "prompt": "1부터 5까지 각 숫자의 두 배를 한 줄씩 출력하세요 (2, 4, 6, 8, 10).",
                "reference_code": "for i in range(1, 6):\n    print(i * 2)",
                "hints": [
                    "1부터 5까지 반복하면서, 반복 변수를 그대로 계산에 써보세요.",
                    "print(i * 2) 처럼 반복 변수 i에 2를 곱해서 출력하세요.",
                    "for i in range(1, 6):\n    print(i * 2)",
                ],
            },
            {
                "id": "p4-multiplication-table",
                "concept_id": "for-loop-variable",
                "prompt": 'input()으로 숫자(단)를 입력받아, 구구단 그 단을 1부터 9까지 "N x i = 결과" 형식으로 출력하세요.',
                "reference_code": 'n = int(input())\nfor i in range(1, 10):\n    print(n, "x", i, "=", n * i)',
                "stdin": "3\n",
                "input_hint": "몇 단을 볼지 입력해보세요. 예: 3",
                "hints": [
                    "1부터 9까지 반복하면서 매번 n * i를 계산하면 됩니다.",
                    "print(n, \"x\", i, \"=\", n * i) 처럼 콤마로 나열하면 자동으로 띄어쓰기가 들어갑니다.",
                    'n = int(input())\nfor i in range(1, 10):\n    print(n, "x", i, "=", n * i)',
                ],
            },
            {
                "id": "p5-mini-full-table",
                "concept_id": "for-range-start-stop",
                "prompt": "2단과 3단을 순서대로 이어서 출력하세요. 각 단은 1 x 1 = 1 형식으로 9줄씩, 총 18줄입니다.",
                "reference_code": 'for n in range(2, 4):\n    for i in range(1, 10):\n        print(n, "x", i, "=", n * i)',
                "hints": [
                    "for 안에 또 다른 for를 넣어서 '단'을 바꿔가며 반복할 수 있습니다 (반복문 중첩).",
                    "바깥쪽 for n in range(2, 4)로 2단과 3단을 돌고, 안쪽 for i in range(1, 10)으로 각 단을 출력하세요.",
                    'for n in range(2, 4):\n    for i in range(1, 10):\n        print(n, "x", i, "=", n * i)',
                ],
            },
        ],
    },
    {
        "id": 6,
        "title": "반복문 while",
        "goal": "조건이 유지되는 동안 반복하기",
        "concepts": [
            {
                "id": "while-basics",
                "title": "while 기본 구조",
                "explanation": "while 조건: 은 조건이 참인 동안 계속 반복합니다. for와 달리 몇 번 반복할지 미리 정해져 있지 않을 때 씁니다.",
                "example_code": 'count = 0\nwhile count < 3:\n    print(count)\n    count += 1',
            },
            {
                "id": "while-break",
                "title": "무한 루프와 break",
                "explanation": "while True: 는 조건 없이 계속 반복합니다. 원하는 순간 break를 만나면 반복문을 즉시 빠져나갑니다.",
                "example_code": 'i = 1\nwhile True:\n    print(i)\n    if i == 3:\n        break\n    i += 1',
            },
            {
                "id": "while-input",
                "title": "while과 input() 함께 쓰기",
                "explanation": "정답을 맞힐 때까지 반복해서 입력받는 것처럼, while 안에서 input()을 여러 번 호출할 수 있습니다.",
                "example_code": 'answer = 7\nguess = int(input())\nwhile guess != answer:\n    print("다시 시도하세요")\n    guess = int(input())\nprint("정답입니다!")',
                "stdin_for_example": "3\n7\n",
            },
        ],
        "problems": [
            {
                "id": "p1-while-count",
                "concept_id": "while-basics",
                "prompt": '0부터 4까지 "카운트: N" 형식으로 한 줄씩 출력하세요 (while 사용).',
                "reference_code": 'count = 0\nwhile count < 5:\n    print("카운트:", count)\n    count += 1',
                "hints": [
                    "count를 0에서 시작해서, count < 5인 동안 반복하면 됩니다.",
                    "반복할 때마다 출력하고 나서 count += 1로 값을 늘리는 걸 잊지 마세요.",
                    'count = 0\nwhile count < 5:\n    print("카운트:", count)\n    count += 1',
                ],
            },
            {
                "id": "p2-double-until-over-100",
                "concept_id": "while-basics",
                "prompt": "1부터 시작하는 변수에 2를 계속 곱해서, 100을 넘는 순간 멈추고 그 값을 출력하세요 (while 사용).",
                "reference_code": "n = 1\nwhile n <= 100:\n    n *= 2\nprint(n)",
                "hints": [
                    "n이 100 이하인 동안에는 계속 2를 곱하도록 while 조건을 만드세요.",
                    "반복문이 끝난 뒤에 n을 출력하면 됩니다 (반복 중에는 출력하지 않아도 돼요).",
                    "n = 1\nwhile n <= 100:\n    n *= 2\nprint(n)",
                ],
            },
            {
                "id": "p3-break-at-seven",
                "concept_id": "while-break",
                "prompt": "1부터 순서대로 늘어나는 숫자를 한 줄씩 출력하다가, 7을 출력한 뒤에 멈추세요 (1~7 출력).",
                "reference_code": "i = 1\nwhile True:\n    print(i)\n    if i == 7:\n        break\n    i += 1",
                "hints": [
                    "while True:로 무한히 반복하다가, 원하는 조건에서 break로 빠져나올 수 있습니다.",
                    "i를 출력한 다음 i가 7인지 검사해서 break하고, 아니면 i를 1 늘리세요.",
                    "i = 1\nwhile True:\n    print(i)\n    if i == 7:\n        break\n    i += 1",
                ],
            },
            {
                "id": "p4-guess-until-correct",
                "concept_id": "while-input",
                "prompt": '정답은 7입니다. input()으로 숫자를 반복해서 입력받아, 틀리면 "다시 시도하세요"를, 맞으면 "정답입니다!"를 출력하고 멈추세요.',
                "reference_code": 'answer = 7\nwhile True:\n    guess = int(input())\n    if guess == answer:\n        print("정답입니다!")\n        break\n    else:\n        print("다시 시도하세요")',
                "stdin": "3\n5\n7\n",
                "input_hint": "여러 줄에 걸쳐 숫자를 입력해보세요. 예: 3 / 5 / 7 (줄마다 하나씩)",
                "hints": [
                    "while True: 안에서 매번 input()을 새로 받아야 합니다.",
                    "입력값이 정답과 같으면 출력 후 break, 다르면 다시 시도 메시지를 출력하세요.",
                    'answer = 7\nwhile True:\n    guess = int(input())\n    if guess == answer:\n        print("정답입니다!")\n        break\n    else:\n        print("다시 시도하세요")',
                ],
            },
            {
                "id": "p5-mini-updown-game",
                "concept_id": "while-input",
                "prompt": '정답은 50입니다. input()으로 추측값을 반복 입력받아, 정답보다 작으면 "더 큰 숫자입니다", 크면 "더 작은 숫자입니다", 같으면 "정답입니다!"를 출력하고 멈추는 업다운 게임을 만드세요.',
                "reference_code": 'answer = 50\nwhile True:\n    guess = int(input())\n    if guess == answer:\n        print("정답입니다!")\n        break\n    elif guess < answer:\n        print("더 큰 숫자입니다")\n    else:\n        print("더 작은 숫자입니다")',
                "stdin": "30\n70\n50\n",
                "input_hint": "여러 줄에 걸쳐 숫자를 입력해보세요. 예: 30 / 70 / 50",
                "hints": [
                    "이전 문제에 조건을 하나 더 추가하는 것뿐입니다: 작을 때 / 클 때 / 같을 때.",
                    "elif로 '더 큰 숫자입니다'와 '더 작은 숫자입니다' 두 경우를 구분하세요.",
                    'answer = 50\nwhile True:\n    guess = int(input())\n    if guess == answer:\n        print("정답입니다!")\n        break\n    elif guess < answer:\n        print("더 큰 숫자입니다")\n    else:\n        print("더 작은 숫자입니다")',
                ],
            },
        ],
    },
    {
        "id": 7,
        "title": "리스트와 딕셔너리",
        "goal": "여러 값을 구조적으로 관리하기",
        "concepts": [
            {
                "id": "list-basics",
                "title": "리스트 만들고 값 꺼내기",
                "explanation": "리스트는 [ ] 안에 여러 값을 콤마로 나열해서 저장합니다. 순서(인덱스)는 0부터 시작합니다.",
                "example_code": 'fruits = ["사과", "바나나", "포도"]\nprint(fruits[1])',
            },
            {
                "id": "list-loop-append",
                "title": "리스트 전체 반복하기 / 추가하기",
                "explanation": "for 값 in 리스트: 로 모든 항목을 순서대로 꺼낼 수 있습니다. append()로 리스트 끝에 새 값을 추가할 수 있습니다.",
                "example_code": 'nums = [1, 2, 3]\nfor n in nums:\n    print(n)',
            },
            {
                "id": "dict-basics",
                "title": "딕셔너리 기본",
                "explanation": "딕셔너리는 {키: 값} 형태로 저장합니다. 순서가 아니라 키(key)로 값을 찾습니다.",
                "example_code": 'person = {"name": "파이코치", "age": 5}\nprint(person["name"])',
            },
        ],
        "problems": [
            {
                "id": "p1-list-index",
                "concept_id": "list-basics",
                "prompt": 'fruits 리스트에 "사과", "바나나", "포도"를 저장하고, 두 번째 항목을 출력하세요.',
                "reference_code": 'fruits = ["사과", "바나나", "포도"]\nprint(fruits[1])',
                "hints": [
                    "리스트의 순서(인덱스)는 0부터 시작합니다. 두 번째 항목의 인덱스는 몇일까요?",
                    "fruits[1]로 두 번째 항목에 접근할 수 있습니다.",
                    'fruits = ["사과", "바나나", "포도"]\nprint(fruits[1])',
                ],
            },
            {
                "id": "p2-list-loop",
                "concept_id": "list-loop-append",
                "prompt": "리스트 [1, 2, 3, 4, 5]의 모든 값을 한 줄씩 출력하세요.",
                "reference_code": "nums = [1, 2, 3, 4, 5]\nfor n in nums:\n    print(n)",
                "hints": [
                    "for 변수 in 리스트: 형태로 리스트의 모든 값을 순서대로 꺼낼 수 있습니다.",
                    "for n in nums: 다음 줄에 print(n)을 넣으세요.",
                    "nums = [1, 2, 3, 4, 5]\nfor n in nums:\n    print(n)",
                ],
            },
            {
                "id": "p3-list-append",
                "concept_id": "list-loop-append",
                "prompt": '빈 리스트 todo를 만들고 "숙제", "운동"을 순서대로 append로 추가한 뒤, 리스트 전체를 반복 출력하세요.',
                "reference_code": 'todo = []\ntodo.append("숙제")\ntodo.append("운동")\nfor t in todo:\n    print(t)',
                "hints": [
                    "todo = [] 로 빈 리스트를 만들고, append()로 값을 하나씩 추가할 수 있습니다.",
                    "추가가 끝나면 for로 todo 리스트를 순회하며 출력하세요.",
                    'todo = []\ntodo.append("숙제")\ntodo.append("운동")\nfor t in todo:\n    print(t)',
                ],
            },
            {
                "id": "p4-dict-lookup",
                "concept_id": "dict-basics",
                "prompt": 'person 딕셔너리에 "name": "파이코치", "age": 5 를 저장하고, "파이코치는 5살입니다" 형식으로 출력하세요.',
                "reference_code": 'person = {"name": "파이코치", "age": 5}\nprint(person["name"] + "는 " + str(person["age"]) + "살입니다")',
                "hints": [
                    "딕셔너리 값은 person[\"키\"] 형태로 꺼낼 수 있습니다.",
                    "age는 숫자라서 문자열과 이어붙이려면 str()로 문자열로 바꿔야 합니다.",
                    'person = {"name": "파이코치", "age": 5}\nprint(person["name"] + "는 " + str(person["age"]) + "살입니다")',
                ],
            },
            {
                "id": "p5-mini-todolist",
                "concept_id": "list-loop-append",
                "prompt": 'input()으로 할 일을 3개 입력받아 리스트에 저장한 뒤, "1. 할일" 형식으로 번호를 매겨 출력하세요.',
                "reference_code": 'todo = []\nfor i in range(3):\n    todo.append(input())\nfor i in range(len(todo)):\n    print(str(i + 1) + ". " + todo[i])',
                "stdin": "숙제\n운동\n독서\n",
                "input_hint": "할 일 3개를 한 줄씩 입력해보세요. 예: 숙제 / 운동 / 독서",
                "hints": [
                    "먼저 for와 range(3)으로 3번 input()을 받아 리스트에 append하세요.",
                    "번호를 매기려면 range(len(todo))로 인덱스를 돌면서 str(i+1)을 앞에 붙이세요.",
                    'todo = []\nfor i in range(3):\n    todo.append(input())\nfor i in range(len(todo)):\n    print(str(i + 1) + ". " + todo[i])',
                ],
            },
        ],
    },
    {
        "id": 8,
        "title": "함수 def",
        "goal": "반복되는 코드를 기능으로 묶기",
        "concepts": [
            {
                "id": "def-basics",
                "title": "함수 정의와 호출",
                "explanation": "def 이름(): 으로 함수를 만들고, 이름() 으로 호출해서 실행합니다. 같은 코드를 여러 번 쓰지 않아도 됩니다.",
                "example_code": 'def greet():\n    print("안녕하세요!")\n\ngreet()',
            },
            {
                "id": "def-params",
                "title": "매개변수로 값 전달하기",
                "explanation": "함수 이름 옆 괄호에 매개변수를 적으면, 호출할 때마다 다른 값을 넘겨서 다르게 동작시킬 수 있습니다.",
                "example_code": 'def welcome(name):\n    print(name + "님 환영합니다!")\n\nwelcome("파이코치")',
            },
            {
                "id": "def-return",
                "title": "return으로 값 돌려받기",
                "explanation": "return은 함수의 결과값을 호출한 곳으로 돌려줍니다. print와 달리 그 값을 변수에 저장해서 다시 쓸 수 있습니다.",
                "example_code": 'def add(a, b):\n    return a + b\n\nprint(add(3, 4))',
            },
        ],
        "problems": [
            {
                "id": "p1-simple-function",
                "concept_id": "def-basics",
                "prompt": '인사말을 출력하는 greet 함수를 만들고 호출해서 "안녕하세요!"를 출력하세요.',
                "reference_code": 'def greet():\n    print("안녕하세요!")\n\ngreet()',
                "hints": [
                    "def 함수이름(): 다음 줄에 들여쓰기로 실행할 코드를 씁니다.",
                    "함수를 만든 뒤에는 함수이름() 으로 직접 호출해야 실행됩니다.",
                    'def greet():\n    print("안녕하세요!")\n\ngreet()',
                ],
            },
            {
                "id": "p2-function-param",
                "concept_id": "def-params",
                "prompt": '이름을 매개변수로 받아 "OOO님 환영합니다!"를 출력하는 welcome(name) 함수를 만들고, welcome("파이코치")로 호출하세요.',
                "reference_code": 'def welcome(name):\n    print(name + "님 환영합니다!")\n\nwelcome("파이코치")',
                "hints": [
                    "함수 괄호 안에 매개변수 이름을 적으면 함수 안에서 그 값을 변수처럼 쓸 수 있습니다.",
                    "welcome(\"파이코치\")처럼 호출할 때 괄호 안에 실제 값을 넣습니다.",
                    'def welcome(name):\n    print(name + "님 환영합니다!")\n\nwelcome("파이코치")',
                ],
            },
            {
                "id": "p3-return-value",
                "concept_id": "def-return",
                "prompt": "두 수를 더해서 돌려주는 add(a, b) 함수를 만들고, add(3, 4)의 결과를 출력하세요.",
                "reference_code": "def add(a, b):\n    return a + b\n\nprint(add(3, 4))",
                "hints": [
                    "함수 안에서 print 대신 return을 쓰면 값을 함수 밖으로 돌려줄 수 있습니다.",
                    "add(3, 4)의 결과를 print()로 감싸서 출력하세요.",
                    "def add(a, b):\n    return a + b\n\nprint(add(3, 4))",
                ],
            },
            {
                "id": "p4-function-combine",
                "concept_id": "def-return",
                "prompt": "숫자를 제곱해서 돌려주는 square(n) 함수를 만들고, square(3)과 square(4)를 더한 값을 출력하세요.",
                "reference_code": "def square(n):\n    return n * n\n\nprint(square(3) + square(4))",
                "hints": [
                    "square(n)은 n * n을 return하면 됩니다.",
                    "return으로 받은 값끼리는 그대로 + 로 계산할 수 있습니다: square(3) + square(4)",
                    "def square(n):\n    return n * n\n\nprint(square(3) + square(4))",
                ],
            },
            {
                "id": "p5-mini-calculator-functions",
                "concept_id": "def-return",
                "prompt": 'add(a, b), subtract(a, b), multiply(a, b) 세 함수를 만들고, input()으로 숫자 두 개를 받아 각 함수의 결과를 "합: N", "차: N", "곱: N" 형식으로 출력하세요.',
                "reference_code": 'def add(a, b):\n    return a + b\n\ndef subtract(a, b):\n    return a - b\n\ndef multiply(a, b):\n    return a * b\n\nx = int(input())\ny = int(input())\nprint("합:", add(x, y))\nprint("차:", subtract(x, y))\nprint("곱:", multiply(x, y))',
                "stdin": "6\n2\n",
                "input_hint": "숫자를 한 줄씩 입력해보세요. 예: 6 / 2",
                "hints": ["세 함수 모두 두 개의 매개변수를 받아 계산 결과를 return하는 형태로 만드세요.", "함수를 다 만든 뒤, input()으로 받은 두 값을 각 함수에 넘겨서 결과를 출력하세요.", 'def add(a, b):\n    return a + b\n\ndef subtract(a, b):\n    return a - b\n\ndef multiply(a, b):\n    return a * b\n\nx = int(input())\ny = int(input())\nprint("합:", add(x, y))\nprint("차:", subtract(x, y))\nprint("곱:", multiply(x, y))'],
            },
        ],
    },
    {
        "id": 9,
        "title": "파일과 모듈",
        "goal": "파일 저장·불러오기와 코드 가져오기",
        "concepts": [
            {
                "id": "file-write",
                "title": "파일에 쓰기",
                "explanation": 'open("파일명", "w")로 파일을 쓰기 모드로 열고 write()로 내용을 저장합니다. with 문을 쓰면 자동으로 파일이 닫힙니다.',
                "example_code": 'with open("memo.txt", "w") as f:\n    f.write("안녕하세요")',
            },
            {
                "id": "file-read",
                "title": "파일 읽기",
                "explanation": 'open("파일명")으로 파일을 열고 read()로 전체 내용을 문자열로 가져올 수 있습니다.',
                "example_code": 'with open("memo.txt", "w") as f:\n    f.write("안녕하세요")\n\nwith open("memo.txt") as f:\n    print(f.read())',
            },
            {
                "id": "import-module",
                "title": "import로 모듈 가져오기",
                "explanation": "import 모듈이름 으로 다른 파일(모듈)에 이미 만들어진 기능을 가져와 쓸 수 있습니다. math는 수학 계산을 위한 표준 모듈입니다.",
                "example_code": "import math\nprint(math.sqrt(16))",
            },
        ],
        "problems": [
            {
                "id": "p1-write-read",
                "concept_id": "file-write",
                "prompt": 'memo.txt 파일에 "오늘의 다짐: 꾸준히 하자"를 저장한 뒤, 파일을 다시 읽어서 내용을 출력하세요.',
                "reference_code": 'with open("memo.txt", "w") as f:\n    f.write("오늘의 다짐: 꾸준히 하자")\n\nwith open("memo.txt") as f:\n    print(f.read())',
                "hints": [
                    "with open(\"memo.txt\", \"w\") as f: 다음 줄에서 f.write(...)로 저장합니다.",
                    "저장한 뒤에는 open(\"memo.txt\")로 다시 열어서 f.read()로 내용을 가져와 출력하세요.",
                    'with open("memo.txt", "w") as f:\n    f.write("오늘의 다짐: 꾸준히 하자")\n\nwith open("memo.txt") as f:\n    print(f.read())',
                ],
            },
            {
                "id": "p2-write-multiline",
                "concept_id": "file-read",
                "prompt": 'todo.txt 파일에 "숙제"와 "운동"을 줄바꿈으로 구분해서 저장한 뒤, 파일을 읽어서 그대로 출력하세요.',
                "reference_code": 'with open("todo.txt", "w") as f:\n    f.write("숙제\\n운동")\n\nwith open("todo.txt") as f:\n    print(f.read())',
                "hints": [
                    "문자열 안에 \\n을 넣으면 파일 안에서도 줄이 바뀝니다.",
                    'f.write("숙제\\n운동") 처럼 한 번에 두 줄을 저장할 수 있습니다.',
                    'with open("todo.txt", "w") as f:\n    f.write("숙제\\n운동")\n\nwith open("todo.txt") as f:\n    print(f.read())',
                ],
            },
            {
                "id": "p3-math-sqrt",
                "concept_id": "import-module",
                "prompt": "math 모듈을 가져와서 16의 제곱근을 출력하세요.",
                "reference_code": "import math\nprint(math.sqrt(16))",
                "hints": [
                    "가장 먼저 import math로 모듈을 가져와야 합니다.",
                    "제곱근 함수는 math.sqrt(숫자) 형태로 사용합니다.",
                    "import math\nprint(math.sqrt(16))",
                ],
            },
            {
                "id": "p4-math-floor",
                "concept_id": "import-module",
                "prompt": "math 모듈의 floor 함수를 사용해서 7.8을 내림한 값을 출력하세요.",
                "reference_code": "import math\nprint(math.floor(7.8))",
                "hints": [
                    "내림(소수점 버리기) 함수는 math 모듈 안에 있습니다.",
                    "math.floor(숫자) 형태로 사용해보세요.",
                    "import math\nprint(math.floor(7.8))",
                ],
            },
            {
                "id": "p5-mini-memo-saver",
                "concept_id": "file-write",
                "prompt": 'input()으로 메모 내용을 입력받아 notes.txt에 저장하고, 저장 직후 파일을 다시 읽어 "저장된 메모: OOO" 형식으로 출력하세요.',
                "reference_code": 'memo = input()\nwith open("notes.txt", "w") as f:\n    f.write(memo)\n\nwith open("notes.txt") as f:\n    saved = f.read()\nprint("저장된 메모: " + saved)',
                "stdin": "오늘도 화이팅\n",
                "input_hint": "메모로 남길 문장을 입력해보세요. 예: 오늘도 화이팅",
                "hints": [
                    "input()으로 받은 값을 변수에 저장한 뒤, 그 변수를 파일에 write하세요.",
                    "저장 후 파일을 다시 열어 read()로 읽은 값을 saved 같은 변수에 담아 출력하세요.",
                    'memo = input()\nwith open("notes.txt", "w") as f:\n    f.write(memo)\n\nwith open("notes.txt") as f:\n    saved = f.read()\nprint("저장된 메모: " + saved)',
                ],
            },
        ],
    },
    {
        "id": 10,
        "title": "실전 종합",
        "goal": "지금까지 배운 문법을 조합해 작은 프로그램 완성하기",
        "concepts": [
            {
                "id": "combining-skills",
                "title": "여러 기능 조합하기",
                "explanation": "지금까지 배운 변수, 조건문, 반복문, 함수, 리스트, 파일을 하나의 프로그램 안에서 함께 사용할 수 있습니다. 큰 문제는 작은 단계로 나눠서 순서대로 해결하세요.",
                "example_code": 'def check_even_odd(n):\n    if n % 2 == 0:\n        return "짝수"\n    else:\n        return "홀수"\n\nprint(check_even_odd(7))',
            },
            {
                "id": "program-design",
                "title": "작은 프로그램 설계하기",
                "explanation": "입력받기 → 처리하기 → 출력하기 순서로 생각하면 복잡한 프로그램도 단계별로 만들 수 있습니다.",
                "example_code": 'nums = [3, 8, 1, 9, 4]\nfor n in nums:\n    if n % 2 == 0:\n        print(n)',
            },
        ],
        "problems": [
            {
                "id": "p1-function-if",
                "concept_id": "combining-skills",
                "prompt": "숫자를 받아 짝수면 '짝수', 홀수면 '홀수'를 돌려주는 check_even_odd(n) 함수를 만들고, check_even_odd(7)의 결과를 출력하세요.",
                "reference_code": 'def check_even_odd(n):\n    if n % 2 == 0:\n        return "짝수"\n    else:\n        return "홀수"\n\nprint(check_even_odd(7))',
                "hints": [
                    "함수 안에서 if/else로 짝수인지 홀수인지 판단한 뒤 return하세요.",
                    "print(check_even_odd(7)) 로 결과를 확인하세요.",
                    'def check_even_odd(n):\n    if n % 2 == 0:\n        return "짝수"\n    else:\n        return "홀수"\n\nprint(check_even_odd(7))',
                ],
            },
            {
                "id": "p2-filter-even",
                "concept_id": "program-design",
                "prompt": "숫자 리스트 [3, 8, 1, 9, 4]에서 짝수만 한 줄에 하나씩 출력하세요.",
                "reference_code": "nums = [3, 8, 1, 9, 4]\nfor n in nums:\n    if n % 2 == 0:\n        print(n)",
                "hints": [
                    "리스트를 for로 순회하면서, 각 값에 if로 짝수 조건을 검사하세요.",
                    "조건이 참일 때만 print 하면 짝수만 걸러낼 수 있습니다.",
                    "nums = [3, 8, 1, 9, 4]\nfor n in nums:\n    if n % 2 == 0:\n        print(n)",
                ],
            },
            {
                "id": "p3-function-list-total",
                "concept_id": "combining-skills",
                "prompt": "숫자 리스트를 받아 합계를 돌려주는 total(nums) 함수를 만들고, total([1, 2, 3, 4, 5])의 결과를 출력하세요.",
                "reference_code": "def total(nums):\n    s = 0\n    for n in nums:\n        s += n\n    return s\n\nprint(total([1, 2, 3, 4, 5]))",
                "hints": [
                    "함수 안에서 합계를 저장할 변수(s=0)를 만들고, for로 리스트를 돌며 더해나가세요.",
                    "반복이 끝난 뒤 s를 return하면 됩니다.",
                    "def total(nums):\n    s = 0\n    for n in nums:\n        s += n\n    return s\n\nprint(total([1, 2, 3, 4, 5]))",
                ],
            },
            {
                "id": "p4-find-max",
                "concept_id": "program-design",
                "prompt": "input()으로 숫자를 3개 입력받아, 그 중 가장 큰 값을 출력하세요.",
                "reference_code": "biggest = int(input())\nfor _ in range(2):\n    n = int(input())\n    if n > biggest:\n        biggest = n\nprint(biggest)",
                "stdin": "4\n9\n2\n",
                "input_hint": "숫자 3개를 한 줄씩 입력해보세요. 예: 4 / 9 / 2",
                "hints": [
                    "첫 입력값을 일단 가장 큰 값으로 가정하고 시작하세요.",
                    "나머지 두 번은 반복문 안에서 입력받아, 지금까지의 최댓값보다 크면 갱신하세요.",
                    "biggest = int(input())\nfor _ in range(2):\n    n = int(input())\n    if n > biggest:\n        biggest = n\nprint(biggest)",
                ],
            },
            {
                "id": "p5-final-project",
                "concept_id": "combining-skills",
                "prompt": (
                    "input()으로 이름, 나이, 취미를 순서대로 입력받아 아래 형식으로 출력하는 자기소개 프로그램을 완성하세요 "
                    "(성인 여부는 19세 기준).\n"
                    "=== 자기소개 ===\n이름: OOO\n나이: OO살\n취미: OOO\n성인 여부: 성인입니다 / 미성년자입니다"
                ),
                "reference_code": (
                    'name = input()\n'
                    'age = int(input())\n'
                    'hobby = input()\n'
                    'print("=== 자기소개 ===")\n'
                    'print("이름: " + name)\n'
                    'print("나이: " + str(age) + "살")\n'
                    'print("취미: " + hobby)\n'
                    'if age >= 19:\n'
                    '    print("성인 여부: 성인입니다")\n'
                    'else:\n'
                    '    print("성인 여부: 미성년자입니다")'
                ),
                "stdin": "파이코치\n5\n코딩\n",
                "input_hint": "이름 / 나이 / 취미 순서로 한 줄씩 입력해보세요. 예: 홍길동 / 10 / 게임",
                "hints": [
                    "input()을 세 번 받아 이름, 나이, 취미를 각각 변수에 저장하세요. 나이는 숫자로 변환합니다.",
                    "지금까지 배운 문자열 이어붙이기와 if/else를 그대로 활용하면 됩니다. 순서대로 한 줄씩 print하세요.",
                    (
                        'name = input()\n'
                        'age = int(input())\n'
                        'hobby = input()\n'
                        'print("=== 자기소개 ===")\n'
                        'print("이름: " + name)\n'
                        'print("나이: " + str(age) + "살")\n'
                        'print("취미: " + hobby)\n'
                        'if age >= 19:\n'
                        '    print("성인 여부: 성인입니다")\n'
                        'else:\n'
                        '    print("성인 여부: 미성년자입니다")'
                    ),
                ],
            },
        ],
    },
]


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
