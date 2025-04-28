from fastapi import Request
from logger import logger

async def logging_middleware(request: Request, handler):
    log_dict = {
        "method": request.method,
        "url": request.url,
    }
    logger.info(log_dict)
    response = await handler(request)
    return response