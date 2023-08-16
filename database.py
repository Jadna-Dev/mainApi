from json import JSONDecoder
import mysql.connector as db

try:
    with open("./config.json", "r") as conf1:
        conf = JSONDecoder().decode(conf1.read())
        dbip = conf["databaseIp"]
        dbport = conf["databasePort"]
        dbpass = conf["databasePass"]

    conn = db.connect(user="jadna", password=dbpass,
                      host=dbip, port=dbport)
    cur = conn.cursor()
except Exception as e:
    print(str(e))
    with open("./Errorlog.txt", "a") as er:
        er.write(str(e)+"\n")


