# PyCoach

파이썬 개인 코칭 학습 앱. 기획 배경과 로드맵은 [pycoach-project-plan.md](./pycoach-project-plan.md) 참고.

## 구조

```text
backend/   FastAPI 서버
frontend/  React + Vite + TypeScript 클라이언트
```

## 실행 방법

### 백엔드 (터미널 1)

```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

`http://localhost:8000/api/hello` 에서 응답을 확인할 수 있습니다.

AI 코치 기능을 쓰려면 `backend/.env.example`을 `backend/.env`로 복사하고 본인의 API 키를 채워 넣으세요.

### 프론트엔드 (터미널 2)

```bash
cd frontend
npm run dev
```

`http://localhost:5173` 에서 화면을 확인할 수 있습니다. 프론트의 `/api` 요청은 Vite 프록시를 통해 백엔드(`localhost:8000`)로 전달됩니다.
