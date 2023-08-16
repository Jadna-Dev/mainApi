from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fernet import Fernet
import activation.database as db

activation = FastAPI()

fernet = Fernet(b'VelTY920UXSRTjsT4O7EjYiKNeBMmusSrJguaLeC4s0=')


@activation.post("/check_activation/")
async def get_activation(data:dict):

    r = db.check_activation(data["hard_disk_info"])
    db.conn.rollback

    return JSONResponse({
        "licence":str(r),
    })
