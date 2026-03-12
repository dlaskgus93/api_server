# app/exceptions.py

class ModelProcessingError(Exception):
    def __init__(self, error_code: str, message: str, detail: str = None):
        # 🌟 인자로 error_code를 받도록 추가!
        self.error_code = error_code
        self.message = message
        self.detail = detail
        # 부모 Exception 클래스 초기화 (일반적으로 message를 넘김)
        super().__init__(self.message)