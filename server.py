from flask_app import app #se importa el objeto app de la clase Flask
from flask_app.controllers import users, reservaciones  #se importan los controladores del modulo flask_app

if __name__=="__main__":
    app.run(debug=True)