import time

from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.logger import logger


class RequestLoggerMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        message = (
            f"{request.method} "
            f"{request.url.path} "
            f"{process_time:.4f} sec"
        )

        print(message)

        logger.info(message)

        return response