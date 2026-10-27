from flask import Blueprint, jsonify, request
from database import mysql

maestros_bp = Blueprint(
    'maestros',
    __name__,
    url_prefix='/api/maestros'
)


def fila_a_diccionario(cursor,fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas,fila))

@maestros_bp.route('/', methods=['GET'])
def lista_maestros():
    cursor = None

    try:
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT idmaestro, nombre, apaterno, amaterno, correo
            FROM maestros
        """)

        datos = cursor.fetchall()

        maestros = [
            fila_a_diccionario(cursor, fila)
            for fila in datos
        ]

        return jsonify({
            'maestros': maestros,
            'mensaje': 'Lista de maestros',
            'exito': True
        }), 200

    except Exception as e:
        print("ERROR AL CONSULTAR MAESTROS:", repr(e))

        return jsonify({
            'mensaje': 'Error al consultar la tabla de maestros',
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


    
@maestros_bp.route('/', methods=['POST'])
def registrar_maestro():
    cursor = None

    try:
        datos = request.get_json()

        if not datos:
            return jsonify({
                'mensaje': 'Debes enviar los datos en formato JSON',
                'exito': False
            }), 400

        nombre = datos.get('nombre')
        apaterno = datos.get('apaterno')
        amaterno = datos.get('amaterno')
        correo = datos.get('correo')

        if not all([nombre, apaterno, amaterno, correo]):
            return jsonify({
                'mensaje': 'Todos los campos son obligatorios',
                'exito': False
            }), 400

        cursor = mysql.connection.cursor()

        cursor.execute("""
            INSERT INTO maestros
            (nombre, apaterno, amaterno, correo)
            VALUES (%s, %s, %s, %s)
        """, (nombre, apaterno, amaterno, correo))

        mysql.connection.commit()

        return jsonify({
            'idmaestro': cursor.lastrowid,
            'mensaje': 'Maestro registrado correctamente',
            'exito': True
        }), 201

    except Exception as e:
        mysql.connection.rollback()
        print("ERROR AL REGISTRAR MAESTRO:", repr(e))

        return jsonify({
            'mensaje': 'Error al registrar el maestro',
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()



@maestros_bp.route('/<string:idmaestro>', methods=['DELETE'])
def eliminar_maestro(idmaestro):
    cursor = None

    try:
        cursor = mysql.connection.cursor()

        cursor.execute("""
            DELETE FROM maestros
            WHERE idmaestro = %s
        """, (idmaestro,))

        if cursor.rowcount == 0:
            mysql.connection.rollback()

            return jsonify({
                'mensaje': 'Maestro no encontrado',
                'exito': False
            }), 404

        mysql.connection.commit()

        return jsonify({
            'mensaje': 'Maestro eliminado correctamente',
            'exito': True
        }), 200

    except Exception as e:
        mysql.connection.rollback()
        print("ERROR AL ELIMINAR MAESTRO:", repr(e))

        return jsonify({
            'mensaje': 'Error al eliminar el maestro',
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()
