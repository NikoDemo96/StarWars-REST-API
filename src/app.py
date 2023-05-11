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
from models import db, User, Planet, Character, Favorites
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
    
# Get all users
@app.route("/users", methods=["GET"]) 
def get_all_users():
    user_list = User.query.all()
    serialized_users = [user.serialize() for user in user_list]
    return jsonify({"users": serialized_users})

#Get all the favorites in general.
@app.route("/users/favoritesall", methods=["GET"]) 
def get_all_favorites():
    favorites_list = Favorites.query.all()
    serialized_favorites = [favorites.serialize() for favorites in favorites_list]
    return jsonify ({"favorites": serialized_favorites})

#Get all the favorites that belong to the current user.
@app.route("/users/favorites", methods=["GET"]) 
def get_one_favorite(user_id):
    favorites_exists = Favorites.query.filter_by(user_id=user_id).first()
    if not character_exists:
        return{"error": "No existe un favorito para ese id"}
    return jsonify ({"favorites": favorites_exists.serialize()})

#Add a new favorite planet to the current user with the planet id = planet_id.
@app.route("/favorite/planets/<int:planet_id>", methods=["POST"]) 
def add_favorite_planet(planet_id):
    body = request.json
    user_id = body.get("user_id", None)
    if not user_id:
        return {"error": "todos los campos son requeridos"}, 400
    favorites_exists = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    print(favorites_exists)
    if favorites_exists:
        return{"error": "This planet already exists"}, 400

    new_favorites = Favorites(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorites)
    
    try:
        db.session.commit()
        return jsonify({"msg": "Favorite planet created"}), 201
    except Exception as error:
        db.session.rollback()
        return jsonify({"msg":"error"})


#Add new favorite people to the current user with the people id = people_id.
@app.route("/favorite/people/<int:character_id>", methods=["POST"]) 
def add_favorite_character(character_id):
    body = request.json
    user_id = body.get("user_id", None)
    if not user_id:
        return {"error": "todos los campos son requeridos"}, 400
    favorites_exists = Favorites.query.filter_by(user_id=user_id, character_id=character_id).first()
    print(favorites_exists)
    if favorites_exists:
        return{"error": "This character already existts"}, 400
    
    new_favorites = Favorites(user_id=user_id, character_id=character_id)
    db.session.add(new_favorites)

    try:
        db.session.commit()
        return jsonify({"msg":"Favorite character created"}), 201
    except Exception as error:
        db.session.rollback()
        return jsonify({"msg":"error"})

# Delete favorite planet with the id = planet_id.
@app.route("/favorite/planet/<int:planet_id>/<int:user_id>", methods=["DELETE"]) 
def delete_favorite_planet(planet_id, user_id):
    favorite_delete = Favorites.query.filter_by(planet_id=planet_id, user_id=user_id).first()
    if not favorite_delete:
        return{"error": "Favorite planet doesn't exist"}, 400

    db.session.delete(favorite_delete)
    try:
        db.session.commit()
        return {"msg": "Favorite planet deleted"}, 200
    except Exception as error:
        db.session.rollback()
        return jsonify({"error": error})
    
# Delete favorite people with the id = people_id.
@app.route("/favorite/people/<int:character_id>/<int:user_id>", methods=["DELETE"]) 
def delete_favorite_people(character_id, user_id):
    favorite_delete = Favorites.query.filter_by(character_id=character_id, user_id=user_id).first()
    if not favorite_delete:
        return{"error": "Favorite character doesn't exist"}, 400

    db.session.delete(favorite_delete)
    try:
        db.session.commit()
        return{"msg": "Favorite character deleted"}, 200
    except Exception as error:
        db.session.rollback()
        return jsonify({"error": error})
    
# Get all the characters
@app.route("/people", methods=["GET"])
def get_all_characters():
    character_list = Character.query.all()
    serialized_characters = [character.serialize() for character in character_list]
    return jsonify({"characters": serialized_characters})

# Get one single characters information
@app.route("/people/<int:id>", methods=["GET"])
def get_character_by_id(id):
    character_exists = Character.query.filter_by(id=id).first()
    if not character_exists:
        return {"error": "No existe un personaje con ese id"}, 404
    
    return jsonify ({"character": character_exists.serialize()})

#Todos los planetas
@app.route("/planets", methods=["GET"])
def get_all_planets():
    # Model.query.all() --> trae todos los elementos
    planets = Planet.query.all() # Trae todos
    # nueva_lista = [item.serialize() for item in list]
    print(planets)
    serialized_planets = [planet.serialize() for planet in planets] # Comprension de listas
    print(serialized_planets)
    return jsonify({"planet": serialized_planets}) # Ahora me trae una lista con 2 planetas

#Trae UN planeta
@app.route("/planets/<int:id>", methods=['GET'])
def get_planet_by_id(id):
    #Model.query.filter_by(campovalor)
    planet_exists = Planet.query.filter_by(id=id).first()
    if not planet_exists:
        return {"error": "No existe un planeta con ese id"}, 404

    return jsonify({"planet": planet_exists.serialize()})


# Add Character

@app.route("/people", methods=["POST"])
def add_character():
    body = request.json
    body_name = body.get("name", None)
    body_eye_color = body.get("eye_color", None)
    body_hair_color = body.get("hair_color", None)
    body_gender = body.get("gender", None)
    body_birth_year = body.get("birth_year", None)
    body_height = body.get("height", None)
    body_mass = body.get("mass", None)
    body_homeworld = body.get("homeworld", None)

    #Validar para verificar que todos los campos eestan siendo enviados. Si falta un campo, manda error.
    if body_name is None or body_eye_color is None or body_hair_color is None or body_gender is None or body_birth_year is None or body_height is None or body_mass is None or body_homeworld is None:
        return {"error": f"todos los campos son requeridos"}, 400

    #Validacion para ver si el personaje ya existe
    character_exists = Character.query.filter_by(name=body_name).first()
    if character_exists:
        return {"Error": f"Ya existe un personaje con el nombre: {body_name}"}
    
    #Creando una nueva instancia del modelo para agregar un personaje nuevo
    #Una instancia en la clase character es Han Solo, Luke, etc. Una nueva instancia es un nuevo elemento dentro de la clase.
    new_character = Character(name=body_name, eye_color=body_eye_color, hair_color=body_hair_color, gender=body_gender, birth_year=body_birth_year, height=body_height, mass=body_mass, homeworld=body_homeworld)

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
    return jsonify({"planet": f"Planeta {body_name} creado con exito"}), 201





#Termina de trabajar tarea aqui

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
