from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from psycopg2 import connect
from datetime import date
app = Flask(__name__)



# Configuración de la base de datos
USER = "postgres"
PASSWORD = "adminpg"
HOST = "localhost"
PORT = 5433
DATABASE = "postgres"


    
# Definir la URI de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   # Para evitar un warning

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cedula_identidad = db.Column(db.String(255), unique=True, nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    primer_apellido = db.Column(db.String(255), nullable=False)
    segundo_apellido = db.Column(db.String(255), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)

with app.app_context():
    db.create_all()



@app.route('/test')
def test():
    try:
        db.session.query("1").from_statement("SELECT 1").all()
        return 'Conexión exitosa', 200
    except Exception as e:
        return str(e), 500



@app.route('/usuarios', methods=['POST'])
def create_user():
    # 1. Recibe los datos del usuario desde la solicitud
    data = request.get_json()

    # 2. Valida los datos
    if not data:
        return jsonify({"message": "No se proporcionaron datos"}), 400
    required_fields = ["cedula_identidad", "nombre", "primer_apellido", "segundo_apellido", "fecha_nacimiento"]
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"Falta el campo {field}"}), 400

    # Verifica si el usuario ya existe
    existing_user = Usuario.query.filter_by(cedula_identidad=data['cedula_identidad']).first()
    if existing_user:
        return jsonify({"message": "Un usuario con esta cédula ya existe"}), 400

    # 3. Inserta el usuario en la base de datos
    try:
        nuevo_usuario = Usuario(
            cedula_identidad=data['cedula_identidad'],
            nombre=data['nombre'],
            primer_apellido=data['primer_apellido'],
            segundo_apellido=data['segundo_apellido'],
            fecha_nacimiento=data['fecha_nacimiento']
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": f"Error al crear el usuario: {str(e)}"}), 500

    # 4. Devuelve una respuesta apropiada
    return jsonify({"message": "Usuario creado exitosamente", "usuario_id": nuevo_usuario.id}), 201

@app.route('/usuarios', methods=['GET'])
def get_users():
    usuarios = Usuario.query.all()
    response = [{
        "id": usuario.id,
        "cedula_identidad": usuario.cedula_identidad,
        "nombre": usuario.nombre,
        "primer_apellido": usuario.primer_apellido,
        "segundo_apellido": usuario.segundo_apellido,
        "fecha_nacimiento": usuario.fecha_nacimiento.strftime('%Y-%m-%d')
    } for usuario in usuarios]
    return jsonify(response)


@app.route('/usuarios/<int:id_usuario>', methods=['GET'])
def get_user(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return jsonify({"message": "Usuario no encontrado"}), 404
    response = {
        "id": usuario.id,
        "cedula_identidad": usuario.cedula_identidad,
        "nombre": usuario.nombre,
        "primer_apellido": usuario.primer_apellido,
        "segundo_apellido": usuario.segundo_apellido,
        "fecha_nacimiento": usuario.fecha_nacimiento.strftime('%Y-%m-%d')
    }
    return jsonify(response)



@app.route('/usuarios/<int:id_usuario>', methods=['PUT'])
def update_user(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return jsonify({"message": "Usuario no encontrado"}), 404
    
    data = request.get_json()
    usuario.cedula_identidad = data.get('cedula_identidad', usuario.cedula_identidad)
    usuario.nombre = data.get('nombre', usuario.nombre)
    usuario.primer_apellido = data.get('primer_apellido', usuario.primer_apellido)
    usuario.segundo_apellido = data.get('segundo_apellido', usuario.segundo_apellido)
    usuario.fecha_nacimiento = data.get('fecha_nacimiento', usuario.fecha_nacimiento)
    
    db.session.commit()
    return jsonify({"message": "Usuario actualizado exitosamente"})



@app.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
def delete_user(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return jsonify({"message": "Usuario no encontrado"}), 404
    
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"message": "Usuario eliminado exitosamente"})

@app.route('/usuarios/promedio-edad', methods=['GET'])
def get_average_age():
    # 1. Obtener todas las fechas de nacimiento
    nacimientos = [u.fecha_nacimiento for u in Usuario.query.all()]
    
    # 2. Calcular la edad para cada usuario
    edades = [(date.today() - nacimiento).days // 365 for nacimiento in nacimientos]
    
    # 3. Calcular el promedio
    promedio = sum(edades) / len(edades) if edades else 0
    
    return jsonify({"promedioEdad": promedio})

@app.route('/estado', methods=['GET'])
def get_status():
    return jsonify({
        "nameSystem": "api-users",
        "version": "0.0.1",
        "developer": "Alejandro Muñoz Castro",
        "email": "alembol9@gmail.com"
    })

if __name__ == '__main__':
    app.run(debug=True)
