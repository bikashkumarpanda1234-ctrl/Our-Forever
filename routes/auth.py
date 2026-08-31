from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    request,
    flash
)

from models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    # Already logged in
    if session.get("logged_in"):
        return redirect(url_for("home.index"))

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Please enter username and password.", "error")
            return render_template("auth/login.html")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):

            session.clear()

            session["logged_in"] = True
            session["user_id"] = user.id
            session["username"] = user.username

            return redirect(url_for("home.index"))

        flash("Invalid username or password.", "error")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():

    session.clear()

    return render_template("auth/logout.html")