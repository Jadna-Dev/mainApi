from fastapi import FastAPI
from checkSales.database import *

cs = FastAPI()


@cs.post("/login/")
async def login(data: dict):
    try:
        r = select_login(data["id"], data["password"])
        if r == "failed":
            return {
                "info": "failed",
                "msg": "Incorrect Password or Id"
            }
        else:
            return {
                "info": "successfull",
                "token": r
            }
    except Exception as e:
        return error_handler(e)


@cs.post("/check_token/")
async def getdata(data: dict):
    try:
        return select_token(data["token"])

    except Exception as e:
        return error_handler(e)


@cs.post("/getdata/")
async def getdata(data: dict):
    try:
        if select_token(data["token"])["info"] != "successfull":
            return {"info": "failed"}
        r = select_data(data["dbname"])
        lg = select_last_login(data["dbname"],data["id"])
        return {
            "info": "successfull",
            "data": r,
            "lg":lg
            
        }
    except Exception as e:
        return error_handler(e)



def error_handler(err: Exception):
    return {
        "info": "failed",
        "msg": str(err)
    }
