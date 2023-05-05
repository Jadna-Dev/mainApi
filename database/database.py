from json import JSONDecoder
import mysql.connector as db

try:
    with open("./config.json", "r") as conf1:
        conf = JSONDecoder().decode(conf1.read())
        dbip = conf["databaseIp"]
        dbport = conf["databasePort"]
        dbpass = conf["databasePass"]

    conn = db.connect(user="root", password=dbpass,
                      host=dbip, port=dbport)
    cur = conn.cursor()
except Exception as e:
    print(str(e))
    with open("./Errorlog.txt", "a") as er:
        er.write(str(e)+"\n")


def drop_table(dbname, tablename):
    cur.execute(f"DROP TABLE IF exists {dbname}.{tablename};")


def create_pdxgoods(dbname):
    cur.execute(f"""
                CREATE TABLE {dbname}.`pdxgoods` (
  `itemcode` varchar(20) NOT NULL,
  `originalnumber` varchar(20) DEFAULT '',
  `itemname1` varchar(100) DEFAULT '',
  `itemname2` varchar(100) DEFAULT '',
  `tax` varchar(1) NOT NULL DEFAULT '',
  `sale1` decimal(18,3) DEFAULT '0.000',
  `sale2` decimal(18,3) DEFAULT '0.000',
  `sale3` decimal(18,3) DEFAULT '0.000',
  `sale4` decimal(18,3) DEFAULT '0.000',
  `tax_included` varchar(1) NOT NULL DEFAULT '',
  `disc1` decimal(18,3) DEFAULT '0.000',
  `disc2` decimal(18,3) DEFAULT '0.000',
  `disc3` decimal(18,3) DEFAULT '0.000',
  `disc4` decimal(18,3) DEFAULT '0.000',
  `qty_in` int NOT NULL DEFAULT '1',
  `qty_out` int NOT NULL DEFAULT '1',
  `category` varchar(30) DEFAULT NULL,
  `set` varchar(20) DEFAULT NULL,
  `brand` varchar(20) DEFAULT NULL,
  `supplier` varchar(10) DEFAULT NULL,
  `size` varchar(10) DEFAULT NULL,
  `color` varchar(20) DEFAULT NULL,
  `unit` varchar(20) DEFAULT NULL,
  `type` varchar(20) DEFAULT 'Inventory',
  `family` varchar(20) DEFAULT NULL,
  `note` varchar(300) DEFAULT '',
  PRIMARY KEY (`itemcode`),
  UNIQUE KEY `itemcode_UNIQUE` (`itemcode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

                """)
    conn.commit()


def create_pdxinv(dbname):
    cur.execute(f""" CREATE TABLE {dbname}.`pdxinv` (
  `itemcode` varchar(100) DEFAULT NULL,
  `type` varchar(45) DEFAULT NULL,
  `depstk` varchar(45) DEFAULT NULL,
  `qin` decimal(18,7) DEFAULT NULL,
  `qout` decimal(18,7) DEFAULT NULL,
  `qprice` decimal(18,7) DEFAULT NULL,
  `qpacking` decimal(18,7) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
""")
    conn.commit()


def create_pdxset(dbname):
    cur.execute(f""" CREATE TABLE {dbname}.`pdxset` (
  `id` varchar(6) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

""")
    conn.commit()
