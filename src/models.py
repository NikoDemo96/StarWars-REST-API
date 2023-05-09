from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
#Modelos para starwars API
#Despues de modificar/agregar un modelo a la BDD, correr pipenv run migrate y pipenv run upgrade.

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    eye_color = db.Column(db.String(30), nullable=True, default="N/A")
    hair_color = db.Column(db.String(30), nullable=True, default="N/A")
    gender = db.Column(db.String(30), nullable=True, default="N/A")
    birth_year = db.Column(db.String(30), nullable=True)
    height = db.Column(db.Integer, nullable=True)
    mass = db.Column(db.Integer, nullable=True)
    homeworld = db.Column(db.String(30), nullable=True)


    #Estos son metodos de visualizacion. Cuando yo pido algo a la base de datos, puedo especificar que me puede traer.
    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.name,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "height": self.height,
            "mass": self.mass,
            "homeworld": self.homeworld,
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    population = db.Column(db.Integer, nullable=True)
    climate = db.Column(db.String(30), nullable=True)
    terrain = db.Column(db.String(30), nullable=True)
    diameter = db.Column(db.Integer, nullable=True)
    rotation_period = db.Column(db.Integer, nullable=True)
    orbital_period = db.Column(db.Integer, nullable=True)
    gravity = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return '<Planet %r>' % self.name #no estoy seguro de si aqui va name o que
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population, 
            "climate": self.climate,
            "terrain": self.terrain,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
        }


