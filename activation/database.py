from database import conn, cur


def check_activation(info):
    conn.rollback()
    cur.execute(
        f"""SELECT * FROM pyx.licences_data where serial_number = '{info["serial_number"]}';""")
    rows = cur
    keys = [i[0] for i in cur.description]
    lic = [dict(zip(keys, row)) for row in rows]

    data = {}
    cur.execute(
        f"""SELECT * FROM pyx.licences where serial_number = '{info["serial_number"]}';""")
    rows = cur
    keys = [i[0] for i in cur.description]
    tdata = [dict(zip(keys, row)) for row in rows]
    if len(tdata) !=0:
        data = tdata[0]

    if len(lic) == 0:
        cur.execute(f"""INSERT INTO `pyx`.`licences` 
                        (`serial_number`, `system_name`, `size`, `model`) 
                        VALUES ('{info["serial_number"]}', '{info["system_name"]}', '{info["serial_number"]}', '{info["model"]}');""")
        cur.execute(f"""INSERT INTO `pyx`.`licences_data` 
                        (`serial_number`, `type`, `status`) 
                        VALUES ('{info["serial_number"]}', 'backoffice', 'pending');""")
        conn.commit()
    return {
        "data": data,
        "lic": lic,
    }
