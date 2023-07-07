from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette import status

app = FastAPI()

class dataMismatchException(Exception):
    def __init__(self, msg : str):
        self.msg=msg

@app.exception_handler(dataMismatchException)
def data_mismatch(request:Request, exc: dataMismatchException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={'message' : exc.msg},
    )
    

class authenticationFailedException(Exception):
    def __init__(self,msg : str):
        self.msg=msg

@app.exception_handler(authenticationFailedException)
async def authentication_Exception(request:Request, exc: authenticationFailedException):
    return JSONResponse(
        status_code=409,
        content={"message":f"{exc.msg}"},
    )