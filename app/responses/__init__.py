import datetime
from starlette.responses import JSONResponse


def response(status=200, message="Operation completed successfully", timestamp=datetime.datetime.now().isoformat(), **args):
    return JSONResponse({"timestamp": timestamp, "status": status, "message": message, **args}, status_code=status)


def server_error_response():
    return response(status=500, message="Internal Server Error")
