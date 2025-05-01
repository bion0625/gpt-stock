from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
import asyncio

# .env 파일 로드 (가장 위에서)
load_dotenv()

from app.auth import router as auth_router
from app.portfolio import router as portfolio_router
from app.collect import router as collect_router
from app.database import init_db

# 실행 코드
# 기본
# python -m venv .venv
# .\.venv\Scripts\activate
# pip install -r requirements.txt
# 서버
# uvicorn app.main:app --reload

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(portfolio_router)
app.include_router(collect_router)

@app.get("/")
def read_root():
    return {"message": "주식 분석 API 서버에 오신 것을 환영합니다"}
