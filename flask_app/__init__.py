from flask import Flask #se importa la clase Flask del modulo flask
app = Flask(__name__) #se instancia el objeto app de la clase Flask
app.secret_key = "jdfaljka%&$#" #se establece una clave secreta para el app