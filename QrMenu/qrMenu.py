from os import error
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import QrMenu.database as db 

qrMenu = FastAPI()

@qrMenu.post("/get_items/")
async def get_items(data:dict):
    try:
        r = db.select_items(data["dbname"])
        db.conn.rollback()
        return{
            "data":r,
            "info":"Successfull"
        }
    except Exception as e:
        return errorHandler(e)
        
        
def errorHandler(e):
    db.conn.rollback()
    return{
        "info":"Failed",
        "msg":str(e)
    }