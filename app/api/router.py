import os
import shutil
from fastapi import APIRouter, Depends, Form, File, UploadFile
from app.schemas.model_schema import *
from app.services.model_service import ModelService

router = APIRouter(prefix="/api/v1/models", tags=["Models"])
service = ModelService()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMP_DIR = os.path.join(BASE_DIR, "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

@router.get("", response_model=List[ModelResponse], responses={400: {"model": ErrorResponse}})
async def list_models(request: ModelListRequest = Depends()):
    # 🌟 서비스의 async 함수를 호출합니다.
    return await service.get_model_list_async(request)

@router.post("/upload", response_model=ModelRegisterResponse, responses={400: {"model": ErrorResponse}})
async def register_model(model_name: str = Form(...), file: UploadFile = File(...)):
    # 1. 파일 저장
    temp_path = os.path.join(TEMP_DIR, file.filename)
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 2. DTO 구성
    request_dto = ModelUploadRequest(model_name=model_name)
    
    # 3. 🌟 Celery 없이 직접 비동기 서비스 호출
    result = await service.register_model_async(request_dto, temp_path)
    
    return ModelRegisterResponse(message="등록 완료", result=result)