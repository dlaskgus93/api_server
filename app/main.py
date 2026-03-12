# app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.api.router import router as model_router
from app.exceptions import ModelProcessingError
from app.schemas.model_schema import ErrorResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 앱 시작 시 필요한 로직 (예: DB 연결)
    print("🚀 Model Serving Server Started!")
    yield
    # 앱 종료 시 필요한 로직
    print("🛑 Server Shutdown.")

app = FastAPI(lifespan=lifespan)

# 🌟 전역 예외 그물: 서비스에서 던진 모든 ModelProcessingError를 여기서 낚아챕니다.
@app.exception_handler(ModelProcessingError)
async def model_error_handler(request, exc: ModelProcessingError):
    return JSONResponse(
        status_code=400,
        content={
            "error_code": exc.error_code, # 🌟 exc에서 꺼내 쓰기
            "message": exc.message,
            "detail": exc.detail
        }
    )

app.include_router(model_router)