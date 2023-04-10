from fastapi import FastAPI
from api import auth, expenses
from database import engine

app = FastAPI()

# 인증과 가계부 API를 등록
app.include_router(auth.router)
app.include_router(expenses.router)


@app.on_event("startup")
async def startup():
    # 데이터베이스 연결을 생성
    await engine.connect()


@app.on_event("shutdown")
async def shutdown():
    # 데이터베이스 연결을 종료
    await engine.disconnect()
