from sqlite3 import dbapi2
from database.database import conn, cur
import uuid


def select_login(id, password):
    cur.execute(
        f"SELECT * FROM jnp.clients_online where service_name = 'cs' and client_id = '{id}' and password = '{password}';")
    rows = cur
    keys = [i[0] for i in cur.description]
    data = [dict(zip(keys, row)) for row in rows]
    mytoken = str(uuid.uuid1())
    for d in data:
        cur.execute(f"""
                    UPDATE `jnp`.`clients_online` SET `token` = '{mytoken}' WHERE (`username` = '{d["username"]}');
                    """)
        conn.commit()
        return mytoken
    return "failed"


def select_token(token: str):
    cur.execute(f"SELECT * FROM jnp.clients_online where token = '{token}';")
    rows = cur
    keys = [i[0] for i in cur.description]
    service = [dict(zip(keys, row)) for row in rows]
    for s in service:
        cur.execute(
            f"SELECT * FROM jnp.clients where id = '{s['client_id']}';")
        compname = ""
        rows = cur
        keys = [i[0] for i in cur.description]
        user = [dict(zip(keys, row)) for row in rows]
        for u in user:
            compname = u["company_name"]

        cur.execute(
            f"SELECT * FROM jnp.clients_data where client_id = '{s['client_id']}';")
        rows = cur
        keys = [i[0] for i in cur.description]
        client_data = [dict(zip(keys, row)) for row in rows]
        return {
            "info": "successfull",
            "compname": compname,
            "data_list": client_data,
            "id": s['client_id']
        }
    return {"info": "failed", "msg": "Token Expired"}


def select_data(dbname):
    conn.database = dbname
    cur.execute(f"""
                   SELECT `pdxset`.name,pdxset.id,pdxgoods.itemcode,sum(CASE WHEN pdxinv.type = 'PI' or pdxinv.type = 'PIOPEN'  THEN  pdxinv.qprice * pdxinv.qin else 0 END) as total_cost
                        ,sum(CASE WHEN pdxinv.type = 'SA' THEN  pdxinv.qprice * pdxinv.qpacking else 0 END)-sum(CASE WHEN pdxinv.type = 'SR'   THEN  pdxinv.qprice * pdxinv.qpacking else 0 END) as total_sales
                        ,pdxgoods.pdxcost * (sum(CASE WHEN pdxinv.type = 'SA'   THEN  pdxinv.qout  else 0 END) - sum(CASE WHEN pdxinv.type = 'SR'   THEN  pdxinv.qin else 0 END)) as sales_cost
                        ,sum(CASE WHEN pdxinv.type = 'PIADJ' THEN pdxinv.qprice *  pdxinv.qin else 0 END) AS adjkqty
                        ,pdxgoods.pdxcost * (sum(CASE WHEN pdxinv.type = 'PI'   THEN  pdxinv.qin else 0 END) - sum(CASE WHEN pdxinv.type = 'SA'   THEN  pdxinv.qout  else 0 END) + sum(CASE WHEN pdxinv.type = 'SR'   THEN  pdxinv.qin  else 0 END) + sum(CASE WHEN pdxinv.type = 'PIADJ' THEN pdxinv.qin else 0 END)) AS stock_value
                                FROM pdxset
                                left JOIN `pdxgoods`
                                ON pdxset.id = `pdxgoods`.set
                                inner join pdxinv
                                on pdxinv.itemcode = pdxgoods.itemcode
                                
                                group by pdxset.name,pdxgoods.itemcode
                   """)
    rows = cur
    keys = [i[0] for i in cur.description]
    data = [dict(zip(keys, row)) for row in rows]

    cur.execute(f"""
                   SELECT distinct(id) as id,name from pdxset order by id
                   """)
    rows = cur
    keys = [i[0] for i in cur.description]
    setlist = [dict(zip(keys, row)) for row in rows]
    # {"name":"CON   B","itemcode":"1031-18","total_cost":2245.4456,"total_sales":955.5216667,"sales_cost":676.7005}
    fdata = []
    for setid in setlist:
        total_cost = 0
        total_sales = 0
        sales_cost = 0
        qtyvalue = 0
        for d in data:
            if setid["id"] == d["id"]:
                total_cost = total_cost + float(d["total_cost"])
                total_sales = total_sales + float(d["total_sales"])
                sales_cost = float(sales_cost) + float(d["sales_cost"])
                # qtyvalue =  float(d['adjkqty'])
                qtyvalue = float(d['stock_value'])
        fdata.append({
            "setname": setid["name"],
            "total_cost": f"{round( total_cost):,}",
            "total_sales": f"{round( total_sales):,}",
            "sales_cost": f"{round( sales_cost):,}",
            "sales_profit": f"{round( float(total_sales - sales_cost)):,}",
            # "stock_value": f"{round( float((total_cost - sales_cost) - qtyvalue )):,}",
            "stock_value": f"{round( float(qtyvalue )):,}",
        })
    return fdata


def select_last_login(dbname, id):
    cur.execute(f"""
                SELECT * FROM jnp.clients_data where client_id = '{id}' and dbname = '{dbname}';
                """)
    rows = cur
    keys = [i[0] for i in cur.description]
    data = [dict(zip(keys, row)) for row in rows]
    for d in data:
        return d["last_updated"]
    return "Error"
