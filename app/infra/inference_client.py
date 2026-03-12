import os
import httpx
import asyncio  # 🌟 지연 시간 시뮬레이션을 위해 추가

class InferenceClient:
    def __init__(self):
        self.base_url = "http://fake-inference-server:8000/api"

    async def fetch_models_async(self, model_name: str, status: str = None):
        """[비동기] 모델 목록 조회"""
        # 🌟 실제 서버 통신 대기 시간을 1초로 시뮬레이션
        await asyncio.sleep(1) 
        
        # 실제 코드는 주석 처리 유지
        # async with httpx.AsyncClient() as client:
        #     params = {"name": model_name}
        #     if status: params["status"] = status
        #     response = await client.get(f"{self.base_url}/models", params=params, timeout=10.0)
        #     return response.json()
        
        return [{"model_name": model_name, "status": status or "LOADED"}]

    async def upload_to_inference_async(self, model_name: str, file_path: str):
        """[비동기] 모델 파일 업로드"""
        # 🌟 업로드가 오래 걸리는 상황(5초)을 시뮬레이션
        # 이 5초 동안 '전체 조회 API'를 호출해보면 비동기가 잘 되는지 알 수 있습니다!
        await asyncio.sleep(5)

        if not os.path.exists(file_path):
            raise Exception(f"파일 존재하지 않음: {file_path}")

        # 실제 코드는 주석 처리 유지
        # async with httpx.AsyncClient() as client:
        #     with open(file_path, "rb") as f:
        #         files = {"file": (os.path.basename(file_path), f)}
        #         data = {"model_name": model_name}

        #         response = await client.post(
        #             f"{self.base_url}/v1/predict",
        #             data=data,
        #             files=files,
        #             timeout=60.0 # 작업 시간이 긴 것을 고려
        #         )
        #         response.raise_for_status()
        #         return response.json()

        return {"status": "success", "message": f"{model_name} 업로드 완료(Mock)"}

                
