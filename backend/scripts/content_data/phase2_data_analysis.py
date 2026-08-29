"""Phase 2 — numpy / pandas 확장 (레벨 17~23).

실제 수강한 데이터 분석 강의(course_Data_Analysis)를 참고해서, 기존
콘텐츠에 빠져 있던 2차원 배열과 pandas .loc/.iloc 인덱싱을 새 레벨로
추가했다.
"""

LEVELS = [
    {
        "id": 17,
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
        "id": 18,
        "title": "numpy 2차원 배열",
        "goal": "행렬 형태의 배열 생성, 인덱싱, 특수 배열",
        "concepts": [
            {
                "id": "2d-array-basics",
                "title": "2차원 배열 만들기",
                "explanation": "리스트 안에 리스트를 넣으면 행(row)과 열(column)을 가진 2차원 배열(행렬)이 됩니다. shape은 (행 개수, 열 개수)를 알려줍니다.",
                "example_code": "import numpy as np\narr = np.array([[1, 2, 3], [4, 5, 6]])\nprint(arr.shape)",
            },
            {
                "id": "2d-indexing",
                "title": "2차원 배열 인덱싱",
                "explanation": "arr[행, 열]로 특정 위치의 값을, arr[행, :]으로 한 행 전체를 꺼낼 수 있습니다.",
                "example_code": "import numpy as np\narr = np.array([[1, 2, 3], [4, 5, 6]])\nprint(arr[0, 1])",
            },
            {
                "id": "special-arrays",
                "title": "특수한 배열 생성하기",
                "explanation": "np.zeros(모양)은 0으로, np.ones(모양)은 1로 채워진 배열을 만듭니다. np.eye(n)은 대각선만 1인 단위행렬을 만듭니다.",
                "example_code": "import numpy as np\nprint(np.zeros((2, 3)))",
            },
        ],
        "problems": [
            {
                "id": "p1-2d-shape",
                "concept_id": "2d-array-basics",
                "prompt": "[[1, 2, 3], [4, 5, 6]] 리스트로 2차원 배열을 만들고 shape을 출력하세요.",
                "reference_code": "import numpy as np\narr = np.array([[1, 2, 3], [4, 5, 6]])\nprint(arr.shape)",
                "hints": [
                    "리스트 안에 리스트를 넣으면 2차원 배열이 만들어집니다.",
                    "arr.shape를 출력해보세요.",
                    "import numpy as np\narr = np.array([[1, 2, 3], [4, 5, 6]])\nprint(arr.shape)",
                ],
            },
            {
                "id": "p2-2d-index",
                "concept_id": "2d-indexing",
                "prompt": "위와 같은 배열에서 첫 번째 행, 두 번째 열의 값(2)을 인덱싱으로 출력하세요.",
                "reference_code": "import numpy as np\narr = np.array([[1, 2, 3], [4, 5, 6]])\nprint(arr[0, 1])",
                "hints": [
                    "2차원 배열은 arr[행, 열] 형태로 콤마를 사용해 접근합니다.",
                    "arr[0, 1]을 출력해보세요.",
                    "import numpy as np\narr = np.array([[1, 2, 3], [4, 5, 6]])\nprint(arr[0, 1])",
                ],
            },
            {
                "id": "p3-2d-row",
                "concept_id": "2d-indexing",
                "prompt": "위와 같은 배열에서 첫 번째 행 전체를 출력하세요.",
                "reference_code": "import numpy as np\narr = np.array([[1, 2, 3], [4, 5, 6]])\nprint(arr[0, :])",
                "hints": [
                    "행은 그대로 두고 열 자리에 : 을 쓰면 그 행 전체를 가져옵니다.",
                    "arr[0, :]을 출력해보세요.",
                    "import numpy as np\narr = np.array([[1, 2, 3], [4, 5, 6]])\nprint(arr[0, :])",
                ],
            },
            {
                "id": "p4-zeros",
                "concept_id": "special-arrays",
                "prompt": "2행 3열 크기의 0으로 채워진 배열을 만들어 출력하세요.",
                "reference_code": "import numpy as np\nprint(np.zeros((2, 3)))",
                "hints": [
                    "np.zeros((행, 열)) 형태로 크기를 튜플로 넘깁니다.",
                    "np.zeros((2, 3))을 출력해보세요.",
                    "import numpy as np\nprint(np.zeros((2, 3)))",
                ],
            },
            {
                "id": "p5-mini-identity",
                "concept_id": "special-arrays",
                "prompt": "3x3 단위행렬(대각선만 1)을 np.eye()로 만들어 출력하세요.",
                "reference_code": "import numpy as np\nprint(np.eye(3))",
                "hints": [
                    "단위행렬을 만드는 함수 이름을 떠올려 보세요 (eye).",
                    "np.eye(3)을 출력해보세요.",
                    "import numpy as np\nprint(np.eye(3))",
                ],
            },
        ],
    },
    {
        "id": 19,
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
            {
                "id": "axis-aggregation",
                "title": "axis로 방향을 지정한 집계",
                "explanation": "2차원 배열에서 axis=0은 열(세로) 방향으로, axis=1은 행(가로) 방향으로 계산합니다.",
                "example_code": "import numpy as np\narr = np.array([[1, 2, 3], [4, 5, 6]])\nprint(arr.sum(axis=0))\nprint(arr.sum(axis=1))",
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
                "id": "p2-array-plus-array",
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
                "id": "p3-filter",
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
                "id": "p4-axis-sum",
                "concept_id": "axis-aggregation",
                "prompt": "[[1, 2, 3], [4, 5, 6]] 배열에서 각 열의 합(axis=0)과 각 행의 합(axis=1)을 순서대로 출력하세요.",
                "reference_code": "import numpy as np\narr = np.array([[1, 2, 3], [4, 5, 6]])\nprint(arr.sum(axis=0))\nprint(arr.sum(axis=1))",
                "hints": [
                    "axis=0은 세로(열) 방향, axis=1은 가로(행) 방향으로 계산합니다.",
                    "arr.sum(axis=0)과 arr.sum(axis=1)을 순서대로 출력하세요.",
                    "import numpy as np\narr = np.array([[1, 2, 3], [4, 5, 6]])\nprint(arr.sum(axis=0))\nprint(arr.sum(axis=1))",
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
        "id": 20,
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
                "explanation": 'DataFrame은 여러 열(컬럼)로 이루어진 표입니다. pd.DataFrame({"컬럼": [값들]})로 만들고, df["컬럼"]으로 원하는 열만 꺼낼 수 있습니다.',
                "example_code": 'import pandas as pd\ndata = {"이름": ["철수", "영희"], "점수": [90, 85]}\ndf = pd.DataFrame(data)\nprint(df["점수"])',
            },
            {
                "id": "dataframe-filter",
                "title": "조건으로 행 선택하기",
                "explanation": 'df[df["컬럼"] > 값] 형태로 조건을 만족하는 행만 골라낼 수 있습니다. numpy 배열 필터링과 같은 원리입니다.',
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
                    '딕셔너리 {"컬럼명": [값들]} 형태로 pd.DataFrame()에 전달하세요.',
                    'df["점수"]로 점수 컬럼만 꺼낼 수 있습니다.',
                    'import pandas as pd\ndata = {"이름": ["철수", "영희", "민수"], "점수": [90, 85, 95]}\ndf = pd.DataFrame(data)\nprint(df["점수"])',
                ],
            },
            {
                "id": "p3-first-row-value",
                "concept_id": "dataframe-basics",
                "prompt": "위와 같은 DataFrame에서 첫 번째 사람의 이름을 출력하세요.",
                "reference_code": 'import pandas as pd\ndata = {"이름": ["철수", "영희", "민수"], "점수": [90, 85, 95]}\ndf = pd.DataFrame(data)\nprint(df["이름"][0])',
                "hints": [
                    '먼저 df["이름"]으로 이름 컬럼(Series)을 꺼내세요.',
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
                    'df["점수"] >= 90은 각 행이 조건을 만족하는지 알려주는 True/False 목록입니다.',
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
                    '먼저 조건으로 행을 필터링한 뒤, 그 결과에서 다시 ["상품"] 컬럼만 꺼내면 됩니다.',
                    'df[df["수량"] >= 6]["상품"] 처럼 대괄호를 두 번 이어서 쓸 수 있습니다.',
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
        "id": 21,
        "title": "pandas 인덱싱: loc와 iloc",
        "goal": ".loc/.iloc로 행과 열을 정확히 선택하고, 다중 조건으로 필터링하기",
        "concepts": [
            {
                "id": "iloc",
                "title": "iloc — 정수 위치로 선택하기",
                "explanation": "iloc는 순서(정수 위치)로 행이나 열을 선택합니다. 리스트 인덱싱과 비슷하게 0부터 시작합니다.",
                "example_code": 'import pandas as pd\ndf = pd.DataFrame({"이름": ["철수", "영희", "민수"], "점수": [90, 85, 95]})\nprint(df.iloc[1])',
            },
            {
                "id": "loc",
                "title": "loc — 라벨(이름)로 선택하기",
                "explanation": "loc는 인덱스 라벨이나 컬럼 이름으로 선택합니다. df.loc[행라벨, 컬럼이름] 형태로 행과 열을 동시에 지정할 수 있습니다.",
                "example_code": 'import pandas as pd\ndf = pd.DataFrame({"이름": ["철수", "영희", "민수"], "점수": [90, 85, 95]})\nprint(df.loc[0, "이름"])',
            },
            {
                "id": "multi-condition-mask",
                "title": "다중 조건 마스킹",
                "explanation": "&(and), |(or), ~(not)로 여러 조건을 조합할 수 있습니다. 각 조건은 반드시 괄호로 감싸야 합니다.",
                "example_code": (
                    'import pandas as pd\n'
                    'df = pd.DataFrame({"점수": [90, 85, 95, 70], "나이": [22, 35, 28, 40]})\n'
                    'mask = (df["점수"] >= 80) & (df["나이"] < 30)\n'
                    'print(df[mask])'
                ),
            },
        ],
        "problems": [
            {
                "id": "p1-iloc-row",
                "concept_id": "iloc",
                "prompt": '이름 ["철수", "영희", "민수"]과 점수 [90, 85, 95]로 DataFrame을 만들고, iloc[1]로 두 번째 행을 출력하세요.',
                "reference_code": 'import pandas as pd\ndf = pd.DataFrame({"이름": ["철수", "영희", "민수"], "점수": [90, 85, 95]})\nprint(df.iloc[1])',
                "hints": [
                    "iloc는 순서(정수 위치)로 행을 선택합니다. 인덱스는 0부터 시작합니다.",
                    "df.iloc[1]을 출력해보세요.",
                    'import pandas as pd\ndf = pd.DataFrame({"이름": ["철수", "영희", "민수"], "점수": [90, 85, 95]})\nprint(df.iloc[1])',
                ],
            },
            {
                "id": "p2-loc-cell",
                "concept_id": "loc",
                "prompt": "위와 같은 DataFrame에서 loc를 사용해 인덱스 0의 '이름' 값을 출력하세요.",
                "reference_code": 'import pandas as pd\ndf = pd.DataFrame({"이름": ["철수", "영희", "민수"], "점수": [90, 85, 95]})\nprint(df.loc[0, "이름"])',
                "hints": [
                    "loc[행라벨, 컬럼이름] 형태로 특정 칸을 콕 집어 선택할 수 있습니다.",
                    'df.loc[0, "이름"]을 출력해보세요.',
                    'import pandas as pd\ndf = pd.DataFrame({"이름": ["철수", "영희", "민수"], "점수": [90, 85, 95]})\nprint(df.loc[0, "이름"])',
                ],
            },
            {
                "id": "p3-iloc-slice",
                "concept_id": "iloc",
                "prompt": "위와 같은 DataFrame에서 iloc로 첫 두 행, 첫 번째 컬럼만 선택해서 출력하세요.",
                "reference_code": 'import pandas as pd\ndf = pd.DataFrame({"이름": ["철수", "영희", "민수"], "점수": [90, 85, 95]})\nprint(df.iloc[:2, :1])',
                "hints": [
                    "iloc도 슬라이싱을 지원합니다: df.iloc[행범위, 열범위].",
                    "df.iloc[:2, :1]을 출력해보세요.",
                    'import pandas as pd\ndf = pd.DataFrame({"이름": ["철수", "영희", "민수"], "점수": [90, 85, 95]})\nprint(df.iloc[:2, :1])',
                ],
            },
            {
                "id": "p4-and-mask",
                "concept_id": "multi-condition-mask",
                "prompt": "점수 [90, 85, 95, 70], 나이 [22, 35, 28, 40]로 DataFrame을 만들고, 점수가 80 이상이면서 동시에 나이가 30 미만인 행만 출력하세요.",
                "reference_code": (
                    'import pandas as pd\n'
                    'df = pd.DataFrame({"점수": [90, 85, 95, 70], "나이": [22, 35, 28, 40]})\n'
                    'mask = (df["점수"] >= 80) & (df["나이"] < 30)\n'
                    'print(df[mask])'
                ),
                "hints": [
                    "두 조건을 모두 만족해야 하니 &(and)를 사용하세요.",
                    "각 조건은 괄호로 감싸야 합니다: (조건1) & (조건2)",
                    (
                        'import pandas as pd\n'
                        'df = pd.DataFrame({"점수": [90, 85, 95, 70], "나이": [22, 35, 28, 40]})\n'
                        'mask = (df["점수"] >= 80) & (df["나이"] < 30)\n'
                        'print(df[mask])'
                    ),
                ],
            },
            {
                "id": "p5-mini-or-mask",
                "concept_id": "multi-condition-mask",
                "prompt": "위와 같은 데이터에서 점수가 80 미만이거나 나이가 35 이상인 행을 출력하세요.",
                "reference_code": (
                    'import pandas as pd\n'
                    'df = pd.DataFrame({"점수": [90, 85, 95, 70], "나이": [22, 35, 28, 40]})\n'
                    'mask = (df["점수"] < 80) | (df["나이"] >= 35)\n'
                    'print(df[mask])'
                ),
                "hints": [
                    "둘 중 하나만 만족해도 되니 |(or)를 사용하세요.",
                    "(df[\"점수\"] < 80) | (df[\"나이\"] >= 35) 형태로 작성하세요.",
                    (
                        'import pandas as pd\n'
                        'df = pd.DataFrame({"점수": [90, 85, 95, 70], "나이": [22, 35, 28, 40]})\n'
                        'mask = (df["점수"] < 80) | (df["나이"] >= 35)\n'
                        'print(df[mask])'
                    ),
                ],
            },
        ],
    },
    {
        "id": 22,
        "title": "pandas 데이터 정제",
        "goal": "결측치·중복 처리, groupby, 정렬, isin",
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
                "explanation": 'groupby("컬럼")으로 같은 값끼리 묶은 뒤 sum(), mean() 등을 붙이면 그룹별 통계를 구할 수 있습니다.',
                "example_code": 'import pandas as pd\ndata = {"분류": ["A", "A", "B"], "수량": [10, 20, 5]}\ndf = pd.DataFrame(data)\nprint(df.groupby("분류")["수량"].sum())',
            },
            {
                "id": "sort-values",
                "title": "sort_values로 정렬하기",
                "explanation": 'sort_values("컬럼")으로 특정 컬럼 기준 오름차순 정렬을, ascending=False를 추가하면 내림차순 정렬을 할 수 있습니다.',
                "example_code": 'import pandas as pd\ndata = {"이름": ["철수", "영희"], "점수": [70, 95]}\ndf = pd.DataFrame(data)\nprint(df.sort_values("점수", ascending=False)["이름"])',
            },
            {
                "id": "isin",
                "title": "isin()으로 여러 값 중 하나인지 확인하기",
                "explanation": "컬럼.isin([값1, 값2, ...])는 그 컬럼의 값이 목록 중 하나와 일치하는지 True/False로 알려줍니다.",
                "example_code": 'import pandas as pd\ns = pd.Series(["사과", "바나나", "포도"])\nprint(s.isin(["사과", "포도"]))',
            },
        ],
        "problems": [
            {
                "id": "p1-count-missing",
                "concept_id": "missing-values",
                "prompt": "점수 [90, None, 95]로 Series를 만들고, 결측치(빈 값)가 몇 개인지 출력하세요.",
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
                    'groupby("분류")로 같은 분류끼리 묶을 수 있습니다.',
                    '묶은 뒤 ["수량"].sum()을 이어 붙이면 분류별 합계가 나옵니다.',
                    'import pandas as pd\ndata = {"분류": ["과일", "과일", "채소"], "수량": [10, 20, 5]}\ndf = pd.DataFrame(data)\nprint(df.groupby("분류")["수량"].sum())',
                ],
            },
            {
                "id": "p4-sort-values",
                "concept_id": "sort-values",
                "prompt": '이름 ["철수", "영희", "민수"]과 점수 [70, 95, 85]로 DataFrame을 만들고, 점수가 높은 순서대로 이름만 출력하세요.',
                "reference_code": 'import pandas as pd\ndata = {"이름": ["철수", "영희", "민수"], "점수": [70, 95, 85]}\ndf = pd.DataFrame(data)\nsorted_df = df.sort_values("점수", ascending=False)\nprint(sorted_df["이름"])',
                "hints": [
                    'sort_values("점수", ascending=False)로 점수를 내림차순 정렬할 수 있습니다.',
                    '정렬한 결과를 변수에 저장한 뒤, 그 결과에서 ["이름"]을 출력하세요.',
                    'import pandas as pd\ndata = {"이름": ["철수", "영희", "민수"], "점수": [70, 95, 85]}\ndf = pd.DataFrame(data)\nsorted_df = df.sort_values("점수", ascending=False)\nprint(sorted_df["이름"])',
                ],
            },
            {
                "id": "p5-mini-isin",
                "concept_id": "isin",
                "prompt": '과일 ["사과", "바나나", "포도", "오렌지"] 컬럼에서 "사과" 또는 "포도"인 행만 isin()으로 필터링해서 출력하세요.',
                "reference_code": 'import pandas as pd\ndf = pd.DataFrame({"과일": ["사과", "바나나", "포도", "오렌지"]})\nmask = df["과일"].isin(["사과", "포도"])\nprint(df[mask])',
                "hints": [
                    '컬럼.isin([값1, 값2])로 목록에 포함된 값인지 한 번에 확인할 수 있습니다.',
                    'df[df["과일"].isin(["사과", "포도"])] 형태로 필터링하세요.',
                    'import pandas as pd\ndf = pd.DataFrame({"과일": ["사과", "바나나", "포도", "오렌지"]})\nmask = df["과일"].isin(["사과", "포도"])\nprint(df[mask])',
                ],
            },
        ],
    },
    {
        "id": 23,
        "title": "데이터 탐색과 요약 통계",
        "goal": "describe·value_counts·agg로 분포·추세 파악하기",
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
                "explanation": 'agg(["mean", "max", "min"])처럼 원하는 통계 함수 이름을 리스트로 넘기면, 여러 결과를 한 번에 계산해줍니다.',
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
                    'describe()의 결과도 Series라서 ["mean"]처럼 이름으로 값을 꺼낼 수 있습니다.',
                    's.describe()["mean"]을 출력해보세요.',
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
                "prompt": '점수 [70, 85, 90, 60, 95, 100]으로 Series를 만들고, 평균·최댓값·최솟값을 agg(["mean", "max", "min"])으로 한 번에 계산해서 출력하세요.',
                "reference_code": 'import pandas as pd\ns = pd.Series([70, 85, 90, 60, 95, 100])\nprint(s.agg(["mean", "max", "min"]))',
                "hints": [
                    "agg()에 원하는 통계 함수 이름을 문자열 리스트로 넘기면 한 번에 계산됩니다.",
                    's.agg(["mean", "max", "min"])을 출력해보세요.',
                    'import pandas as pd\ns = pd.Series([70, 85, 90, 60, 95, 100])\nprint(s.agg(["mean", "max", "min"]))',
                ],
            },
        ],
    },
]
