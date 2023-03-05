#sección de importaciones correspondietes para la construcción del modelo.
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #expresión regular utilizada para la validación del email
#Creación de la clase Usuario correspondiente a la tabla usuarios del BD.
class Usuario:
    def __init__(self,data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.nivel = data['nivel']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO usuarios (nombre,apellido,email,password,created_at) VALUES(%(nombre)s,%(apellido)s,%(email)s,%(password)s, NOW());"
        return connectToMySQL("odonto_reservaciones").query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios;"
        results = connectToMySQL("odonto_reservaciones").query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        results = connectToMySQL("odonto_reservaciones").query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        results = connectToMySQL("odonto_reservaciones").query_db(query,data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE usuarios SET nombre=%(nombre)s, apellido=%(apellido)s, email=%(email)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL("odonto_reservaciones").query_db(query,data)

    #método encargado de la validación de todos los campos para el registro del usuario.
    @staticmethod
    def validate_register(usuario):
        is_valid = True
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        results = connectToMySQL("odonto_reservaciones").query_db(query,usuario)
        if len(results) >= 1:
            flash("Este correo ya existe.","register")
            is_valid=False
        if not EMAIL_REGEX.match(usuario['email']):
            flash("Email inválido.","register")
            is_valid=False
        if len(usuario['nombre']) < 3:
            flash("El nombre debe contener por lo menos 3 caracteres.","register")
            is_valid= False
        if len(usuario['apellido']) < 3:
            flash("El apellido debe contener por lo menos 3 caracteres.","register")
            is_valid= False
        if len(usuario["password"]) < 8:
            flash("La contraseña debe contener por lo menos 8 caracteres.","register")
            is_valid= False
        if usuario['password'] != usuario['confirm_password']:
            flash("Las contraseñas deben coincidir.","register")
            is_valid = False
        return is_valid
    
    #método utilizado para la validación del usuario en la actualización de su cuenta.
    @staticmethod
    def validate_user(usuario):
        is_valid = True
        if not EMAIL_REGEX.match(usuario['email']):
            flash("Email inválido","edit")
            is_valid=False
        if len(usuario['nombre']) < 3:
            flash("El nombre debe contener por lo menos 3 caracteres.","edit")
            is_valid= False
        if len(usuario['apellido']) < 3:
            flash("El apellido debe contener por lo menos 3 caracteres.","edit")
            is_valid= False
        return is_valid