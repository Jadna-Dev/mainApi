from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fernet import Fernet
activation = FastAPI()

fernet = Fernet(b'VelTY920UXSRTjsT4O7EjYiKNeBMmusSrJguaLeC4s0=')


@activation.post("/check_activation/")
async def get_activation(data:dict):
    print(data)
    mac = fernet.decrypt(data["mac"].encode()).decode()
    print(mac)
    return JSONResponse({
        "info": "successfull",
        "error":"",
        "msg1":"",
        "msg2":"",
        "msg3":"",
        "msg4":"",
        "msg5":"",})
