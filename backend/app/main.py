import traceback
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

load_dotenv()

from app import db
from app.routers import coach, levels, practice, profile, progress, report, review


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield


app = FastAPI(title="PyCoach API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5190",
        "https://python-coach-app-claude.vercel.app",
    ],
    allow_origin_regex=r"https://python-coach-app-claude.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TEMP DEBUG — remove once the Render Postgres issue is fully resolved.
@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return await http_exception_handler(request, exc)
    return JSONResponse(
        status_code=500,
        content={"debug_trace": traceback.format_exc()},
    )


app.include_router(levels.router)
app.include_router(practice.router)
app.include_router(review.router)
app.include_router(progress.router)
app.include_router(coach.router)
app.include_router(report.router)
app.include_router(profile.router)


@app.get("/api/hello")
def hello():
    return {"message": "PyCoach 백엔드가 정상적으로 연결되었습니다."}
