from flask import Flask, render_template_string, request, redirect, url_for, session, g, send_from_directory
import sqlite3, os

app = Flask(__name__)
app.secret_key = "clave_segura_2025"
DATABASE = "sanagustin.db"

# ---- Conexión a base de datos ----
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


# ---- Función para mostrar el usuario en la barra ----
def render_with_user(filename, **kwargs):
    """Lee el HTML plano y reemplaza el botón de login si hay sesión activa"""
    with open(filename, encoding="utf-8") as f:
        html = f.read()

    if "usuario" in session:
        reemplazo = f'''
        <li class="nav-item d-flex align-items-center">
          <img src="static/img/user-icon.png" alt="Usuario" style="width:28px;height:28px;border-radius:50%;margin-right:8px;">
          <a class="nav-link" href="/admin">{session["usuario"]}</a>
        </li>
        '''
        # sustituir el botón de login sin eliminar nada más
        html = html.replace(
            '<li class="nav-item"><a class="nav-login', 
            reemplazo + '\n<li style="display:none" class="nav-item"><a class="nav-login'
        )

    return render_template_string(html, **kwargs)


# ---- Rutas HTML ----
@app.route("/")
def index():
    return render_with_user("index.html")

@app.route("/about")
def about():
    return render_with_user("about.html")

@app.route("/referencias")
def referencias():
    return render_with_user("referencias.html")

@app.route("/contacto")
def contacto():
    return render_with_user("contacto.html")

@app.route("/admin")
def admin():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_with_user("admin.html")


# ---- LOGIN ----
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]

        db = get_db()
        cursor = db.execute("SELECT * FROM usuarios WHERE usuario = ? AND password = ?", (usuario, password))
        user = cursor.fetchone()

        if user:
            session["usuario"] = user[1]   # nombre
            session["username"] = user[2]  # usuario
            return redirect(url_for("admin"))
        else:
            return render_with_user("login.html", error="Credenciales incorrectas")

    return render_with_user("login.html")


# ---- LOGOUT ----
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# ---- Archivos estáticos ----
@app.route("/static/<path:path>")
def static_files(path):
    return send_from_directory("static", path)

@app.route("/Bootstrap/<path:path>")
def bootstrap_files(path):
    return send_from_directory("Bootstrap", path)


# ---- Fallback para cualquier otra página HTML ----
@app.route("/<path:filename>")
def serve_html(filename):
    if filename.endswith(".html") and os.path.exists(filename):
        return render_with_user(filename)
    return "Página no encontrada", 404


if __name__ == "__main__":
    app.run(debug=True)
