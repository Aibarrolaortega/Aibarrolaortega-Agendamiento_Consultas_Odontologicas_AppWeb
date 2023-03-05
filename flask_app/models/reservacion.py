#sección de importaciones correspondietes para la construcción del modelo.
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
#Creación de la clase Reserva correspondiente a la tabla reservas del BD.
class Reserva:
    def __init__(self, data):
        self.id = data["id"]
        self.fech_hor = data["fech_hor"]
        self.usuario_id = data['usuario_id']
        self.created_at = data['created_at']
        self.updated_at = data["updated_at"]
        self.reserva_usuario = None #atributo utilizado para la carga de las reservas junto con los datos del usuario que ha hecho la reserva correspondiente.

    @classmethod
    def save(cls,data):
        query = "INSERT INTO reservas (fech_hor, usuario_id) VALUES (%(fech_hor)s,%(usuario_id)s);"
        return connectToMySQL("odonto_reservaciones").query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM reservas;"
        results = connectToMySQL("odonto_reservaciones").query_db(query)
        reservas = []
        for row in results:
            reservas.append( cls(row))
        return reservas
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM reservas WHERE id = %(id)s;"
        return connectToMySQL("odonto_reservaciones").query_db(query,data)

    #este método tiene como fin lograr la optención de todas las reservas hechas por el usuario en cuestión.
    @classmethod
    def get_all_oneuser(cls, data):
        query = "SELECT * FROM reservas WHERE usuario_id = %(id)s ;"
        results =  connectToMySQL("odonto_reservaciones").query_db(query, data)
        all_reservations = []
        for row in results:
            all_reservations.append( cls(row) )
        return all_reservations
    
    #aquí se recupera todas las reservas junto con los datos del usuario que ha hecho. Para el admin
    @classmethod
    def get_all_user_reservation(cls):
        query = "SELECT * FROM reservas LEFT JOIN usuarios ON usuarios.id = reservas.usuario_id;"
        results = connectToMySQL("odonto_reservaciones").query_db(query)
        reservas = []
        if not results:
            return results
        for row in results:
            usuario_data = {
                "id": row["usuarios.id"],
                "nombre": row["nombre"],
                "apellido": row["apellido"],
                "email": row["email"],
                "password": row["password"],
                "nivel": row["nivel"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            }
            reserva = cls(row)
            reserva.reserva_usuario = user.Usuario(usuario_data)
            reservas.append(reserva)
        return reservas
    
    #validación de la fecha y hora escogida por el usuario.
    @staticmethod
    def validate_reservation(usuario):
        is_valid = True
        query = "SELECT * FROM reservas WHERE fech_hor = %(fech_hor)s;"
        results = connectToMySQL("odonto_reservaciones").query_db(query,usuario)
        if len(results) >= 1:
            flash("Este turno ya fue reservado, escoge otro.","reservation")
            is_valid=False
        return is_valid