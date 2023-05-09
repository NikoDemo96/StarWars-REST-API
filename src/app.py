"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#Trabajar a partir de aqui para la tarea
@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


# Todos los personajes
@app.route("/character", methods=["GET"])
def get_all_characters():
    character_list = Character.query.all()
    serialized_characters = [character.serialize() for character in character_list]
    return jsonify({"characters": serialized_characters})

@app.route("/character", methods=["POST"])
def add_character():
    body = request.json
    body_name = body.get("name", None)
    body_eye_color = body.get("eye_color", None)
    body_hair_color = body.get("hair_color", None)
    body_gender = body.get("gender", None)

    #Validar para verificar que todos los campos eestan siendo enviados. Si falta un campo, manda error.
    if body_name is None or body_eye_color is None or body_hair_color is None or body_gender is None:
        return {"error": f"todos los campos son requeridos"}, 400

    #Validacion para ver si el personaje ya existe
    character_exists = Character.query.filter_by(name=body_name).first()
    if character_exists:
        return {"Error": f"Ya existe un personaje con el nombre: {body_name}"}
    
    #Creando una nueva instancia del modelo para agregar un personaje nuevo
    #Una instancia en la clase character es Han Solo, Luke, etc. Una nueva instancia es un nuevo elemento dentro de la clase.
    new_character = Character(name=body_name, eye_color=body_eye_color, hair_color=body_hair_color, gender=body_gender)

    db.session.add(new_character)

    #Try and catch para evitar errores en la base de datos
    #Si en parte de mi Try hay un commit, en mi Exception tiene que haber un rollback.
    #En todos los endpoints que impliquen crear: Meter el commit dentro del try y el rollback dentro del Exception.
    try: 
        db.session.commit()
        return jsonify({"data": f"Personaje {body_name} creado con exito"}), 201
    
    #Si hay un error, atrapo el error y retorno el error.
    except Exception as error:
        db.session.rollback()
        return {"error": error}, 500


#Hacemos una ruta dinamica para buscar por ID  aun personaje en especifico
@app.route("/character/<int:id>", methods=["GET"])
def get_character_by_id(id):
    character_exists = Character.query.filter_by(id=id).first()
    if not character_exists:
        return {"error": "No existe un personaje con ese id"}, 404
    
    return jsonify ({"personaje": character_exists.serialize()})

#Todos los planetas
@app.route("/planets", methods=["GET"])
def get_planets():
    # Model.query.all() --> trae todos los elementos
    planets = Planet.query.all() # Trae todos
    # nueva_lista = [item.serialize() for item in list]
    print(planets)
    serialized_planets = [planet.serialize() for planet in planets] # Comprension de listas
    print(serialized_planets)
    return jsonify({"data": serialized_planets}) # Ahora me trae una lista con 2 planetas

#Trae UN planeta
@app.route("/planet", methods=['GET'])
def get_planet():
    test_id = 1
    #Model.query.filter_by(campovalor)
    planet = Planet.query.filter_by(id=test_id).one_or_none()
    print("serializado")
    print(planet.serialize())
    print("sin serializar")
    print(planet)
    return jsonify({"data": planet.serialize()})

@app.route("/planet", methods=["POST"])
def add_planet():
    # Que campos necesito para crear un planeta
    # --> Body = {name, etc}
    body = request.json #Busco el json del body
    #Validaciones:
    body_name = body.get("name", None) # Extraigo el name del body con el metodo get. El
    #el metodo get va a buscar una propiedad que se llame "name" y sino existe, le pone "none". Si no existe la variable, vale none
    #Le colocamos el valor por defecto "none" para poder atajar mi error con un if. Entonces estoy agregando la validacion del campo.
    #Estoy agregando que como minimo el "name" exista.
    #le colocamos un valor por defecto para hacer un if name 
    if body_name is None:
        return {"error": "Todos los campos requeridos"}, 400

    #Otra validacion para ver si ya existe un planeta con ese nombre
    planet_exists = Planet.query.filter_by(name=body_name).first()
    if planet_exists:
        return{"Error": f"Ya existe un planeta con el nombre: {body_name}"}

    # Creando una nueva instancia del modelo.
    new_planet = Planet(name=body_name) 
    
    db.session.add(new_planet) # Le estoy agregando a mi sesion de base de datos un planeta nuevo. Cuando uno corre el servidor y se va a hacer una consulta a la base de datos, el crea algo que se llama sesion. Y uno accede a esa sesion atra vez de db.session.
    
    db.session.commit() # Con este comando, guardamos el cambio.

    print(body)
    #Luego de usar session.add y session.commit, uno suele regresar un jsonify
    #Status 201 --> Es para cuando uno crea algo en la base de datos
    return jsonify({"data": f"Planeta {body_name} creado con exito"}), 201



#Termina de trabajar tarea aqui

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
