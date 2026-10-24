from flask import Blueprint, jsonify, request
from database import mysql

alumnos_bp = Blueprint(
    'maestros',
    __name__,
    url_prefix='/api/maestros'
)

def fila_a_diccionario(cursor,fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas,fila))

#GET: consultar todos los maestros
@maestros_bp.route('/maestros',methods=['GET'])
def lista_maestros():
    cursor = None

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT matricula, nombre, apaterno, amaterno, correo FROM maestros""")
        datos = cursor.fetchall()
        maestros = [
            fila_a_diccionario(cursor,fila)
            for fila in datos
        ]

        return jsonify({
            'maestros':maestros,
            'mensaje':'Lista de maestros',
            'exito':True

        }),200

    except Exception:
        return jsonify({
        'mensaje':'Error al consultar la tabla de maestros',
        'exito':False
        }),500
    finally:
        if cursor is not None:
            cursor.close()