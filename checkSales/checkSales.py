from fastapi import FastAPI
from database.database import cur,conn
from json import JSONEncoder

cs = FastAPI()

@cs.get("/getdata/{dbname}")
async def getdata(dbname:str):
    conn.database = dbname
    cur.execute(f"""
                   SELECT `pdxset`.name,pdxset.id,pdxgoods.itemcode,sum(CASE WHEN pdxinv.type = 'PI' or pdxinv.type = 'PIOPEN'   THEN  pdxinv.qprice * pdxinv.qin else 0 END) as total_cost
                        ,sum(CASE WHEN pdxinv.type = 'SA' THEN  pdxinv.qprice * pdxinv.qpacking else 0 END)-sum(CASE WHEN pdxinv.type = 'SR'   THEN  pdxinv.qprice * pdxinv.qpacking else 0 END) as total_sales
                        ,max(CASE WHEN pdxinv.type = 'PI' THEN  pdxinv.qprice  else 0 END ) * (sum(CASE WHEN pdxinv.type = 'SA'   THEN  pdxinv.qout  else 0 END) - sum(CASE WHEN pdxinv.type = 'SR'   THEN  pdxinv.qin else 0 END)) as sales_cost
                                FROM pdxset
                                left JOIN `pdxgoods`
                                ON pdxset.id = `pdxgoods`.set
                                inner join pdxinv
                                on pdxinv.itemcode = pdxgoods.itemcode
                                where pdxinv.depstk = "1" 
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
        for d in data:
            if setid["id"] == d["id"]:
                total_cost = total_cost + float(d["total_cost"])
                total_sales = total_sales + float(d["total_sales"])
                sales_cost = sales_cost + float(d["sales_cost"])
        fdata.append({
            "setname":setid["name"],
            "total_cost":total_cost,
            "total_sales":total_sales,
            "sales_cost":sales_cost,
            "sales_profit":total_sales - sales_cost,
            "stock_value":total_cost - sales_cost,
        })
    return  {"info":fdata}