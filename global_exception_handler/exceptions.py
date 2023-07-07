from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette import status


class authenticationFailedException(Exception):
    def __init__(self,msg : str):
        self.msg=msg


async def authentication_exception_handler(request:Request, exc: authenticationFailedException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message":f"{exc.msg}"},
    )

    
class dataNotFoundException(Exception):
    def __init__(self, msg : str):
        self.msg=msg

async def dataNotFoundException_handler(request:Request, exc : dataNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message" : f"{exc.msg}"},
    )