from fastapi.responses import JSONResponse


class BaseResponse:
    def __init__(self, content, status=200):
        self.content = content
        self.status = status

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
                "error": self.content,
                "data": None,
            }
        )
