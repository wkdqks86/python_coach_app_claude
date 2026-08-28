from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from app import db
from app.routers import coach, levels, practice, progress, review


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield


app = FastAPI(title="PyCoach API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(levels.router)
app.include_router(practice.router)
app.include_router(review.router)
app.include_router(progress.router)
app.include_router(coach.router)


@app.get("/api/hello")
def hello():
    return {"message": "PyCoach 백엔드가 정상적으로 연결되었습니다."}
