from flask import Flask, jsonify, request
from flask_cors import CORS

import db_to_json

# Crear una instancia de la aplicación Flask
app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@app.route('/api/v1/hours', methods=['GET'])
def hours():
    try:
        a = db_to_json.get_hours_json()
        print(a)
        return jsonify(a)
    except:
        return []

@app.route('/api/v1/get_user_from_mail_phone', methods=['GET'])
def getNombreApellido():
    try:
        telefono = request.args.get('phone')
        correo = request.args.get('email')
        nombres_apellidos = db_to_json.get_user_from_mail_and_phone_json(telefono, correo)
        return jsonify(nombres_apellidos)
    except:
        return set()


@app.route('/api/v1/not_reserved_tables', methods=['GET'])
def mesas_por_fecha():
    date = "not readed yet"
    try:
        date = request.args.get('date')
        if date:
            a = db_to_json.get_mesas_disponibles_fecha_json(date)
            print(a)
            return jsonify(a)
        else:
            return set()
    except:
        print("Ocurrio un error extraño al evaluar los datos de mesas no reservadas para ", date)
        return set()


@app.route('/api/v1/check_email', methods=['GET'])
def validaCorreo():
    mail = "not readed yet"
    try:
        mail = request.args.get('email')
        return jsonify(db_to_json.email_exists(mail))
    except:
        print("Ocurrio un error extraño al buscar un usuario con el correo ", mail)
        return {"exists": False}


@app.route('/api/v1/check_phone', methods=['GET'])
def ValidaCelular():
    phone = "not readed yet"
    try:
        phone = request.args.get('phone')
        return jsonify(db_to_json.phone_exists(phone))
    except:
        print("Ocurrio un error extraño al buscar un usuario con el telefono ", phone)
        return {"exists": False}


@app.route('/api/v1/get_hours_per_table', methods=['GET'])
def HorasLibresPorMesaYFecha():
    date = table = "not readed yet"
    try:
        date = request.args.get('date')
        table = request.args.get('table')
        return jsonify(db_to_json.get_free_table_hours_per_day(date,table))
    except:
        print("Ocurrio un error extraño al buscar horas para la mesa", table, "y la fecha", date)
        return []


@app.route('/api/v1/registerUser', methods=['GET'])
def registrarUsuario():
    name = last_name = email = phone = "not readed yet"
    try:
        name = request.args.get('name')
        last_name = request.args.get('last_name')
        email = request.args.get('email')
        phone = request.args.get('phone')
        return jsonify(db_to_json.create_new_user(name,last_name, email, phone))
    except Exception as e:
        db_error = str(e)
        print("Ocurrio un error extraño al registrar al usuario con correo",email,"y telefono",phone,":",db_error)
        return jsonify({"id": -1})

@app.route('/api/v1/reserve', methods=['GET'])
def reserve():
    user_id = date = table_id = startTime = endTime = message = "not readed yet"
    try:
        user_id = request.args.get('user_id')
        date = request.args.get('date')
        table_id = request.args.get('table_id')
        startTime = request.args.get('start')
        endTime = request.args.get('end')
        message = request.args.get('message')
        email = request.args.get('email')
        phone = request.args.get('phone')
        to_return = db_to_json.json_reservation(user_id, date, table_id, startTime, endTime, message)
        return jsonify(to_return)
        if to_return["response"] == True:
            #magic_mail.email_successful_reservation(date, email, phone)
            print("response")
    except Exception as e:
        db_error = str(e)
        print("Ocurrió un error extraño al realizar la reserva:", db_error)
        return jsonify({"response": False})

if __name__ == '__main__':
    # Ejecutar la aplicación en el puerto 5000
    app.run(debug=True, host='0.0.0.0',port=8080)