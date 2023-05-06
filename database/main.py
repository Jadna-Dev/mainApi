from time import sleep
from fastapi import FastAPI
from database import database as db

database = FastAPI()


@database.post("/insert_data/")
async def insert_data(ldata: dict):
    err = ""
    try:
        data = ldata["data"]
        db.conn.database = data["onlineDbName"]
        for d in data["data"]:
            db.conn.rollback()
            db.drop_table(data["onlineDbName"], d["tablename"])
            sleep(1)
            exec(f"""db.create_{d["tablename"]}(\"{data["onlineDbName"]}\")""")
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
                            str(val).replace("\'", "").replace("\\","")+"\'"
                    else:
                        values = values + "," + "\'" + \
                            str(val).replace("\'", "").replace("\\","")+"\'"
                # print(
                #     f"""INSERT INTO `{d["tablename"]}` ({fields}) VALUES ({values});"""
                # )
                err = f"""INSERT INTO `{d["tablename"]}` ({fields}) VALUES ({values});"""
                db.cur.execute(
                    f"""INSERT INTO `{d["tablename"]}` ({fields}) VALUES ({values});"""
                )
            db.conn.commit()
        return {
            "info": "successfull"
        }
    except Exception as e:
        print(err)
        return {
            "info": "failed",
            "msg": str(e)
        }
