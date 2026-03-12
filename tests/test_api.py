import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from io import BytesIO

# 🌟 1. 비동기 테스트를 위한 설정 (pytest-asyncio)
@pytest.fixture
async def async_client():
    # ASGITransport를 사용하여 실제 서버 실행 없이 앱의 로직을 테스트합니다.
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

# --- [GET /api/v1/models] 테스트 ---

@pytest.mark.asyncio
async def test_list_models_success(async_client):
    """모델 목록 조회 성공 케이스"""
    response = await async_client.get("/api/v1/models", params={"model_name": "test_model"})
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["model_name"] == "test_model"

@pytest.mark.asyncio
async def test_list_models_validation_error(async_client):
    """모델명 누락 시 커스텀 에러(400) 핸들링 테스트"""
    # model_name을 보내지 않음
    response = await async_client.get("/api/v1/models")
    
    assert response.status_code == 400
    data = response.json()
    assert data["error_code"] == "MODEL_ERR_001"
    assert "모델명은 필수입니다" in data["detail"]


# --- [POST /api/v1/models/upload] 테스트 ---

@pytest.mark.asyncio
async def test_register_model_success(async_client):
    """모델 업로드 및 등록 성공 케이스"""
    # 가상의 파일 생성
    file_content = b"fake model data"
    file = ("test_model.bin", BytesIO(file_content), "application/octet-stream")
    
    response = await async_client.post(
        "/api/v1/models/upload",
        data={"model_name": "my_new_model"},
        files={"file": file}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "등록 완료"
    assert data["result"]["status"] == "success"

@pytest.mark.asyncio
async def test_register_model_business_error(async_client):
    """비즈니스 로직 에러(fail_test 입력 시) 핸들링 테스트"""
    file = ("test.bin", BytesIO(b"data"), "application/octet-stream")
    
    response = await async_client.post(
        "/api/v1/models/upload",
        data={"model_name": "fail_test"}, # 🌟 에러 유발 키워드
        files={"file": file}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert data["error_code"] == "MODEL_ERR_400"
    assert "지원하지 않는 모델명" in data["message"]