"""Phase 3 — Kaggle 경진대회 준비 (레벨 24~28)."""

LEVELS = [
    {
        "id": 24,
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
        "id": 25,
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
        "id": 26,
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
        "id": 27,
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
        "id": 28,
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
