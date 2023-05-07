import datetime
from fastapi import FastAPI
from database.database import cur, conn, drop_table,create_pdxgoods,create_pdxinv,create_pdxset
from json import JSONEncoder
from checkSales.database import *
from time import sleep

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
        print(data["token"])
        return select_token(data["token"])

    except Exception as e:
        return error_handler(e)


@cs.post("/getdata/")
async def getdata(data: dict):
    print(data)
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


@cs.post("/insert_data/")
async def insert_data(ldata: dict):
    err = ""
    conn.rollback()
    try:
        data = ldata["data"]
        conn.database = data["onlineDbName"]
        for d in data["data"]:
            drop_table(data["onlineDbName"], d["tablename"])
            sleep(1)
            exec(f"""create_{d["tablename"]}(\"{data["onlineDbName"]}\")""")
            print("here")
            sleep(1)
            for row in d["data"]:
                fields = ""
                values = ""
                for idx, key in enumerate(row.keys()):
                    if idx == 0:
                        fields = fields + "`"+key+"`"
                    else:
                        fields = fields + "," + "`"+key+"`"

                for idx, val in enumerate(row.values()):
                    if idx == 0:
                        values = values + "\'" + \
                            str(val).replace("\'", "").replace("\\", "")+"\'"
                    else:
                        values = values + "," + "\'" + \
                            str(val).replace("\'", "").replace("\\", "")+"\'"
                # print(
                #     f"""INSERT INTO `{d["tablename"]}` ({fields}) VALUES ({values});"""
                # )
                err = f"""INSERT INTO `{d["tablename"]}` ({fields}) VALUES ({values});"""
                cur.execute(
                    f"""INSERT INTO `{d["tablename"]}` ({fields}) VALUES ({values});"""
                )
                cur.execute(
                    f"UPDATE `jnp`.`clients_data` SET `last_updated` = '{str(datetime.datetime.now())}' WHERE (`client_id` = '{data['client_id']}') and (`dbname` = '{data['onlineDbName']}');")
            conn.commit()
        return {
            "info": "successfull",
            "msg": "here"
        }
    except Exception as e:
        print(err)
        return {
            "info": "failed",
            "msg": str(e)
        }


def error_handler(err: Exception):
    return {
        "info": "failed",
        "msg": str(err)
    }
