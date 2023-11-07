import psycopg2
connection_string = """
    host=dpg-cl4msa9828mc73cvk9l0-a.oregon-postgres.render.com
    user=wachuma_user
    password=yBS3OBxnxevaHKwGoc8EDY7m0orISE4L
    dbname=wachuma
"""

mesas = list()
horas = list()

def get_mesas() -> list:
    if len(mesas) == 0:
        query = "SELECT * FROM Mesas"
        try:
            conn = psycopg2.connect(connection_string)
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                mesas.append(row)
            return mesas
        except psycopg2.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return "error"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        return mesas


def get_mesas_disponibles(fecha, grupo_horas, asistentes) -> list:
    query = "SELECT * FROM GetAvailableTables(?,?,?);"
    response = []
    try:
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        for elements in grupo_horas:
            cursor.execute(query, (fecha, elements, asistentes))
            rows = cursor.fetchall()
            response.append(set())
            for row in rows:
                response[len(response) - 1].add(tuple(row))
        return set.intersection(*response)
    except psycopg2.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return "error"
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_horas() -> list:
    if len(horas) == 0:
        query = "SELECT * FROM Horas"
        try:
            conn = psycopg2.connect(connection_string)
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                horas.append(row)
            return horas
        except psycopg2.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return [("ERROR","ERROR","ERROR")]
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        return horas


def get_user_from_mail_and_phone(telefono, email) -> list:
    response = []
    query = "SELECT Nombres, Apellidos, Id FROM Clientes WHERE Telefono = ? and Correo = ?"
    try:
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute(query, (telefono, email))
        rows = cursor.fetchall()
        for row in rows:
            response = row
        return response
    except psycopg2.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return [("ERROR", "ERROR")]
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_mesas_from_date(date):
    response = []
    query = "SELECT * FROM GetMesasDisponibles(?)"
    try:
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute(query, (date))
        rows = cursor.fetchall()
        for row in rows:
            response.append(row)
        return response
    except psycopg2.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return [("ERROR", "ERROR")]
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def email_exists(email):
    query = "SELECT * FROM Clientes WHERE Correo = ?"
    try:
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute(query, email)
        rows = cursor.fetchall()
        #Si existe alguna fila, devuelve true
        for row in rows:
            return True
        #Si no, devuelve false
        return False
    except psycopg2.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def phone_exists(phone):
    query = "SELECT * FROM Clientes WHERE Telefono = ?"
    try:
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute(query, phone)
        rows = cursor.fetchall()
        #Si existe alguna fila, devuelve true
        for row in rows:
            return True
        #Si no, devuelve false
        return False
    except psycopg2.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_hours_from_table_and_date(date, table) -> list:
    query = "SELECT * FROM GetHorasDisponiblesPorMesa(?, ?)"
    response = []
    try:
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute(query, (date, table))
        rows = cursor.fetchall()
        for row in rows:
            response.append(row)
        return response
    except psycopg2.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return [("ERROR", "ERROR", "ERROR")]
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def register_user(name,last_name, email, phone):
    try:
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        query = "INSERT INTO Clientes (Nombres, Apellidos, Correo, Telefono) VALUES (?,?,?,?)"
        cursor.execute(query, (name,last_name, email, phone))
        conn.commit()
        search = "SELECT Id FROM Clientes WHERE Correo = ?"
        cursor.execute(search, email)
        rows = cursor.fetchall()
        print(rows)
        return rows[0][0]
    except:
        print("Ocurrio un error en la base de datos al registrar un nuevo usuario")
        return -1
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def register_reservation(user_id,date,table_id,start,end,message):
    try:
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        query = "INSERT INTO Mensajes (Mensaje) VALUES (?)"
        search = "SELECT TOP 1 Id FROM Mensajes ORDER BY Id DESC"
        cursor.execute(query, (message))
        cursor.execute(search)
        rows = cursor.fetchall()
        message_id = rows[0][0]
        register = "INSERT INTO Reservas (Fecha, IdCliente, HoraID, MesaID, MensajeID) VALUES (?,?,?,?,?)"
        for value in range(int(start), int(end) + 1):
            cursor.execute(register, (date, user_id, value, table_id, message_id))
        conn.commit()
        return True
    except Exception as e:
        print("Ocurrio un error en la base de datos al realizar la reserva:", str(e))
        a = str(e).split('[')
        if(len(a) > 5):
            if(a[4].startswith("SQL Server]Violation of PRIMARY KEY constraint")):
                return "already"
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
