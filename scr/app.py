
from flask import Flask, jsonify
from flask_cors import CORS

from blueprints.alumnos.routes import alumnos_bp
from blueprints.maestros.routes import maestros_bp
from blueprints.administrativos.routes import administrativos_bp
from config import config
from database import mysql

app = Flask(__name__)

app.config.from_object(config['development'])

CORS(app)
mysql.init_app(app)

app.register_blueprint(alumnos_bp)
app.register_blueprint(maestros_bp)
app.register_blueprint(administrativos_bp)

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return jsonify({
        'mensaje': 'Página no encontrada',
        'exito': False
    }), 404


@app.route('/')
def inicio():
    return jsonify({
        'mensaje': 'API funcionando correctamente',
        'exito': True
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
