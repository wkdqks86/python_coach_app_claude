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
    {
        "id": 11,
        "title": "numpy 배열 기초",
        "goal": "리스트와 다른 ndarray의 개념, 생성·인덱싱·슬라이싱",
        "concepts": [
            {
                "id": "ndarray-basics",
                "title": "numpy 배열(ndarray) 만들기",
                "explanation": "np.array(리스트)로 파이썬 리스트를 numpy 배열로 바꿀 수 있습니다. 배열은 리스트와 비슷해 보이지만, 모든 값에 한 번에 계산을 적용할 수 있다는 큰 차이가 있습니다.",
                "example_code": "import numpy as np\narr = np.array([10, 20, 30])\nprint(arr)",
            },
            {
                "id": "ndarray-index-slice",
                "title": "인덱싱과 슬라이싱",
                "explanation": "배열도 리스트처럼 arr[인덱스]로 값 하나를, arr[시작:끝]으로 여러 값을 꺼낼 수 있습니다.",
                "example_code": "import numpy as np\narr = np.array([10, 20, 30, 40])\nprint(arr[1])\nprint(arr[:2])",
            },
            {
                "id": "ndarray-stats",
                "title": "배열의 기본 통계 함수",
                "explanation": "sum(), mean(), max(), min()으로 배열 전체의 합계·평균·최댓값·최솟값을 반복문 없이 한 번에 구할 수 있습니다.",
                "example_code": "import numpy as np\narr = np.array([10, 20, 30])\nprint(arr.sum())\nprint(arr.mean())",
            },
        ],
        "problems": [
            {
                "id": "p1-make-array",
                "concept_id": "ndarray-basics",
                "prompt": "numpy로 [10, 20, 30, 40, 50] 배열을 만들고 출력하세요.",
                "reference_code": "import numpy as np\narr = np.array([10, 20, 30, 40, 50])\nprint(arr)",
                "hints": [
                    "먼저 import numpy as np로 numpy를 가져와야 합니다.",
                    "np.array(리스트) 형태로 배열을 만들 수 있습니다.",
                    "import numpy as np\narr = np.array([10, 20, 30, 40, 50])\nprint(arr)",
                ],
            },
            {
                "id": "p2-index",
                "concept_id": "ndarray-index-slice",
                "prompt": "배열 [10, 20, 30, 40, 50]에서 세 번째 값(30)을 출력하세요.",
                "reference_code": "import numpy as np\narr = np.array([10, 20, 30, 40, 50])\nprint(arr[2])",
                "hints": [
                    "리스트와 마찬가지로 인덱스는 0부터 시작합니다.",
                    "arr[2]가 세 번째 값입니다.",
                    "import numpy as np\narr = np.array([10, 20, 30, 40, 50])\nprint(arr[2])",
                ],
            },
            {
                "id": "p3-slice",
                "concept_id": "ndarray-index-slice",
                "prompt": "배열 [10, 20, 30, 40, 50]에서 처음 3개 값만 출력하세요.",
                "reference_code": "import numpy as np\narr = np.array([10, 20, 30, 40, 50])\nprint(arr[:3])",
                "hints": [
                    "슬라이싱 arr[:n]은 처음부터 n개를 잘라냅니다.",
                    "arr[:3]을 출력해보세요.",
                    "import numpy as np\narr = np.array([10, 20, 30, 40, 50])\nprint(arr[:3])",
                ],
            },
            {
                "id": "p4-sum-mean",
                "concept_id": "ndarray-stats",
                "prompt": '성적 배열 [80, 90, 70, 100, 85]의 합계와 평균을 "합계: N", "평균: N" 형식으로 출력하세요.',
                "reference_code": 'import numpy as np\nscores = np.array([80, 90, 70, 100, 85])\nprint("합계:", scores.sum())\nprint("평균:", scores.mean())',
                "hints": [
                    "배열에는 sum()과 mean() 메서드가 바로 붙어 있습니다.",
                    "scores.sum(), scores.mean()을 각각 출력하세요.",
                    'import numpy as np\nscores = np.array([80, 90, 70, 100, 85])\nprint("합계:", scores.sum())\nprint("평균:", scores.mean())',
                ],
            },
            {
                "id": "p5-mini-max-min",
                "concept_id": "ndarray-stats",
                "prompt": '성적 배열 [80, 90, 70, 100, 85]에서 최고점과 최저점을 "최고점: N", "최저점: N" 형식으로 출력하세요.',
                "reference_code": 'import numpy as np\nscores = np.array([80, 90, 70, 100, 85])\nprint("최고점:", scores.max())\nprint("최저점:", scores.min())',
                "hints": [
                    "max()와 min()으로 배열의 최댓값과 최솟값을 구할 수 있습니다.",
                    "scores.max(), scores.min()을 각각 출력하세요.",
                    'import numpy as np\nscores = np.array([80, 90, 70, 100, 85])\nprint("최고점:", scores.max())\nprint("최저점:", scores.min())',
                ],
            },
        ],
    },
    {
        "id": 12,
        "title": "numpy 벡터 연산",
        "goal": "브로드캐스팅, 축(axis) 연산, 반복문 없이 계산하기",
        "concepts": [
            {
                "id": "broadcasting",
                "title": "배열 전체에 한 번에 연산하기",
                "explanation": "arr + 10 처럼 배열에 숫자를 바로 연산하면, 반복문 없이 모든 값에 그 연산이 적용됩니다. 이를 브로드캐스팅이라고 합니다.",
                "example_code": "import numpy as np\narr = np.array([1, 2, 3])\nprint(arr + 10)",
            },
            {
                "id": "array-array-op",
                "title": "배열끼리 연산하기",
                "explanation": "크기가 같은 두 배열은 +, -, *, / 로 같은 위치의 값끼리 계산됩니다.",
                "example_code": "import numpy as np\na = np.array([1, 2, 3])\nb = np.array([10, 20, 30])\nprint(a + b)",
            },
            {
                "id": "boolean-filtering",
                "title": "조건으로 배열 필터링하기",
                "explanation": "arr[arr > 5] 처럼 배열 안에 조건을 넣으면, 그 조건을 만족하는 값만 골라낼 수 있습니다.",
                "example_code": "import numpy as np\narr = np.array([1, 6, 3, 8])\nprint(arr[arr > 5])",
            },
        ],
        "problems": [
            {
                "id": "p1-add-scalar",
                "concept_id": "broadcasting",
                "prompt": "배열 [1, 2, 3, 4, 5]의 모든 값에 10을 더한 결과를 출력하세요.",
                "reference_code": "import numpy as np\narr = np.array([1, 2, 3, 4, 5])\nprint(arr + 10)",
                "hints": [
                    "반복문 없이 arr + 10처럼 배열에 바로 숫자를 더할 수 있습니다.",
                    "print(arr + 10)을 그대로 써보세요.",
                    "import numpy as np\narr = np.array([1, 2, 3, 4, 5])\nprint(arr + 10)",
                ],
            },
            {
                "id": "p2-multiply-scalar",
                "concept_id": "broadcasting",
                "prompt": "밝기 배열 [50, 100, 150]의 모든 값을 2배로 만들어 출력하세요.",
                "reference_code": "import numpy as np\nbrightness = np.array([50, 100, 150])\nprint(brightness * 2)",
                "hints": [
                    "곱셈도 브로드캐스팅이 그대로 적용됩니다.",
                    "brightness * 2를 출력해보세요.",
                    "import numpy as np\nbrightness = np.array([50, 100, 150])\nprint(brightness * 2)",
                ],
            },
            {
                "id": "p3-array-plus-array",
                "concept_id": "array-array-op",
                "prompt": "배열 [1, 2, 3]과 [10, 20, 30]을 더한 결과를 출력하세요.",
                "reference_code": "import numpy as np\na = np.array([1, 2, 3])\nb = np.array([10, 20, 30])\nprint(a + b)",
                "hints": [
                    "두 배열의 크기가 같으면 같은 위치끼리 더해집니다.",
                    "a + b를 출력해보세요.",
                    "import numpy as np\na = np.array([1, 2, 3])\nb = np.array([10, 20, 30])\nprint(a + b)",
                ],
            },
            {
                "id": "p4-filter",
                "concept_id": "boolean-filtering",
                "prompt": "배열 [3, 8, 1, 9, 4, 6]에서 5보다 큰 값만 출력하세요.",
                "reference_code": "import numpy as np\narr = np.array([3, 8, 1, 9, 4, 6])\nprint(arr[arr > 5])",
                "hints": [
                    "arr > 5는 각 값이 조건을 만족하는지 True/False 배열을 만들어줍니다.",
                    "arr[arr > 5] 처럼 배열 안에 조건을 그대로 넣으면 걸러낼 수 있습니다.",
                    "import numpy as np\narr = np.array([3, 8, 1, 9, 4, 6])\nprint(arr[arr > 5])",
                ],
            },
            {
                "id": "p5-mini-brightness",
                "concept_id": "boolean-filtering",
                "prompt": "이미지 픽셀 배열 [200, 220, 240, 260, 280]의 모든 값에 30을 더한 뒤, 255 이하인 값만 출력하세요.",
                "reference_code": "import numpy as np\npixels = np.array([200, 220, 240, 260, 280])\nbrightened = pixels + 30\nprint(brightened[brightened <= 255])",
                "hints": [
                    "먼저 브로드캐스팅으로 전체 값에 30을 더한 새 배열을 만드세요.",
                    "그 다음 조건 필터링으로 255 이하인 값만 골라내세요.",
                    "import numpy as np\npixels = np.array([200, 220, 240, 260, 280])\nbrightened = pixels + 30\nprint(brightened[brightened <= 255])",
                ],
            },
        ],
    },
    {
        "id": 13,
        "title": "pandas Series/DataFrame",
        "goal": "표 형태 데이터 읽기·선택·필터링",
        "concepts": [
            {
                "id": "series-basics",
                "title": "Series 만들기",
                "explanation": "pandas의 Series는 인덱스가 붙은 1차원 데이터입니다. pd.Series(리스트)로 만들 수 있습니다.",
                "example_code": "import pandas as pd\ns = pd.Series([10, 20, 30])\nprint(s)",
            },
            {
                "id": "dataframe-basics",
                "title": "DataFrame 만들고 컬럼 선택하기",
                "explanation": "DataFrame은 여러 열(컬럼)로 이루어진 표입니다. pd.DataFrame({\"컬럼\": [값들]})로 만들고, df[\"컬럼\"]으로 원하는 열만 꺼낼 수 있습니다.",
                "example_code": 'import pandas as pd\ndata = {"이름": ["철수", "영희"], "점수": [90, 85]}\ndf = pd.DataFrame(data)\nprint(df["점수"])',
            },
            {
                "id": "dataframe-filter",
                "title": "조건으로 행 선택하기",
                "explanation": "df[df[\"컬럼\"] > 값] 형태로 조건을 만족하는 행만 골라낼 수 있습니다. numpy 배열 필터링과 같은 원리입니다.",
                "example_code": 'import pandas as pd\ndata = {"이름": ["철수", "영희"], "점수": [90, 85]}\ndf = pd.DataFrame(data)\nprint(df[df["점수"] >= 90])',
            },
        ],
        "problems": [
            {
                "id": "p1-make-series",
                "concept_id": "series-basics",
                "prompt": "pandas로 [10, 20, 30] 값을 가진 Series를 만들고 출력하세요.",
                "reference_code": "import pandas as pd\ns = pd.Series([10, 20, 30])\nprint(s)",
                "hints": [
                    "import pandas as pd로 pandas를 가져오세요.",
                    "pd.Series(리스트)로 Series를 만들 수 있습니다.",
                    "import pandas as pd\ns = pd.Series([10, 20, 30])\nprint(s)",
                ],
            },
            {
                "id": "p2-dataframe-column",
                "concept_id": "dataframe-basics",
                "prompt": '이름 ["철수", "영희", "민수"]과 점수 [90, 85, 95]로 DataFrame을 만들고, "점수" 컬럼만 출력하세요.',
                "reference_code": 'import pandas as pd\ndata = {"이름": ["철수", "영희", "민수"], "점수": [90, 85, 95]}\ndf = pd.DataFrame(data)\nprint(df["점수"])',
                "hints": [
                    "딕셔너리 {\"컬럼명\": [값들]} 형태로 pd.DataFrame()에 전달하세요.",
                    "df[\"점수\"]로 점수 컬럼만 꺼낼 수 있습니다.",
                    'import pandas as pd\ndata = {"이름": ["철수", "영희", "민수"], "점수": [90, 85, 95]}\ndf = pd.DataFrame(data)\nprint(df["점수"])',
                ],
            },
            {
                "id": "p3-first-row-value",
                "concept_id": "dataframe-basics",
                "prompt": "위와 같은 DataFrame에서 첫 번째 사람의 이름을 출력하세요.",
                "reference_code": 'import pandas as pd\ndata = {"이름": ["철수", "영희", "민수"], "점수": [90, 85, 95]}\ndf = pd.DataFrame(data)\nprint(df["이름"][0])',
                "hints": [
                    "먼저 df[\"이름\"]으로 이름 컬럼(Series)을 꺼내세요.",
                    "그 뒤에 [0]을 붙이면 첫 번째 값에 접근할 수 있습니다.",
                    'import pandas as pd\ndata = {"이름": ["철수", "영희", "민수"], "점수": [90, 85, 95]}\ndf = pd.DataFrame(data)\nprint(df["이름"][0])',
                ],
            },
            {
                "id": "p4-filter-rows",
                "concept_id": "dataframe-filter",
                "prompt": "위와 같은 DataFrame에서 점수가 90 이상인 사람만 출력하세요.",
                "reference_code": 'import pandas as pd\ndata = {"이름": ["철수", "영희", "민수"], "점수": [90, 85, 95]}\ndf = pd.DataFrame(data)\nprint(df[df["점수"] >= 90])',
                "hints": [
                    "df[\"점수\"] >= 90은 각 행이 조건을 만족하는지 알려주는 True/False 목록입니다.",
                    "df[조건] 형태로 감싸면 조건을 만족하는 행만 남습니다.",
                    'import pandas as pd\ndata = {"이름": ["철수", "영희", "민수"], "점수": [90, 85, 95]}\ndf = pd.DataFrame(data)\nprint(df[df["점수"] >= 90])',
                ],
            },
            {
                "id": "p5-mini-csv-explorer",
                "concept_id": "dataframe-filter",
                "prompt": (
                    '상품 ["사과", "바나나", "포도"], 수량 [10, 5, 8]로 DataFrame을 만들고, '
                    "수량이 6개 이상인 상품의 이름만 출력하세요."
                ),
                "reference_code": (
                    'import pandas as pd\n'
                    'data = {"상품": ["사과", "바나나", "포도"], "수량": [10, 5, 8]}\n'
                    'df = pd.DataFrame(data)\n'
                    'print(df[df["수량"] >= 6]["상품"])'
                ),
                "hints": [
                    "먼저 조건으로 행을 필터링한 뒤, 그 결과에서 다시 [\"상품\"] 컬럼만 꺼내면 됩니다.",
                    "df[df[\"수량\"] >= 6][\"상품\"] 처럼 대괄호를 두 번 이어서 쓸 수 있습니다.",
                    (
                        'import pandas as pd\n'
                        'data = {"상품": ["사과", "바나나", "포도"], "수량": [10, 5, 8]}\n'
                        'df = pd.DataFrame(data)\n'
                        'print(df[df["수량"] >= 6]["상품"])'
                    ),
                ],
            },
        ],
    },
    {
        "id": 14,
        "title": "pandas 데이터 정제",
        "goal": "결측치·중복 처리, groupby, 정렬",
        "concepts": [
            {
                "id": "missing-values",
                "title": "결측치 확인하고 채우기",
                "explanation": "빈 값(None)은 결측치라고 부릅니다. isna()로 어디가 비어있는지 확인하고, fillna(값)으로 채울 수 있습니다.",
                "example_code": 'import pandas as pd\ns = pd.Series([90, None, 95])\nprint(s.isna().sum())',
            },
            {
                "id": "groupby",
                "title": "groupby로 그룹별 집계하기",
                "explanation": "groupby(\"컬럼\")으로 같은 값끼리 묶은 뒤 sum(), mean() 등을 붙이면 그룹별 통계를 구할 수 있습니다.",
                "example_code": 'import pandas as pd\ndata = {"분류": ["A", "A", "B"], "수량": [10, 20, 5]}\ndf = pd.DataFrame(data)\nprint(df.groupby("분류")["수량"].sum())',
            },
            {
                "id": "sort-values",
                "title": "sort_values로 정렬하기",
                "explanation": "sort_values(\"컬럼\")으로 특정 컬럼 기준 오름차순 정렬을, ascending=False를 추가하면 내림차순 정렬을 할 수 있습니다.",
                "example_code": 'import pandas as pd\ndata = {"이름": ["철수", "영희"], "점수": [70, 95]}\ndf = pd.DataFrame(data)\nprint(df.sort_values("점수", ascending=False)["이름"])',
            },
        ],
        "problems": [
            {
                "id": "p1-count-missing",
                "concept_id": "missing-values",
                "prompt": '점수 [90, None, 95]로 Series를 만들고, 결측치(빈 값)가 몇 개인지 출력하세요.',
                "reference_code": "import pandas as pd\nscores = pd.Series([90, None, 95])\nprint(scores.isna().sum())",
                "hints": [
                    "isna()는 각 값이 비어있는지 True/False로 알려줍니다.",
                    "isna().sum()을 이어서 쓰면 True(비어있음)의 개수를 셀 수 있습니다.",
                    "import pandas as pd\nscores = pd.Series([90, None, 95])\nprint(scores.isna().sum())",
                ],
            },
            {
                "id": "p2-fill-missing",
                "concept_id": "missing-values",
                "prompt": "위와 같은 점수 Series에서 빈 값을 0으로 채운 뒤 출력하세요.",
                "reference_code": "import pandas as pd\nscores = pd.Series([90, None, 95])\nscores = scores.fillna(0)\nprint(scores)",
                "hints": [
                    "fillna(값)으로 빈 자리를 원하는 값으로 채울 수 있습니다.",
                    "scores = scores.fillna(0) 처럼 결과를 다시 저장한 뒤 출력하세요.",
                    "import pandas as pd\nscores = pd.Series([90, None, 95])\nscores = scores.fillna(0)\nprint(scores)",
                ],
            },
            {
                "id": "p3-groupby-sum",
                "concept_id": "groupby",
                "prompt": '분류 ["과일", "과일", "채소"]와 수량 [10, 20, 5]로 DataFrame을 만들고, 분류별 수량 합계를 출력하세요.',
                "reference_code": 'import pandas as pd\ndata = {"분류": ["과일", "과일", "채소"], "수량": [10, 20, 5]}\ndf = pd.DataFrame(data)\nprint(df.groupby("분류")["수량"].sum())',
                "hints": [
                    "groupby(\"분류\")로 같은 분류끼리 묶을 수 있습니다.",
                    "묶은 뒤 [\"수량\"].sum()을 이어 붙이면 분류별 합계가 나옵니다.",
                    'import pandas as pd\ndata = {"분류": ["과일", "과일", "채소"], "수량": [10, 20, 5]}\ndf = pd.DataFrame(data)\nprint(df.groupby("분류")["수량"].sum())',
                ],
            },
            {
                "id": "p4-sort-values",
                "concept_id": "sort-values",
                "prompt": '이름 ["철수", "영희", "민수"]과 점수 [70, 95, 85]로 DataFrame을 만들고, 점수가 높은 순서대로 이름만 출력하세요.',
                "reference_code": 'import pandas as pd\ndata = {"이름": ["철수", "영희", "민수"], "점수": [70, 95, 85]}\ndf = pd.DataFrame(data)\nsorted_df = df.sort_values("점수", ascending=False)\nprint(sorted_df["이름"])',
                "hints": [
                    "sort_values(\"점수\", ascending=False)로 점수를 내림차순 정렬할 수 있습니다.",
                    "정렬한 결과를 변수에 저장한 뒤, 그 결과에서 [\"이름\"]을 출력하세요.",
                    'import pandas as pd\ndata = {"이름": ["철수", "영희", "민수"], "점수": [70, 95, 85]}\ndf = pd.DataFrame(data)\nsorted_df = df.sort_values("점수", ascending=False)\nprint(sorted_df["이름"])',
                ],
            },
            {
                "id": "p5-mini-sales-report",
                "concept_id": "groupby",
                "prompt": (
                    '분류 ["과일", "채소", "과일", "채소"]와 수량 [10, 15, 20, 5]로 DataFrame을 만들고, '
                    '분류별 합계를 출력한 뒤 "가장 많이 팔린 카테고리: OOO" 형식으로 가장 합계가 큰 분류를 출력하세요.'
                ),
                "reference_code": (
                    'import pandas as pd\n'
                    'data = {"분류": ["과일", "채소", "과일", "채소"], "수량": [10, 15, 20, 5]}\n'
                    'df = pd.DataFrame(data)\n'
                    'summary = df.groupby("분류")["수량"].sum()\n'
                    'print(summary)\n'
                    'print("가장 많이 팔린 카테고리:", summary.idxmax())'
                ),
                "hints": [
                    "먼저 groupby로 분류별 합계(summary)를 구해서 출력하세요.",
                    "summary.idxmax()는 값이 가장 큰 행의 인덱스(분류 이름)를 돌려줍니다.",
                    (
                        'import pandas as pd\n'
                        'data = {"분류": ["과일", "채소", "과일", "채소"], "수량": [10, 15, 20, 5]}\n'
                        'df = pd.DataFrame(data)\n'
                        'summary = df.groupby("분류")["수량"].sum()\n'
                        'print(summary)\n'
                        'print("가장 많이 팔린 카테고리:", summary.idxmax())'
                    ),
                ],
            },
        ],
    },
    {
        "id": 15,
        "title": "데이터 탐색과 요약 통계",
        "goal": "describe·value_counts로 분포 파악하기 (그래프 시각화는 실제 노트북 환경에서 별도로 연습하는 것을 권장)",
        "concepts": [
            {
                "id": "describe",
                "title": "describe()로 요약 통계 한눈에 보기",
                "explanation": "describe()를 쓰면 개수, 평균, 표준편차, 최솟값, 최댓값 등을 한 번에 볼 수 있습니다. 데이터를 처음 살펴볼 때 가장 먼저 쓰는 명령입니다.",
                "example_code": "import pandas as pd\ns = pd.Series([10, 20, 30, 40, 50])\nprint(s.describe())",
            },
            {
                "id": "value-counts",
                "title": "value_counts()로 값별 개수 세기",
                "explanation": "카테고리 데이터에서 각 값이 몇 번씩 나오는지 value_counts()로 셀 수 있습니다. 어떤 값이 가장 흔한지 바로 알 수 있습니다.",
                "example_code": 'import pandas as pd\nfruits = pd.Series(["사과", "바나나", "사과"])\nprint(fruits.value_counts())',
            },
            {
                "id": "agg",
                "title": "agg()로 여러 통계를 한 번에 계산하기",
                "explanation": "agg([\"mean\", \"max\", \"min\"])처럼 원하는 통계 함수 이름을 리스트로 넘기면, 여러 결과를 한 번에 계산해줍니다.",
                "example_code": 'import pandas as pd\ns = pd.Series([10, 20, 30])\nprint(s.agg(["mean", "max"]))',
            },
        ],
        "problems": [
            {
                "id": "p1-describe",
                "concept_id": "describe",
                "prompt": "점수 [70, 85, 90, 60, 95]로 Series를 만들고 describe()의 결과를 출력하세요.",
                "reference_code": "import pandas as pd\ns = pd.Series([70, 85, 90, 60, 95])\nprint(s.describe())",
                "hints": [
                    "Series를 만든 뒤 describe() 메서드를 바로 이어서 부를 수 있습니다.",
                    "print(s.describe())를 써보세요.",
                    "import pandas as pd\ns = pd.Series([70, 85, 90, 60, 95])\nprint(s.describe())",
                ],
            },
            {
                "id": "p2-describe-mean",
                "concept_id": "describe",
                "prompt": "위와 같은 점수 Series의 describe() 결과에서 평균(mean)만 출력하세요.",
                "reference_code": 'import pandas as pd\ns = pd.Series([70, 85, 90, 60, 95])\nprint(s.describe()["mean"])',
                "hints": [
                    "describe()의 결과도 Series라서 [\"mean\"]처럼 이름으로 값을 꺼낼 수 있습니다.",
                    "s.describe()[\"mean\"]을 출력해보세요.",
                    'import pandas as pd\ns = pd.Series([70, 85, 90, 60, 95])\nprint(s.describe()["mean"])',
                ],
            },
            {
                "id": "p3-value-counts",
                "concept_id": "value-counts",
                "prompt": '과일 목록 ["사과", "바나나", "사과", "포도", "바나나", "사과"]에서 각 과일이 몇 번 나오는지 세어 출력하세요.',
                "reference_code": 'import pandas as pd\nfruits = pd.Series(["사과", "바나나", "사과", "포도", "바나나", "사과"])\nprint(fruits.value_counts())',
                "hints": [
                    "리스트를 Series로 만든 뒤 value_counts()를 이어서 부르세요.",
                    "print(fruits.value_counts())를 써보세요.",
                    'import pandas as pd\nfruits = pd.Series(["사과", "바나나", "사과", "포도", "바나나", "사과"])\nprint(fruits.value_counts())',
                ],
            },
            {
                "id": "p4-most-common",
                "concept_id": "value-counts",
                "prompt": "위와 같은 과일 데이터에서 가장 많이 나온 과일 이름만 출력하세요.",
                "reference_code": 'import pandas as pd\nfruits = pd.Series(["사과", "바나나", "사과", "포도", "바나나", "사과"])\nprint(fruits.value_counts().idxmax())',
                "hints": [
                    "value_counts()의 결과에서 idxmax()를 쓰면 가장 큰 값의 이름(인덱스)을 알 수 있습니다.",
                    "fruits.value_counts().idxmax()를 출력해보세요.",
                    'import pandas as pd\nfruits = pd.Series(["사과", "바나나", "사과", "포도", "바나나", "사과"])\nprint(fruits.value_counts().idxmax())',
                ],
            },
            {
                "id": "p5-mini-eda-summary",
                "concept_id": "agg",
                "prompt": "점수 [70, 85, 90, 60, 95, 100]으로 Series를 만들고, 평균·최댓값·최솟값을 agg([\"mean\", \"max\", \"min\"])으로 한 번에 계산해서 출력하세요.",
                "reference_code": 'import pandas as pd\ns = pd.Series([70, 85, 90, 60, 95, 100])\nprint(s.agg(["mean", "max", "min"]))',
                "hints": [
                    "agg()에 원하는 통계 함수 이름을 문자열 리스트로 넘기면 한 번에 계산됩니다.",
                    's.agg(["mean", "max", "min"])을 출력해보세요.',
                    'import pandas as pd\ns = pd.Series([70, 85, 90, 60, 95, 100])\nprint(s.agg(["mean", "max", "min"]))',
                ],
            },
        ],
    },
    {
        "id": 16,
        "title": "캐글 워크플로 이해",
        "goal": "대회 페이지 구조, train/test/submission 파일 읽기",
        "concepts": [
            {
                "id": "kaggle-files",
                "title": "Kaggle 대회의 기본 파일 구조",
                "explanation": "Kaggle 대회는 보통 정답이 있는 train.csv(학습용), 정답이 없는 test.csv(예측 대상), 제출 형식을 보여주는 sample_submission.csv로 구성됩니다.",
                "example_code": 'import pandas as pd\nsubmission = pd.DataFrame({"id": [1, 2, 3], "target": [0, 0, 0]})\nprint(submission)',
            },
            {
                "id": "csv-read-write",
                "title": "CSV 파일 쓰고 읽기",
                "explanation": "to_csv(파일명, index=False)로 DataFrame을 CSV로 저장하고, pd.read_csv(파일명)으로 다시 불러올 수 있습니다. index=False를 빼먹으면 불필요한 인덱스 컬럼이 함께 저장됩니다.",
                "example_code": 'import pandas as pd\ndf = pd.DataFrame({"id": [1, 2], "score": [90, 85]})\ndf.to_csv("data.csv", index=False)\nprint(pd.read_csv("data.csv"))',
            },
            {
                "id": "shape-head",
                "title": "shape와 head()로 데이터 살펴보기",
                "explanation": "shape는 (행 개수, 열 개수)를 알려주고, head(n)은 처음 n개 행만 보여줍니다. 큰 데이터를 다루기 전에 항상 먼저 확인하는 습관을 들이면 좋습니다.",
                "example_code": 'import pandas as pd\ndf = pd.DataFrame({"id": [1, 2, 3], "score": [90, 85, 70]})\nprint(df.shape)\nprint(df.head(2))',
            },
        ],
        "problems": [
            {
                "id": "p1-write-read-csv",
                "concept_id": "csv-read-write",
                "prompt": "id [1, 2, 3]과 score [90, 85, 70]로 DataFrame을 만들어 data.csv로 저장한 뒤, 다시 읽어서 출력하세요.",
                "reference_code": 'import pandas as pd\ndf = pd.DataFrame({"id": [1, 2, 3], "score": [90, 85, 70]})\ndf.to_csv("data.csv", index=False)\nprint(pd.read_csv("data.csv"))',
                "hints": [
                    "to_csv(\"data.csv\", index=False)로 저장하세요. index=False를 빼먹지 마세요.",
                    "저장한 뒤 pd.read_csv(\"data.csv\")로 다시 읽어서 출력하세요.",
                    'import pandas as pd\ndf = pd.DataFrame({"id": [1, 2, 3], "score": [90, 85, 70]})\ndf.to_csv("data.csv", index=False)\nprint(pd.read_csv("data.csv"))',
                ],
            },
            {
                "id": "p2-shape",
                "concept_id": "shape-head",
                "prompt": "id [1, 2, 3]과 score [90, 85, 70]로 DataFrame을 만들어 저장 후 다시 읽어서, shape(행, 열 개수)를 출력하세요.",
                "reference_code": 'import pandas as pd\ndf = pd.DataFrame({"id": [1, 2, 3], "score": [90, 85, 70]})\ndf.to_csv("data.csv", index=False)\nloaded = pd.read_csv("data.csv")\nprint(loaded.shape)',
                "hints": [
                    "DataFrame에는 shape라는 속성이 바로 붙어 있습니다 (괄호 없이 씁니다).",
                    "loaded.shape를 출력해보세요.",
                    'import pandas as pd\ndf = pd.DataFrame({"id": [1, 2, 3], "score": [90, 85, 70]})\ndf.to_csv("data.csv", index=False)\nloaded = pd.read_csv("data.csv")\nprint(loaded.shape)',
                ],
            },
            {
                "id": "p3-head",
                "concept_id": "shape-head",
                "prompt": "위와 같은 데이터를 만들어 저장 후 다시 읽어서, 처음 2행만 출력하세요.",
                "reference_code": 'import pandas as pd\ndf = pd.DataFrame({"id": [1, 2, 3], "score": [90, 85, 70]})\ndf.to_csv("data.csv", index=False)\nloaded = pd.read_csv("data.csv")\nprint(loaded.head(2))',
                "hints": [
                    "head(n)에 원하는 개수를 넣으면 처음 n개 행만 볼 수 있습니다.",
                    "loaded.head(2)를 출력해보세요.",
                    'import pandas as pd\ndf = pd.DataFrame({"id": [1, 2, 3], "score": [90, 85, 70]})\ndf.to_csv("data.csv", index=False)\nloaded = pd.read_csv("data.csv")\nprint(loaded.head(2))',
                ],
            },
            {
                "id": "p4-make-submission",
                "concept_id": "kaggle-files",
                "prompt": "id [101, 102, 103] 모두에 target 값 0을 채운 제출 파일을 submission.csv로 저장하고, 다시 읽어서 출력하세요.",
                "reference_code": 'import pandas as pd\nsub = pd.DataFrame({"id": [101, 102, 103], "target": [0, 0, 0]})\nsub.to_csv("submission.csv", index=False)\nprint(pd.read_csv("submission.csv"))',
                "hints": [
                    "제출 파일은 보통 id 컬럼과 예측값 컬럼(여기서는 target) 두 개로 구성됩니다.",
                    "DataFrame을 만들어 to_csv로 저장한 뒤 다시 읽어서 출력하세요.",
                    'import pandas as pd\nsub = pd.DataFrame({"id": [101, 102, 103], "target": [0, 0, 0]})\nsub.to_csv("submission.csv", index=False)\nprint(pd.read_csv("submission.csv"))',
                ],
            },
            {
                "id": "p5-mini-baseline-submission",
                "concept_id": "kaggle-files",
                "prompt": (
                    "train 데이터의 target 값 [1, 0, 1, 0]의 평균을 구하고, test 데이터의 id [5, 6, 7] "
                    "모두에 그 평균값을 예측값으로 채운 제출 파일을 만들어 출력하세요."
                ),
                "reference_code": (
                    'import pandas as pd\n'
                    'train_target = [1, 0, 1, 0]\n'
                    'mean_target = sum(train_target) / len(train_target)\n'
                    'test_ids = [5, 6, 7]\n'
                    'sub = pd.DataFrame({"id": test_ids, "target": [mean_target] * len(test_ids)})\n'
                    'sub.to_csv("submission.csv", index=False)\n'
                    'print(pd.read_csv("submission.csv"))'
                ),
                "hints": [
                    "가장 간단한 베이스라인은 정답값을 몰라도, 학습 데이터의 평균으로 전부 똑같이 예측하는 것입니다.",
                    "평균을 구한 뒤, test id 개수만큼 그 값을 리스트로 반복해서 채우세요 ([값] * 개수).",
                    (
                        'import pandas as pd\n'
                        'train_target = [1, 0, 1, 0]\n'
                        'mean_target = sum(train_target) / len(train_target)\n'
                        'test_ids = [5, 6, 7]\n'
                        'sub = pd.DataFrame({"id": test_ids, "target": [mean_target] * len(test_ids)})\n'
                        'sub.to_csv("submission.csv", index=False)\n'
                        'print(pd.read_csv("submission.csv"))'
                    ),
                ],
            },
        ],
    },
    {
        "id": 17,
        "title": "EDA 실전",
        "goal": "결측치·이상치 탐색, feature별 타깃과의 관계 확인",
        "concepts": [
            {
                "id": "check-missing",
                "title": "결측치 확인하기",
                "explanation": "isnull().sum()으로 각 컬럼에 빈 값이 몇 개 있는지 한눈에 확인할 수 있습니다.",
                "example_code": 'import pandas as pd\ndf = pd.DataFrame({"나이": [22, None, 26]})\nprint(df.isnull().sum())',
            },
            {
                "id": "check-outliers",
                "title": "숫자 컬럼 분포 살펴보기",
                "explanation": "describe()의 min/max를 보면 비정상적으로 크거나 작은 값(이상치)이 있는지 힌트를 얻을 수 있습니다.",
                "example_code": 'import pandas as pd\ndf = pd.DataFrame({"나이": [22, 38, 26, 35]})\nprint(df["나이"].describe())',
            },
            {
                "id": "target-relationship",
                "title": "그룹별로 타깃과의 관계 살펴보기",
                "explanation": "groupby(\"컬럼\")[\"타깃\"].mean()으로 각 그룹(예: 성별)에 따라 타깃 값이 어떻게 다른지 확인할 수 있습니다. 이 차이가 클수록 좋은 feature일 가능성이 높습니다.",
                "example_code": 'import pandas as pd\ndf = pd.DataFrame({"성별": ["남", "여", "여"], "생존": [0, 1, 1]})\nprint(df.groupby("성별")["생존"].mean())',
            },
        ],
        "problems": [
            {
                "id": "p1-missing-all-columns",
                "concept_id": "check-missing",
                "prompt": '성별 ["남", "여", "여", "남", "여"], 나이 [22, 38, 26, None, 35], 생존 [0, 1, 1, 0, 1] 데이터를 만들고, 각 컬럼의 결측치 개수를 출력하세요.',
                "reference_code": 'import pandas as pd\ndf = pd.DataFrame({"성별": ["남", "여", "여", "남", "여"], "나이": [22, 38, 26, None, 35], "생존": [0, 1, 1, 0, 1]})\nprint(df.isnull().sum())',
                "hints": [
                    "df.isnull()은 각 칸이 비어있는지 True/False로 알려줍니다.",
                    ".sum()을 이어 붙이면 컬럼별로 True(결측치)의 개수를 셀 수 있습니다.",
                    'import pandas as pd\ndf = pd.DataFrame({"성별": ["남", "여", "여", "남", "여"], "나이": [22, 38, 26, None, 35], "생존": [0, 1, 1, 0, 1]})\nprint(df.isnull().sum())',
                ],
            },
            {
                "id": "p2-missing-one-column",
                "concept_id": "check-missing",
                "prompt": "위와 같은 데이터에서 나이 컬럼의 결측치가 몇 개인지 숫자만 출력하세요.",
                "reference_code": 'import pandas as pd\ndf = pd.DataFrame({"성별": ["남", "여", "여", "남", "여"], "나이": [22, 38, 26, None, 35], "생존": [0, 1, 1, 0, 1]})\nprint(df["나이"].isnull().sum())',
                "hints": [
                    "전체가 아니라 나이 컬럼 하나만 골라서 확인하면 됩니다.",
                    "df[\"나이\"].isnull().sum()을 출력해보세요.",
                    'import pandas as pd\ndf = pd.DataFrame({"성별": ["남", "여", "여", "남", "여"], "나이": [22, 38, 26, None, 35], "생존": [0, 1, 1, 0, 1]})\nprint(df["나이"].isnull().sum())',
                ],
            },
            {
                "id": "p3-describe-outliers",
                "concept_id": "check-outliers",
                "prompt": "위와 같은 데이터에서 나이 컬럼의 describe() 결과를 출력해서 최솟값과 최댓값을 확인하세요.",
                "reference_code": 'import pandas as pd\ndf = pd.DataFrame({"성별": ["남", "여", "여", "남", "여"], "나이": [22, 38, 26, None, 35], "생존": [0, 1, 1, 0, 1]})\nprint(df["나이"].describe())',
                "hints": [
                    "describe()는 결측치를 자동으로 제외하고 통계를 계산합니다.",
                    "df[\"나이\"].describe()를 출력해보세요.",
                    'import pandas as pd\ndf = pd.DataFrame({"성별": ["남", "여", "여", "남", "여"], "나이": [22, 38, 26, None, 35], "생존": [0, 1, 1, 0, 1]})\nprint(df["나이"].describe())',
                ],
            },
            {
                "id": "p4-groupby-target",
                "concept_id": "target-relationship",
                "prompt": "위와 같은 데이터에서 성별별 생존 평균(생존율)을 출력하세요.",
                "reference_code": 'import pandas as pd\ndf = pd.DataFrame({"성별": ["남", "여", "여", "남", "여"], "나이": [22, 38, 26, None, 35], "생존": [0, 1, 1, 0, 1]})\nprint(df.groupby("성별")["생존"].mean())',
                "hints": [
                    "groupby(\"성별\")로 같은 성별끼리 묶을 수 있습니다.",
                    "묶은 뒤 [\"생존\"].mean()을 이어 붙이면 성별별 생존율이 나옵니다.",
                    'import pandas as pd\ndf = pd.DataFrame({"성별": ["남", "여", "여", "남", "여"], "나이": [22, 38, 26, None, 35], "생존": [0, 1, 1, 0, 1]})\nprint(df.groupby("성별")["생존"].mean())',
                ],
            },
            {
                "id": "p5-mini-eda-report",
                "concept_id": "check-missing",
                "prompt": "위와 같은 데이터에서 나이 결측치를 나이 평균으로 채우고 채워진 나이 컬럼을 출력한 뒤, 성별별 생존율도 출력하세요.",
                "reference_code": (
                    'import pandas as pd\n'
                    'df = pd.DataFrame({"성별": ["남", "여", "여", "남", "여"], "나이": [22, 38, 26, None, 35], "생존": [0, 1, 1, 0, 1]})\n'
                    'df["나이"] = df["나이"].fillna(df["나이"].mean())\n'
                    'print(df["나이"])\n'
                    'print(df.groupby("성별")["생존"].mean())'
                ),
                "hints": [
                    "fillna(df[\"나이\"].mean())로 결측치를 평균값으로 채울 수 있습니다.",
                    "채운 결과를 다시 df[\"나이\"]에 저장한 뒤, 나이 컬럼과 성별별 생존율을 순서대로 출력하세요.",
                    (
                        'import pandas as pd\n'
                        'df = pd.DataFrame({"성별": ["남", "여", "여", "남", "여"], "나이": [22, 38, 26, None, 35], "생존": [0, 1, 1, 0, 1]})\n'
                        'df["나이"] = df["나이"].fillna(df["나이"].mean())\n'
                        'print(df["나이"])\n'
                        'print(df.groupby("성별")["생존"].mean())'
                    ),
                ],
            },
        ],
    },
    {
        "id": 18,
        "title": "피처 엔지니어링 기초",
        "goal": "인코딩, 스케일링, 파생 변수 만들기",
        "concepts": [
            {
                "id": "encoding",
                "title": "범주형을 숫자로 바꾸기 (인코딩)",
                "explanation": "머신러닝 모델은 대부분 숫자만 이해합니다. map({\"값\": 숫자})으로 문자열 범주를 숫자로 바꿀 수 있습니다.",
                "example_code": 'import pandas as pd\ndf = pd.DataFrame({"성별": ["남", "여", "남"]})\ndf["성별_encoded"] = df["성별"].map({"남": 0, "여": 1})\nprint(df["성별_encoded"])',
            },
            {
                "id": "derived-feature",
                "title": "조건으로 파생 변수 만들기",
                "explanation": "기존 컬럼에 조건을 적용해 새로운 의미를 가진 컬럼을 만들 수 있습니다. (조건).astype(int)로 True/False를 1/0으로 바꿀 수 있습니다.",
                "example_code": 'import pandas as pd\ndf = pd.DataFrame({"나이": [15, 25, 35]})\ndf["성인여부"] = (df["나이"] >= 19).astype(int)\nprint(df["성인여부"])',
            },
            {
                "id": "scaling",
                "title": "min-max 스케일링으로 값 범위 맞추기",
                "explanation": "(값 - 최솟값) / (최댓값 - 최솟값) 공식으로 모든 값을 0~1 사이로 맞출 수 있습니다. 값의 범위가 서로 다른 컬럼들을 비교하거나 함께 쓸 때 유용합니다.",
                "example_code": 'import pandas as pd\ndf = pd.DataFrame({"나이": [10, 20, 30]})\ndf["나이_scaled"] = (df["나이"] - df["나이"].min()) / (df["나이"].max() - df["나이"].min())\nprint(df["나이_scaled"])',
            },
        ],
        "problems": [
            {
                "id": "p1-encode-gender",
                "concept_id": "encoding",
                "prompt": '성별 ["남", "여", "남", "여"] 데이터를 만들고, 남=0, 여=1로 인코딩한 새 컬럼을 만들어 출력하세요.',
                "reference_code": 'import pandas as pd\ndf = pd.DataFrame({"성별": ["남", "여", "남", "여"]})\ndf["성별_encoded"] = df["성별"].map({"남": 0, "여": 1})\nprint(df["성별_encoded"])',
                "hints": [
                    "map()에 {\"원래값\": 바꿀값} 형태의 딕셔너리를 넘기면 됩니다.",
                    "df[\"성별\"].map({\"남\": 0, \"여\": 1})을 새 컬럼에 저장한 뒤 출력하세요.",
                    'import pandas as pd\ndf = pd.DataFrame({"성별": ["남", "여", "남", "여"]})\ndf["성별_encoded"] = df["성별"].map({"남": 0, "여": 1})\nprint(df["성별_encoded"])',
                ],
            },
            {
                "id": "p2-derived-adult",
                "concept_id": "derived-feature",
                "prompt": "나이 [15, 22, 17, 30] 데이터에서 19세 이상이면 1, 아니면 0인 성인여부 컬럼을 만들어 출력하세요.",
                "reference_code": 'import pandas as pd\ndf = pd.DataFrame({"나이": [15, 22, 17, 30]})\ndf["성인여부"] = (df["나이"] >= 19).astype(int)\nprint(df["성인여부"])',
                "hints": [
                    "df[\"나이\"] >= 19는 각 값이 조건을 만족하는지 True/False로 알려줍니다.",
                    ".astype(int)를 붙이면 True/False가 1/0으로 바뀝니다.",
                    'import pandas as pd\ndf = pd.DataFrame({"나이": [15, 22, 17, 30]})\ndf["성인여부"] = (df["나이"] >= 19).astype(int)\nprint(df["성인여부"])',
                ],
            },
            {
                "id": "p3-cut-bins",
                "concept_id": "derived-feature",
                "prompt": '나이 [5, 25, 45, 70] 데이터를 pd.cut()으로 [0, 18, 40, 100] 구간으로 나눠서 "소아", "성인", "중년" 라벨을 붙이고 출력하세요.',
                "reference_code": 'import pandas as pd\ndf = pd.DataFrame({"나이": [5, 25, 45, 70]})\ndf["연령대"] = pd.cut(df["나이"], bins=[0, 18, 40, 100], labels=["소아", "성인", "중년"])\nprint(df["연령대"])',
                "hints": [
                    "pd.cut(컬럼, bins=구간경계리스트, labels=라벨리스트) 형태로 사용합니다.",
                    "bins=[0, 18, 40, 100]은 0~18, 18~40, 40~100 세 구간을 의미합니다.",
                    'import pandas as pd\ndf = pd.DataFrame({"나이": [5, 25, 45, 70]})\ndf["연령대"] = pd.cut(df["나이"], bins=[0, 18, 40, 100], labels=["소아", "성인", "중년"])\nprint(df["연령대"])',
                ],
            },
            {
                "id": "p4-minmax-scale",
                "concept_id": "scaling",
                "prompt": "나이 [10, 20, 30, 40] 데이터를 min-max 방식으로 0~1 사이 값으로 변환해서 출력하세요.",
                "reference_code": 'import pandas as pd\ndf = pd.DataFrame({"나이": [10, 20, 30, 40]})\ndf["나이_scaled"] = (df["나이"] - df["나이"].min()) / (df["나이"].max() - df["나이"].min())\nprint(df["나이_scaled"])',
                "hints": [
                    "공식은 (값 - 최솟값) / (최댓값 - 최솟값) 입니다.",
                    "df[\"나이\"].min()과 df[\"나이\"].max()를 그대로 공식에 대입하세요.",
                    'import pandas as pd\ndf = pd.DataFrame({"나이": [10, 20, 30, 40]})\ndf["나이_scaled"] = (df["나이"] - df["나이"].min()) / (df["나이"].max() - df["나이"].min())\nprint(df["나이_scaled"])',
                ],
            },
            {
                "id": "p5-mini-preprocessing-pipeline",
                "concept_id": "encoding",
                "prompt": (
                    '성별 ["남", "여", "남", None], 나이 [15, 25, None, 35] 데이터에서 '
                    "1) 나이 결측치는 평균으로, 2) 성별 결측치는 '남'으로 채우고, "
                    "3) 성별을 남=0, 여=1로 인코딩한 최종 DataFrame을 출력하세요."
                ),
                "reference_code": (
                    'import pandas as pd\n'
                    'data = pd.DataFrame({"성별": ["남", "여", "남", None], "나이": [15, 25, None, 35]})\n'
                    'data["나이"] = data["나이"].fillna(data["나이"].mean())\n'
                    'data["성별"] = data["성별"].fillna("남")\n'
                    'data["성별_encoded"] = data["성별"].map({"남": 0, "여": 1})\n'
                    'print(data)'
                ),
                "hints": [
                    "결측치 채우기(fillna) 두 번, 그다음 인코딩(map) 순서로 진행하면 됩니다.",
                    "나이는 fillna(평균), 성별은 fillna(\"남\")으로 각각 채운 뒤 마지막에 인코딩 컬럼을 추가하세요.",
                    (
                        'import pandas as pd\n'
                        'data = pd.DataFrame({"성별": ["남", "여", "남", None], "나이": [15, 25, None, 35]})\n'
                        'data["나이"] = data["나이"].fillna(data["나이"].mean())\n'
                        'data["성별"] = data["성별"].fillna("남")\n'
                        'data["성별_encoded"] = data["성별"].map({"남": 0, "여": 1})\n'
                        'print(data)'
                    ),
                ],
            },
        ],
    },
    {
        "id": 19,
        "title": "베이스라인 모델링",
        "goal": "scikit-learn으로 첫 모델 학습·검증(train/valid split)",
        "concepts": [
            {
                "id": "train-test-split",
                "title": "train_test_split으로 데이터 나누기",
                "explanation": "모델이 처음 보는 데이터에서도 잘 맞히는지 확인하려면, 가진 데이터를 학습용과 검증용으로 미리 나눠둬야 합니다. random_state를 고정하면 항상 같은 방식으로 나뉩니다.",
                "example_code": 'from sklearn.model_selection import train_test_split\nX = [[1], [2], [3], [4], [5], [6]]\ny = [0, 0, 0, 1, 1, 1]\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)\nprint(len(X_train), len(X_test))',
            },
            {
                "id": "model-fit",
                "title": "모델 학습시키기 (fit)",
                "explanation": "LogisticRegression() 같은 모델을 만든 뒤 fit(X, y)를 호출하면 학습이 시작됩니다. 학습이 끝나면 predict()로 새 데이터의 결과를 예측할 수 있습니다.",
                "example_code": 'from sklearn.linear_model import LogisticRegression\nX_train = [[1], [2], [3], [7], [8], [9]]\ny_train = [0, 0, 0, 1, 1, 1]\nmodel = LogisticRegression()\nmodel.fit(X_train, y_train)\nprint(model.predict([[5]]))',
            },
            {
                "id": "accuracy",
                "title": "정확도 평가하기 (accuracy_score)",
                "explanation": "accuracy_score(정답, 예측)으로 전체 중 몇 %를 맞혔는지 확인할 수 있습니다. 모델의 성능을 숫자로 비교할 때 가장 기본이 되는 지표입니다.",
                "example_code": 'from sklearn.metrics import accuracy_score\ny_true = [0, 1, 1, 0]\ny_pred = [0, 1, 0, 0]\nprint(accuracy_score(y_true, y_pred))',
            },
        ],
        "problems": [
            {
                "id": "p1-split-sizes",
                "concept_id": "train-test-split",
                "prompt": "X = [[1]~[10]] (10개), y = [0,0,0,0,0,1,1,1,1,1] 데이터를 test_size=0.2, random_state=42로 나누고, 학습용/검증용 크기를 각각 출력하세요.",
                "reference_code": (
                    'from sklearn.model_selection import train_test_split\n'
                    'X = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]\n'
                    'y = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]\n'
                    'X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n'
                    'print(len(X_train), len(X_test))'
                ),
                "hints": [
                    "train_test_split(X, y, test_size=0.2, random_state=42)로 나눌 수 있습니다.",
                    "결과로 X_train, X_test, y_train, y_test 네 개가 순서대로 나옵니다. len()으로 각 크기를 출력하세요.",
                    (
                        'from sklearn.model_selection import train_test_split\n'
                        'X = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]\n'
                        'y = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]\n'
                        'X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n'
                        'print(len(X_train), len(X_test))'
                    ),
                ],
            },
            {
                "id": "p2-fit-predict",
                "concept_id": "model-fit",
                "prompt": "X_train = [[1],[2],[3],[8],[9],[10]], y_train = [0,0,0,1,1,1]로 LogisticRegression 모델을 학습시키고, [[5]]를 예측한 결과를 출력하세요.",
                "reference_code": (
                    'from sklearn.linear_model import LogisticRegression\n'
                    'X_train = [[1], [2], [3], [8], [9], [10]]\n'
                    'y_train = [0, 0, 0, 1, 1, 1]\n'
                    'model = LogisticRegression()\n'
                    'model.fit(X_train, y_train)\n'
                    'print(model.predict([[5]]))'
                ),
                "hints": [
                    "model = LogisticRegression() 으로 모델을 만들고 model.fit(X_train, y_train)으로 학습시키세요.",
                    "model.predict([[5]])처럼 새로운 값을 리스트 안의 리스트로 넘겨서 예측하세요.",
                    (
                        'from sklearn.linear_model import LogisticRegression\n'
                        'X_train = [[1], [2], [3], [8], [9], [10]]\n'
                        'y_train = [0, 0, 0, 1, 1, 1]\n'
                        'model = LogisticRegression()\n'
                        'model.fit(X_train, y_train)\n'
                        'print(model.predict([[5]]))'
                    ),
                ],
            },
            {
                "id": "p3-accuracy-score",
                "concept_id": "accuracy",
                "prompt": "정답 y_true = [0, 1, 1, 0, 1]과 예측 y_pred = [0, 1, 0, 0, 1]의 정확도(accuracy)를 출력하세요.",
                "reference_code": (
                    'from sklearn.metrics import accuracy_score\n'
                    'y_true = [0, 1, 1, 0, 1]\n'
                    'y_pred = [0, 1, 0, 0, 1]\n'
                    'print(accuracy_score(y_true, y_pred))'
                ),
                "hints": [
                    "accuracy_score(정답, 예측) 형태로 순서에 주의해서 넘기세요.",
                    "print(accuracy_score(y_true, y_pred))를 그대로 써보세요.",
                    (
                        'from sklearn.metrics import accuracy_score\n'
                        'y_true = [0, 1, 1, 0, 1]\n'
                        'y_pred = [0, 1, 0, 0, 1]\n'
                        'print(accuracy_score(y_true, y_pred))'
                    ),
                ],
            },
            {
                "id": "p4-train-accuracy",
                "concept_id": "model-fit",
                "prompt": "X_train = [[1],[2],[3],[8],[9],[10]], y_train = [0,0,0,1,1,1]로 모델을 학습시킨 뒤, 학습 데이터 자체에 대한 정확도를 출력하세요.",
                "reference_code": (
                    'from sklearn.linear_model import LogisticRegression\n'
                    'from sklearn.metrics import accuracy_score\n'
                    'X_train = [[1], [2], [3], [8], [9], [10]]\n'
                    'y_train = [0, 0, 0, 1, 1, 1]\n'
                    'model = LogisticRegression()\n'
                    'model.fit(X_train, y_train)\n'
                    'pred = model.predict(X_train)\n'
                    'print(accuracy_score(y_train, pred))'
                ),
                "hints": [
                    "학습에 쓴 X_train을 그대로 predict()에 다시 넣어보세요.",
                    "예측 결과와 y_train을 accuracy_score로 비교하세요.",
                    (
                        'from sklearn.linear_model import LogisticRegression\n'
                        'from sklearn.metrics import accuracy_score\n'
                        'X_train = [[1], [2], [3], [8], [9], [10]]\n'
                        'y_train = [0, 0, 0, 1, 1, 1]\n'
                        'model = LogisticRegression()\n'
                        'model.fit(X_train, y_train)\n'
                        'pred = model.predict(X_train)\n'
                        'print(accuracy_score(y_train, pred))'
                    ),
                ],
            },
            {
                "id": "p5-mini-baseline-pipeline",
                "concept_id": "train-test-split",
                "prompt": (
                    "X = [[1]~[10]] (10개), y = [0,0,0,0,0,1,1,1,1,1] 데이터를 test_size=0.3, random_state=42로 나누고, "
                    'LogisticRegression을 학습시켜 검증 데이터에 대한 정확도를 "정확도: N" 형식으로 출력하세요.'
                ),
                "reference_code": (
                    'from sklearn.model_selection import train_test_split\n'
                    'from sklearn.linear_model import LogisticRegression\n'
                    'from sklearn.metrics import accuracy_score\n'
                    'X = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]\n'
                    'y = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]\n'
                    'X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)\n'
                    'model = LogisticRegression()\n'
                    'model.fit(X_train, y_train)\n'
                    'pred = model.predict(X_test)\n'
                    'print("정확도:", accuracy_score(y_test, pred))'
                ),
                "hints": [
                    "지금까지 배운 세 단계(나누기 → 학습 → 평가)를 순서대로 이어 붙이면 됩니다.",
                    "검증에는 X_test/y_test를 쓴다는 점에 주의하세요 — 학습에 쓴 데이터로 평가하면 안 됩니다.",
                    (
                        'from sklearn.model_selection import train_test_split\n'
                        'from sklearn.linear_model import LogisticRegression\n'
                        'from sklearn.metrics import accuracy_score\n'
                        'X = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]\n'
                        'y = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]\n'
                        'X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)\n'
                        'model = LogisticRegression()\n'
                        'model.fit(X_train, y_train)\n'
                        'pred = model.predict(X_test)\n'
                        'print("정확도:", accuracy_score(y_test, pred))'
                    ),
                ],
            },
        ],
    },
    {
        "id": 20,
        "title": "제출과 개선 루프",
        "goal": "리더보드 점수 해석, 실험 기록, 다음 개선 아이디어 도출",
        "concepts": [
            {
                "id": "compare-experiments",
                "title": "여러 설정을 비교해서 더 나은 걸 고르기",
                "explanation": "모델의 파라미터(예: C 값)를 바꿔가며 정확도를 비교하면, 어떤 설정이 더 나은지 실험으로 확인할 수 있습니다. 감이 아니라 숫자로 비교하는 습관이 중요합니다.",
                "example_code": (
                    'from sklearn.linear_model import LogisticRegression\n'
                    'from sklearn.metrics import accuracy_score\n'
                    'X_train = [[1], [2], [8], [9]]\n'
                    'y_train = [0, 0, 1, 1]\n'
                    'model = LogisticRegression(C=1.0)\n'
                    'model.fit(X_train, y_train)\n'
                    'print(accuracy_score(y_train, model.predict(X_train)))'
                ),
            },
            {
                "id": "record-experiments",
                "title": "실험 결과 기록하기",
                "explanation": "실험할 때마다 결과를 딕셔너리나 리스트에 남겨두면, 나중에 어떤 설정이 가장 좋았는지 쉽게 비교할 수 있습니다.",
                "example_code": 'results = {"C=0.1": 0.8, "C=10": 0.9}\nbest = max(results, key=results.get)\nprint(best, results[best])',
            },
            {
                "id": "validate-submission",
                "title": "제출 파일 형식 검증하기",
                "explanation": "제출하기 전에 컬럼 이름과 행 개수가 요구사항과 맞는지 코드로 미리 확인하면, Kaggle에 잘못된 형식을 제출하는 실수를 줄일 수 있습니다.",
                "example_code": (
                    'import pandas as pd\n'
                    'sub = pd.DataFrame({"id": [1, 2, 3], "target": [0, 1, 0]})\n'
                    'print(list(sub.columns) == ["id", "target"])'
                ),
            },
        ],
        "problems": [
            {
                "id": "p1-compare-c",
                "concept_id": "compare-experiments",
                "prompt": (
                    "X_train=[[1],[2],[3],[8],[9],[10]], y_train=[0,0,0,1,1,1], X_test=[[2],[9]], y_test=[0,1]로 "
                    "C=0.1과 C=10 두 모델을 각각 학습·평가해서 정확도를 비교 출력하세요."
                ),
                "reference_code": (
                    'from sklearn.linear_model import LogisticRegression\n'
                    'from sklearn.metrics import accuracy_score\n'
                    'X_train = [[1], [2], [3], [8], [9], [10]]\n'
                    'y_train = [0, 0, 0, 1, 1, 1]\n'
                    'X_test = [[2], [9]]\n'
                    'y_test = [0, 1]\n'
                    'model_a = LogisticRegression(C=0.1)\n'
                    'model_a.fit(X_train, y_train)\n'
                    'acc_a = accuracy_score(y_test, model_a.predict(X_test))\n'
                    'model_b = LogisticRegression(C=10)\n'
                    'model_b.fit(X_train, y_train)\n'
                    'acc_b = accuracy_score(y_test, model_b.predict(X_test))\n'
                    'print("C=0.1:", acc_a)\n'
                    'print("C=10:", acc_b)'
                ),
                "hints": [
                    "LogisticRegression(C=값)처럼 파라미터를 다르게 준 모델을 두 개 만드세요.",
                    "각각 학습·예측·정확도 계산까지 똑같은 과정을 반복하면 됩니다.",
                    (
                        'from sklearn.linear_model import LogisticRegression\n'
                        'from sklearn.metrics import accuracy_score\n'
                        'X_train = [[1], [2], [3], [8], [9], [10]]\n'
                        'y_train = [0, 0, 0, 1, 1, 1]\n'
                        'X_test = [[2], [9]]\n'
                        'y_test = [0, 1]\n'
                        'model_a = LogisticRegression(C=0.1)\n'
                        'model_a.fit(X_train, y_train)\n'
                        'acc_a = accuracy_score(y_test, model_a.predict(X_test))\n'
                        'model_b = LogisticRegression(C=10)\n'
                        'model_b.fit(X_train, y_train)\n'
                        'acc_b = accuracy_score(y_test, model_b.predict(X_test))\n'
                        'print("C=0.1:", acc_a)\n'
                        'print("C=10:", acc_b)'
                    ),
                ],
            },
            {
                "id": "p2-best-experiment",
                "concept_id": "record-experiments",
                "prompt": '실험 결과 {"C=0.1": 0.8, "C=10": 0.9, "C=1": 0.85}에서 가장 높은 정확도를 낸 설정 이름과 값을 출력하세요.',
                "reference_code": 'results = {"C=0.1": 0.8, "C=10": 0.9, "C=1": 0.85}\nbest = max(results, key=results.get)\nprint(best, results[best])',
                "hints": [
                    "max(딕셔너리, key=딕셔너리.get)을 쓰면 값이 가장 큰 키를 찾을 수 있습니다.",
                    "찾은 키(best)와 그 값(results[best])을 함께 출력하세요.",
                    'results = {"C=0.1": 0.8, "C=10": 0.9, "C=1": 0.85}\nbest = max(results, key=results.get)\nprint(best, results[best])',
                ],
            },
            {
                "id": "p3-validate-submission",
                "concept_id": "validate-submission",
                "prompt": "id [1, 2, 3], target [0, 1, 0]로 제출 파일을 만들고, 컬럼이 정확히 [id, target]이면서 행이 3개인지 확인한 결과(True/False)를 출력하세요.",
                "reference_code": (
                    'import pandas as pd\n'
                    'sub = pd.DataFrame({"id": [1, 2, 3], "target": [0, 1, 0]})\n'
                    'has_correct_columns = list(sub.columns) == ["id", "target"]\n'
                    'has_correct_rows = len(sub) == 3\n'
                    'print(has_correct_columns and has_correct_rows)'
                ),
                "hints": [
                    "list(sub.columns)로 컬럼 이름 목록을 뽑아서 원하는 목록과 비교할 수 있습니다.",
                    "두 조건(컬럼, 행 개수)을 and로 함께 검사하세요.",
                    (
                        'import pandas as pd\n'
                        'sub = pd.DataFrame({"id": [1, 2, 3], "target": [0, 1, 0]})\n'
                        'has_correct_columns = list(sub.columns) == ["id", "target"]\n'
                        'has_correct_rows = len(sub) == 3\n'
                        'print(has_correct_columns and has_correct_rows)'
                    ),
                ],
            },
            {
                "id": "p4-best-score-index",
                "concept_id": "record-experiments",
                "prompt": '실험 점수 리스트 [0.75, 0.82, 0.79, 0.85]에서 가장 높은 점수와 몇 번째 실험이었는지를 "최고 점수: N", "N번째 실험" 형식으로 출력하세요.',
                "reference_code": (
                    'scores = [0.75, 0.82, 0.79, 0.85]\n'
                    'best_score = max(scores)\n'
                    'best_index = scores.index(best_score) + 1\n'
                    'print("최고 점수:", best_score)\n'
                    'print(str(best_index) + "번째 실험")'
                ),
                "hints": [
                    "max(리스트)로 가장 큰 값을, .index(값)으로 그 값의 위치(0부터 시작)를 알 수 있습니다.",
                    "몇 '번째'는 사람이 세는 방식이라 인덱스에 1을 더해야 합니다.",
                    (
                        'scores = [0.75, 0.82, 0.79, 0.85]\n'
                        'best_score = max(scores)\n'
                        'best_index = scores.index(best_score) + 1\n'
                        'print("최고 점수:", best_score)\n'
                        'print(str(best_index) + "번째 실험")'
                    ),
                ],
            },
            {
                "id": "p5-mini-improvement-loop",
                "concept_id": "compare-experiments",
                "prompt": (
                    "y_test=[0,0,1,1,1]에 대해, 모두 1로 예측하는 베이스라인의 정확도와, "
                    "X_train=[[1],[2],[8],[9],[10]]/y_train=[0,0,1,1,1]로 학습한 모델이 같은 X_test에 대해 낸 정확도를 "
                    '각각 "베이스라인 정확도: N", "모델 정확도: N" 형식으로 출력하세요.'
                ),
                "reference_code": (
                    'from sklearn.linear_model import LogisticRegression\n'
                    'from sklearn.metrics import accuracy_score\n'
                    'y_test = [0, 0, 1, 1, 1]\n'
                    'baseline_pred = [1, 1, 1, 1, 1]\n'
                    'baseline_acc = accuracy_score(y_test, baseline_pred)\n'
                    '\n'
                    'X_train = [[1], [2], [8], [9], [10]]\n'
                    'y_train = [0, 0, 1, 1, 1]\n'
                    'X_test = [[1], [2], [8], [9], [10]]\n'
                    'model = LogisticRegression()\n'
                    'model.fit(X_train, y_train)\n'
                    'model_acc = accuracy_score(y_test, model.predict(X_test))\n'
                    '\n'
                    'print("베이스라인 정확도:", baseline_acc)\n'
                    'print("모델 정확도:", model_acc)'
                ),
                "hints": [
                    "베이스라인은 학습 없이 정답과 미리 정해둔 예측값을 그냥 비교하면 됩니다.",
                    "모델은 지금까지처럼 학습(fit) 후 predict로 예측한 값을 정답과 비교하세요.",
                    (
                        'from sklearn.linear_model import LogisticRegression\n'
                        'from sklearn.metrics import accuracy_score\n'
                        'y_test = [0, 0, 1, 1, 1]\n'
                        'baseline_pred = [1, 1, 1, 1, 1]\n'
                        'baseline_acc = accuracy_score(y_test, baseline_pred)\n'
                        '\n'
                        'X_train = [[1], [2], [8], [9], [10]]\n'
                        'y_train = [0, 0, 1, 1, 1]\n'
                        'X_test = [[1], [2], [8], [9], [10]]\n'
                        'model = LogisticRegression()\n'
                        'model.fit(X_train, y_train)\n'
                        'model_acc = accuracy_score(y_test, model.predict(X_test))\n'
                        '\n'
                        'print("베이스라인 정확도:", baseline_acc)\n'
                        'print("모델 정확도:", model_acc)'
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
