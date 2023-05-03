from time import sleep
from fastapi import FastAPI
from database import database as db

database = FastAPI()


@database.post("/insert_data/")
async def insert_data(ldata: dict):
    data = ldata["data"]
    db.conn.database = data["onlineDbName"]
    for d in data["data"]:
        db.conn.rollback()
        db.drop_table(data["onlineDbName"], d["tablename"])
        sleep(2)
        exec(f"""db.create_{d["tablename"]}(\"{data["onlineDbName"]}\")""")
        print("here")
        sleep(2)
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
                    values = values + "\'" + str(val).replace("\'", "")+"\'"
                else:
                    values = values + "," + "\'" + \
                        str(val).replace("\'", "")+"\'"
            print(
                f"""INSERT INTO `{d["tablename"]}` ({fields}) VALUES ({values});""")
            db.cur.execute(
                f"""INSERT INTO `{d["tablename"]}` ({fields}) VALUES ({values});"""
            )
        db.conn.commit()
