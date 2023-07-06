from database import conn,cur

def select_items(dbname):
    conn.rollback()
    cur.execute(f"""
                SELECT * FROM {dbname}.goods
                    left join {dbname}.qrgoods on goods.itemcode = qrgoods.itemcode
                    left join {dbname}.qrsubcat on qrgoods.subcat = qrsubcat.sub
                    where qrgoods.`hide` = '' ;
                """)
    rows = cur
    keys = [i[0] for i in cur.description]
    return [dict(zip(keys, row)) for row in rows]
