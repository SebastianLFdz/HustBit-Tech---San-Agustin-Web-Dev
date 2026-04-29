from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv("test.env")

app = Flask(__name__)
app.secret_key = "clave_segura_2025"
DATABASE = "sanagustin.db"

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

# ---- Rutas HTML ----
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/referencias")
def referencias():
    return render_template("referencias.html")

@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        correo = request.form.get("correo", "").strip()
        telefono = request.form.get("telefono", "").strip()
        proyecto = request.form.get("proyecto", "").strip()
        mensaje = request.form.get("mensaje", "").strip()

        SENDER_EMAIL = os.environ.get("EMAIL_USER")
        EMAIL_PASS = os.environ.get("EMAIL_PASS")
        RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL", "angelyoussef621@gmail.com")

        if not SENDER_EMAIL or not EMAIL_PASS:
            return render_template("contacto.html", error_correo="Error de configuración de servidor.")

        subject = f"Solicitud de contacto - {nombre or 'Sin nombre'}"
        html_content = f"""
        <html>
        <body style="font-family: Poppins, Arial, sans-serif; background:#f6f6f6; padding:20px;">
          <div style="max-width:700px;margin:20px auto;background:#ffffff;border-radius:8px;padding:22px;box-shadow:0 10px 30px rgba(0,0,0,0.08);">
            <h2 style="color:#bfa888;margin-bottom:6px;">Nueva solicitud de contacto</h2>
            <table style="width:100%;margin-top:12px;border-collapse:collapse;">
              <tr><td style="padding:8px;border-top:1px solid #eee;"><strong>Nombre</strong></td><td style="padding:8px;border-top:1px solid #eee;">{nombre}</td></tr>
              <tr><td style="padding:8px;border-top:1px solid #eee;"><strong>Correo</strong></td><td style="padding:8px;border-top:1px solid #eee;">{correo}</td></tr>
              <tr><td style="padding:8px;border-top:1px solid #eee;"><strong>Teléfono</strong></td><td style="padding:8px;border-top:1px solid #eee;">{telefono}</td></tr>
              <tr><td style="padding:8px;border-top:1px solid #eee;"><strong>Proyecto</strong></td><td style="padding:8px;border-top:1px solid #eee;">{proyecto}</td></tr>
            </table>
            <h4 style="margin-top:18px;margin-bottom:8px;color:#333;">Mensaje</h4>
            <div style="background:#fafafa;border:1px solid #f0f0f0;padding:12px;border-radius:6px;color:#333;">
              {mensaje.replace(chr(10), '<br>')}
            </div>
          </div>
        </body>
        </html>
        """

        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Reply-To"] = correo if correo else SENDER_EMAIL
        msg.attach(MIMEText(html_content, "html"))

        file = request.files.get("archivo")
        if file and getattr(file, "filename", None):
            try:
                from email.mime.base import MIMEBase
                from email import encoders
                part = MIMEBase("application", "octet-stream")
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f'attachment; filename="{file.filename}"')
                msg.attach(part)
            except Exception as e:
                print("Error adjuntando archivo:", e)

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(SENDER_EMAIL, EMAIL_PASS)
                server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
            return redirect(url_for("contacto", exito=1))
        except Exception as e:
            print("Error enviando correo:", e)
            return render_template("contacto.html", error_correo="Error al enviar el mensaje. Intenta de nuevo.")

    return render_template("contacto.html")

@app.route("/admin")
def admin():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("admin.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]

        db = get_db()
        cursor = db.execute("SELECT * FROM usuarios WHERE usuario = ? AND password = ?", (usuario, password))
        user = cursor.fetchone()

        if user:
            session["usuario"] = user[1]
            session["username"] = user[2]
            return redirect(url_for("admin"))
        else:
            return render_template("login.html", error="Credenciales incorrectas")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)