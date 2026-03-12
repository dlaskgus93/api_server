# app/schemas/model_schema.py
from pydantic import BaseModel
from typing import Optional, List, Any

# --- 공통 에러 DTO ---
class ErrorResponse(BaseModel):
    error_code: str
    message: str
    detail: str

# --- API 1: 모델 리스트 조회 DTO ---
class ModelListRequest(BaseModel):
    model_name: Optional[str] = None # 테스트를 위함 원래는 : str
    status: Optional[str] = None # 선택적 필드

class ModelResponse(BaseModel):
    model_name: str
    status: str

# --- API 2: 모델 등록 DTO ---
class ModelRegisterResponse(BaseModel):
    message: str
    result: dict

class ModelUploadRequest(BaseModel): # DTO
    model_name: str