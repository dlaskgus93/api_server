from app.exceptions import ModelProcessingError
from app.infra.inference_client import InferenceClient
from app.schemas.model_schema import ModelListRequest, ModelUploadRequest

class ModelService:
    def __init__(self):
        self.infra = InferenceClient()

    # [API 1] 리스트 조회 (비동기로 변경)
    async def get_model_list_async(self, request_dto: ModelListRequest):
        try:
            if not request_dto.model_name:
                raise ModelProcessingError(error_code="MODEL_ERR_001", message="검증 실패", detail="모델명은 필수입니다.")
            
            # 🌟 인프라의 비동기 함수 호출
            return await self.infra.fetch_models_async(request_dto.model_name, request_dto.status)
        
        except ModelProcessingError as e:
            raise e

        except Exception as e:
            raise ModelProcessingError(error_code="MODEL_ERR_002", message="조회 실패", detail=str(e))

    # [API 2] 모델 등록 (비동기 + DTO)
    async def register_model_async(self, request_dto: ModelUploadRequest, file_path: str):
        try:
            if request_dto.model_name == "fail_test":
                raise ModelProcessingError(
                    error_code="MODEL_ERR_400", 
                    message="지원하지 않는 모델명입니다.", 
                    detail="fail_test는 테스트용 예약어입니다."
                )
            
            if not request_dto.model_name:
                raise ModelProcessingError(error_code="ERR_001", message="모델명 누락", detail="DTO 검증 오류")

            # 🌟 인퍼런스 서버로 직접 비동기 호출
            result = await self.infra.upload_to_inference_async(
                model_name=request_dto.model_name,
                file_path=file_path
            )
            return result

        except ModelProcessingError as e:
            raise e

        except Exception as e:
            # 🌟 여기서 던져진 에러는 Global Handler가 낚아챕니다.
            raise ModelProcessingError(
                error_code="MODEL_ERR_500",
                message="인퍼런스 서버 처리 중 오류 발생",
                detail=str(e)
            )