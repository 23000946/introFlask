
from flask import Blueprint, jsonify, request
from database import mysql

administrativos_bp = Blueprint(
    'administrativos',
    __name__,
    url_prefix='/api/administrativos'
)


@administrativos_bp.route('/', methods=['GET'])
def lista_administrativos():
    cursor = None

    try:
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT numempleado, nombre, apaterno, amaterno,
                   telefono, correo, departamento
            FROM administrativos
        """)

        datos = cursor.fetchall()
        columnas = [columna[0] for columna in cursor.description]

        administrativos = [
            dict(zip(columnas, fila))
            for fila in datos
        ]

        return jsonify({
            'administrativos': administrativos,
            'mensaje': 'Lista de administrativos',
            'exito': True
        }), 200

    except Exception as e:
        print("ERROR AL CONSULTAR ADMINISTRATIVOS:", repr(e))

        return jsonify({
            'mensaje': 'Error al consultar la tabla de administrativos',
            'detalle': str(e),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


@administrativos_bp.route('/', methods=['POST'])
def registrar_administrativo():
    cursor = None

    try:
        datos = request.get_json()

        if not datos:
            return jsonify({
                'mensaje': 'No se recibieron datos del administrativo',
                'exito': False
            }), 400

        nombre = datos.get('nombre')
        apaterno = datos.get('apaterno')
        amaterno = datos.get('amaterno')
        telefono = datos.get('telefono')
        correo = datos.get('correo')
        departamento = datos.get('departamento')

        if any(valor is None or valor == '' for valor in [
            nombre, apaterno, amaterno, telefono, correo, departamento
        ]):
            return jsonify({
                'mensaje': 'Faltan campos obligatorios',
                'exito': False
            }), 400

        cursor = mysql.connection.cursor()

        cursor.execute("""
            INSERT INTO administrativos
                (nombre, apaterno, amaterno, telefono, correo, departamento)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            nombre, apaterno, amaterno,
            telefono, correo, departamento
        ))

        mysql.connection.commit()
        numempleado = cursor.lastrowid

        return jsonify({
            'mensaje': 'Administrativo registrado correctamente',
            'exito': True,
            'administrativo': {
                'numempleado': numempleado,
                'nombre': nombre,
                'apaterno': apaterno,
                'amaterno': amaterno,
                'telefono': telefono,
                'correo': correo,
                'departamento': departamento
            }
        }), 201

    except Exception as e:
        mysql.connection.rollback()
        print("ERROR AL REGISTRAR ADMINISTRATIVO:", repr(e))

        return jsonify({
            'mensaje': 'Error al registrar el administrativo',
            'detalle': str(e),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


@administrativos_bp.route('/<int:numempleado>', methods=['GET'])
def consultar_administrativo(numempleado):
    cursor = None

    try:
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT numempleado, nombre, apaterno, amaterno,
                   telefono, correo, departamento
            FROM administrativos
            WHERE numempleado = %s
        """, (numempleado,))

        fila = cursor.fetchone()

        if fila is None:
            return jsonify({
                'mensaje': 'Administrativo no encontrado',
                'exito': False
            }), 404

        columnas = [columna[0] for columna in cursor.description]
        administrativo = dict(zip(columnas, fila))

        return jsonify({
            'administrativo': administrativo,
            'mensaje': 'Administrativo encontrado correctamente',
            'exito': True
        }), 200

    except Exception as e:
        print("ERROR AL CONSULTAR ADMINISTRATIVO:", repr(e))

        return jsonify({
            'mensaje': 'Error al consultar el administrativo',
            'detalle': str(e),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


# DELETE: eliminar un administrativo por ID
@administrativos_bp.route('/<int:numempleado>', methods=['DELETE'])
def eliminar_administrativo(numempleado):
    cursor = None

    try:
        cursor = mysql.connection.cursor()

        cursor.execute("""
            DELETE FROM administrativos
            WHERE numempleado = %s
        """, (numempleado,))

        if cursor.rowcount == 0:
            mysql.connection.rollback()

            return jsonify({
                'mensaje': 'Administrativo no encontrado',
                'exito': False
            }), 404

        mysql.connection.commit()

        return jsonify({
            'mensaje': 'Administrativo eliminado correctamente',
            'exito': True
        }), 200

    except Exception as e:
        mysql.connection.rollback()
        print("ERROR AL ELIMINAR ADMINISTRATIVO:", repr(e))

        return jsonify({
            'mensaje': 'Error al eliminar el administrativo',
            'detalle': str(e),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()
