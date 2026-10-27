
from flask import Blueprint, jsonify, request
from database import mysql

alumnos_bp = Blueprint(
    'alumnos',
    __name__,
    url_prefix='/api/alumnos'
)

@alumnos_bp.route('/', methods=['GET'])
def lista_alumnos():
    cursor = None

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT matricula, nombre, apaterno, amaterno, correo
            FROM alumno
        """)

        datos = cursor.fetchall()
        columnas = [columna[0] for columna in cursor.description]

        alumnos = [
            dict(zip(columnas, fila))
            for fila in datos
        ]

        return jsonify({
            'alumnos': alumnos,
            'mensaje': 'Lista de alumnos',
            'exito': True
        }), 200

    except Exception as e:
        print("ERROR EN ALUMNOS:", repr(e))
        return jsonify({
            'mensaje': 'Error al consultar la tabla de alumnos',
            'detalle': str(e),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


@alumnos_bp.route('/', methods=['POST'])
def registrar_alumno():
    cursor = None

    try:
        datos = request.get_json()

        if not datos:
            return jsonify({
                'mensaje': 'No se recibieron datos del alumno',
                'exito': False
            }), 400

        matricula = datos.get('matricula')
        nombre = datos.get('nombre')
        apaterno = datos.get('apaterno')
        amaterno = datos.get('amaterno')
        correo = datos.get('correo')

        if any(valor is None for valor in [
            matricula, nombre, apaterno, amaterno, correo
        ]):
            return jsonify({
                'mensaje': 'Faltan campos obligatorios',
                'exito': False
            }), 400

        cursor = mysql.connection.cursor()

        cursor.execute("""
            INSERT INTO alumno
                (matricula, nombre, apaterno, amaterno, correo)
            VALUES (%s, %s, %s, %s, %s)
        """, (matricula, nombre, apaterno, amaterno, correo))

        mysql.connection.commit()

        return jsonify({
            'mensaje': 'Alumno registrado correctamente',
            'exito': True,
            'alumno': {
                'matricula': matricula,
                'nombre': nombre,
                'apaterno': apaterno,
                'amaterno': amaterno,
                'correo': correo
            }
        }), 201

    except Exception as e:
        mysql.connection.rollback()
        print("ERROR AL REGISTRAR ALUMNO:", repr(e))
        return jsonify({
            'mensaje': 'Error al registrar el alumno',
            'detalle': str(e),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


@alumnos_bp.route('/<string:matricula>', methods=['GET'])
def consultar_alumno(matricula):
    cursor = None

    try:
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT matricula, nombre, apaterno, amaterno, correo
            FROM alumno
            WHERE matricula = %s
        """, (matricula,))

        fila = cursor.fetchone()

        if fila is None:
            return jsonify({
                'mensaje': 'Alumno no encontrado',
                'exito': False
            }), 404

        alumno = dict(zip(
            [columna[0] for columna in cursor.description],
            fila
        ))

        return jsonify({
            'alumno': alumno,
            'mensaje': 'Alumno encontrado correctamente',
            'exito': True
        }), 200

    except Exception as e:
        print("ERROR AL CONSULTAR ALUMNO:", repr(e))
        return jsonify({
            'mensaje': 'Error al consultar el alumno',
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


@alumnos_bp.route('/<string:matricula>', methods=['DELETE'])
def eliminar_alumno(matricula):
    cursor = None

    try:
        cursor = mysql.connection.cursor()

        cursor.execute("""
            DELETE FROM alumno
            WHERE matricula = %s
        """, (matricula,))

        if cursor.rowcount == 0:
            mysql.connection.rollback()

            return jsonify({
                'mensaje': 'Alumno no encontrado',
                'exito': False
            }), 404

        mysql.connection.commit()

        return jsonify({
            'mensaje': 'Alumno eliminado correctamente',
            'exito': True
        }), 200

    except Exception as e:
        mysql.connection.rollback()
        print("ERROR AL ELIMINAR ALUMNO:", repr(e))

        return jsonify({
            'mensaje': 'Error al eliminar el alumno',
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()