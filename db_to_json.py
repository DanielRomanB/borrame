import new_db
def get_user_from_mail_and_phone_json(telf, mail):
    datosUsuario = db.get_user_from_mail_and_phone(telf, mail)
    if len(datosUsuario) == 3:
        return {
            "name": datosUsuario[0],
            "last_name": datosUsuario[1],
            "id": datosUsuario[2]
        }
    else:
        return {}


def get_mesas_disponibles_fecha_json(fecha):
    jsonmesas = []
    mesasPorFecha = db.get_mesas_from_date(fecha);
    for mesa in mesasPorFecha:
        jsonmesas.append(
            {
                "id": str(mesa[0]),
                "guests": str(mesa[1])
            }
        )
    return jsonmesas

def get_mesas_json():
    jsonmesas = []
    listaMesas = db.get_mesas()
    for mesa in listaMesas:
        jsonmesas.append(
            {
                "id": str(mesa[0]),
                "guests": str(mesa[1])
            }
        )
    return jsonmesas

def get_hours_json(id):
    json_hours = []
    lista_horas = db.get_horas()
    for hora in lista_horas:
        json_hours.append(
            {
                "id": str(hora[0]),
                "hour": str(hora[1]),
                "minute": str(hora[2]).zfill(2)
            }
        )
    return json_hours

def get_hour_from_id(id):
    lista_horas = db.get_horas()
    if (id > len(lista_horas)): return "??:??"
    for hora in lista_horas:
        if hora[0] == id:
            return str(hora[1]) + ":" + str(hora[2]).zfill(2)

def email_exists(email):
    return {"exists": db.email_exists(email)}


def phone_exists(phone):
    return {"exists": db.phone_exists(phone)}


def get_free_table_hours_per_day(date, table):
    json_hours = []
    lista_horas = db.get_hours_from_table_and_date(date, table)
    for hora in lista_horas:
        json_hours.append(
            {
                "id": str(hora[0]),
                "hour": str(hora[1]),
                "minute": str(hora[2]).zfill(2),
                "next_hour": str(hora[3]),
                "next_minute": str(hora[4]).zfill(2),
            }
        )
    return json_hours


def create_new_user(name, last_name, email, phone):
    return {"id": db.register_user(name,last_name, email, phone)}


def json_reservation(user_id,date,table_id,start,end,message):
    return {"response": db.register_reservation(user_id, date, table_id, start, end, message)}
