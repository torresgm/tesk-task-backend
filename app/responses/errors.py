from starlette.exceptions import HTTPException
from app.responses import response


async def not_found(request, exc: HTTPException):
    return response(status=exc.status_code, message="Not Found")

async def bad_request(request, exc: HTTPException):
    return response(status=exc.status_code, message="Bad Request", errors=exc.detail)

# async def server_error(request, exc: HTTPException):
#     return response(None, status=exc.status_code, message="Internal Server Error")
