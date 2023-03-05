#En esta sección se hacen todas las importaciones pertinentes para la construcción
#del controlador del modelo user.
from flask_app import app
from flask import render_template,redirect,session,request, flash
from flask_app.models.user import Usuario
from flask_app.models.reservacion import Reserva
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app) #creación del objeto bcrypt para realizar el hash.

@app.route('/')
@app.route('/register', methods=['GET', 'POST']) #corresponde al registro.
def register():
    if request.method == "POST":
        if Usuario.validate_register(request.form): #se valida los campos del registro, si algo sale mal se vuelve a la pagina pricipal.
            data = {
                "nombre": request.form["nombre"],
                "apellido": request.form["apellido"],
                "email": request.form["email"],
                "password": bcrypt.generate_password_hash(request.form["password"])
            }
            id = Usuario.save(data) #se camptura el id del usuario registrado.
            session["usuario_id"] = id #se le asiga a la sesión el id capturado.
            return redirect('/login')
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST']) #corresponde al login
def login():
    if request.method == "POST":
        user = Usuario.get_by_email(request.form) #se verifica que el email exista.
        if not user:
            flash("Correo/Contraseña inválida.","login")
            return redirect('/login')
        if not bcrypt.check_password_hash(user.password, request.form['password']): #se verifica que la contraseña esté bien.
            flash("Correo/Contraseña inválida.","login")
            return redirect('/login')
        session["user_id"] = user.id
        return redirect("/dashboard")
    return render_template('login.html')

@app.route("/dashboard") #corresponde a la primera paágina una vez que se logea.
def dashboard():
    if "user_id" not in session: #verifica que el usuario esté logeado.
        return redirect("/logout")
    data = {
        "id": session["user_id"]
    }
    return render_template("dashboard.html",usuario=Usuario.get_by_id(data))

@app.route("/user/account", methods=["GET","POST"]) #corresponde a la página donde se realizan ediciones de lo que corresponde al usuario logeado.
def update_user():
    if "user_id" not in session: #verifica que el usuario esté logeado.
        return redirect("/logout")
    usuario_data = {
        "id": session["user_id"]
    }
    if request.method == "POST":
        if not Usuario.validate_user(request.form): #se valida la carga de los campos para la actualización.
            return redirect("/user/account")
        data = {
        "nombre": request.form["nombre"],
        "apellido": request.form["apellido"],
        "email": request.form["email"],
        "id":session["user_id"]
        }
        Usuario.update(data)
        return redirect("/user/account")
    return render_template("account.html", reservas=Reserva.get_all_oneuser(usuario_data), usuario=Usuario.get_by_id(usuario_data))

#corresponde al cierre de sesión.
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")