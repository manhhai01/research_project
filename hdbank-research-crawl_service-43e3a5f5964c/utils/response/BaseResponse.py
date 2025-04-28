from fastapi.responses import JSONResponse

class BaseResponse:
    def __init__(self, data: dict):
        self.content = data['message']
        self.status = data['status'] if 'status' in data else 200

    def success(self):
        return JSONResponse(
            content={
                "data": self.content,
                "error": None,
            }
        )
    
    def error(self):
        return JSONResponse(
            content={
                "data": None,
                "error": self.content,
            },
            status_code=self.status,
        )
