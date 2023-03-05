#En esta sección se hacen todas las importaciones pertinentes para la construcción
#del controlador del modelo reservacion.
from flask_app import app
from flask import render_template,redirect,session,request, flash
from flask_app.models.reservacion import Reserva

#corresponde a la creación de una nueva reserva.
@app.route("/new", methods=["GET","POST"])
def create_reservation():
    if "user_id" not in session: #verifica que el usuario esté logeado.
        return redirect("/logout")
    if request.method == "POST":
        if not Reserva.validate_reservation(request.form): #se valida los campos cargados para la reserva.
            return redirect("/new")
        data = {
        "fech_hor": request.form["fech_hor"],
        "usuario_id": session["user_id"]
        }
        Reserva.save(data)
        flash("Tu reserva ha sido registrada con éxito.","reserva_hecha")
        return redirect("/new")
    return render_template("reservation.html", reservas=Reserva.get_all())

#corresponde a la viasualización que el admin tendrá de todas las reservas hechas.
@app.route("/show_reservations")
def show_reservation():
    if "user_id" not in session: #verifica que el usuario esté logeado.
        return redirect("/logout")
    return render_template("show_reservation.html", reservas=Reserva.get_all_user_reservation())

#corresponde a la eliminación de una reserva de la BD, ésta función solo la puede realizar el usuario logeado con sus propias reservas.
@app.route("/delete/<int:id>")
def delete(id):
    if "user_id" not in session: #verifica que el usuario esté logeado.
        return redirect("/logout")
    data = {
        "id": id
    }
    Reserva.destroy(data)
    return redirect("/user/account")