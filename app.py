# app.py
from flask import g, Flask, render_template, render_template_string, request, redirect, url_for, session, g, send_from_directory
import sqlite3
import os
import psycopg2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Cargar variables locales; en Vercel se usan las variables configuradas en el proyecto.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "test.env"))

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "clave-segura-local")
DATABASE = os.environ.get("DATABASE_PATH", os.path.join(BASE_DIR, "sanagustin.db"))


# ---- Conexión a base de datos ----
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        # Vercel inyecta automáticamente POSTGRES_URL
        db = g._database = psycopg2.connect(os.environ.get("POSTGRES_URL"))
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


# ---- Función para mostrar el usuario en la barra ----
def render_with_user(filename, **kwargs):
    return render_template(filename, **kwargs)


# ---- Rutas HTML ----
@app.route("/")
def index():
    return render_with_user("index.html")


@app.route("/about")
@app.route("/about.html")
def about():
    return render_with_user("about.html")


@app.route("/proyectos")
@app.route("/proyectos.html")
def proyectos():
    return render_with_user("proyectos.html")


@app.route("/referencias", methods=["GET", "POST"])
@app.route("/referencias.html", methods=["GET", "POST"])
def referencias():
    db = get_db()
    
    # 1. Asegurar que la tabla existe
    db.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            comentario TEXT NOT NULL,
            calificacion REAL NOT NULL,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    db.commit()

    # 2. Si el usuario envía una nueva reseña
    if request.method == "POST":
        nombre = request.form.get("nombre", "Anónimo").strip()
        comentario = request.form.get("comentario", "").strip()
        try:
            calificacion = float(request.form.get("calificacion", 5.0))
        except ValueError:
            calificacion = 5.0
            
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO reviews (nombre, comentario, calificacion) VALUES (%s, %s, %s)", (nombre, comentario, calificacion))
        db.commit() # Importante: guarda los cambios
        cursor.close()

    # 3. Preparar los datos para mostrar
    filtro = request.args.get("stars")
    
    if filtro:
        # Si se hace clic en una barra, filtramos por la estrella (ej. 4 trae de 4.0 a 4.9)
        cursor = db.execute("SELECT nombre, comentario, calificacion, date(fecha) FROM reviews WHERE CAST(calificacion AS INTEGER) = ? ORDER BY fecha DESC", (int(filtro),))
    else:
        cursor = db.execute("SELECT nombre, comentario, calificacion, date(fecha) FROM reviews ORDER BY fecha DESC")
        
    reviews = cursor.fetchall()
    
    # Obtener todas las calificaciones para la estadística tipo Amazon
    cursor = db.execute("SELECT calificacion FROM reviews")
    all_ratings = [row[0] for row in cursor.fetchall()]
    total_reviews = len(all_ratings)
    
    promedio = sum(all_ratings) / total_reviews if total_reviews > 0 else 0.0
    
    # Contar cuántas reseñas hay por cada nivel de estrella para las barras de progreso
    estrellas_count = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    for r in all_ratings:
        nivel = int(r) # Convierte 4.5 a 4
        if nivel in estrellas_count:
            estrellas_count[nivel] += 1
            
    # Calcular el porcentaje para el CSS de cada barra
    estrellas_pct = {k: (v / total_reviews * 100 if total_reviews > 0 else 0) for k, v in estrellas_count.items()}

    return render_with_user("referencias.html", 
                            reviews=reviews, 
                            total=total_reviews, 
                            promedio=round(promedio, 1), 
                            pct=estrellas_pct,
                            filtro=filtro)


# contacto GET: sirve contacto.html; POST: procesa y envía correo
@app.route("/contacto", methods=["GET", "POST"])
@app.route("/contacto.html", methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        # Tomar campos del formulario
        nombre = request.form.get("nombre", "").strip()
        correo = request.form.get("correo", "").strip()
        telefono = request.form.get("telefono", "").strip()
        proyecto = request.form.get("proyecto", "").strip()
        mensaje = request.form.get("mensaje", "").strip()

        # Configuración del correo (lee de variables de entorno)
        SENDER_EMAIL = os.environ.get("EMAIL_USER")
        EMAIL_PASS = os.environ.get("EMAIL_PASS")
        RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL", "angelyoussef621@gmail.com")

        if not SENDER_EMAIL or not EMAIL_PASS:
            # Responder con un mensaje claro (no romper la app)
            return render_template_string("""
                <div style='text-align:center;margin-top:100px;font-family:Poppins,Arial,sans-serif;'>
                    <h3 style='color:#bfa888;'>⚠️ Error de configuración</h3>
                    <p>No está configurado el correo emisor. Revisa EMAIL_USER y EMAIL_PASS en test.env.</p>
                    <a href='/contacto' style='color:#bfa888;'>Volver</a>
                </div>
            """)

        # Asunto y HTML del mensaje
        subject = "Solicitud de contacto - {}".format(nombre or "Sin nombre")
        # Construyo el HTML con format() para evitar conflictos de llaves en f-strings
        html_content = """
        <html>
        <body style="font-family: Poppins, Arial, sans-serif; background:#f6f6f6; padding:20px;">
          <div style="max-width:700px;margin:20px auto;background:#ffffff;border-radius:8px;padding:22px;box-shadow:0 10px 30px rgba(0,0,0,0.08);">
            <h2 style="color:#bfa888;margin-bottom:6px;">Nueva solicitud de contacto</h2>
            <p style="color:#333;margin-top:0;">Has recibido un nuevo mensaje desde el formulario de contacto del sitio web.</p>
            <table style="width:100%;margin-top:12px;border-collapse:collapse;">
              <tr><td style="padding:8px;border-top:1px solid #eee;"><strong>Nombre</strong></td><td style="padding:8px;border-top:1px solid #eee;">{NOMBRE}</td></tr>
              <tr><td style="padding:8px;border-top:1px solid #eee;"><strong>Correo</strong></td><td style="padding:8px;border-top:1px solid #eee;">{CORREO}</td></tr>
              <tr><td style="padding:8px;border-top:1px solid #eee;"><strong>Teléfono</strong></td><td style="padding:8px;border-top:1px solid #eee;">{TELEFONO}</td></tr>
              <tr><td style="padding:8px;border-top:1px solid #eee;"><strong>Tipo de proyecto</strong></td><td style="padding:8px;border-top:1px solid #eee;">{PROYECTO}</td></tr>
            </table>

            <h4 style="margin-top:18px;margin-bottom:8px;color:#333;">Mensaje</h4>
            <div style="background:#fafafa;border:1px solid #f0f0f0;padding:12px;border-radius:6px;color:#333;">
              {MENSAJE}
            </div>

            <p style="font-size:12px;color:#777;margin-top:18px;">Enviado automáticamente desde el formulario de contacto — San Agustín Cocinas.</p>
          </div>
        </body>
        </html>
        """.format(
            NOMBRE=(nombre or "—"),
            CORREO=(correo or "—"),
            TELEFONO=(telefono or "—"),
            PROYECTO=(proyecto or "—"),
            MENSAJE=(mensaje.replace("\n", "<br>") if mensaje else "<em>Sin mensaje</em>")
        )

        # Crear mensaje MIME y adjuntar si corresponde
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Reply-To"] = correo if correo else SENDER_EMAIL
        msg.attach(MIMEText(html_content, "html"))

        # Adjuntar archivo si se envió (request.files)
        file = request.files.get("archivo")
        if file and getattr(file, "filename", None):
            try:
                from email.mime.base import MIMEBase
                from email import encoders
                part = MIMEBase("application", "octet-stream")
                payload = file.read()
                part.set_payload(payload)
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", 'attachment; filename="{}"'.format(file.filename))
                msg.attach(part)
            except Exception as e_attach:
                # Si falla adjuntar, imprimimos pero seguimos para evitar interrumpir el envío
                print("Error adjuntando archivo:", e_attach)

        # Enviar por SMTP (GMail)
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(SENDER_EMAIL, EMAIL_PASS)
                server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

            # Redirigir a /contacto?exito=1 para que el modal se muestre en el HTML
            return redirect(url_for("contacto") + "?exito=1")

        except Exception as e:
            # Imprimir para depuración en consola
            print("Error enviando correo:", type(e).__name__, e)
            # Responder con mensaje amigable al usuario (no mostrar trace completo)
            return render_template_string("""
                <div style='text-align:center;margin-top:100px;font-family:Poppins,Arial,sans-serif;'>
                    <h3 style='color:#bfa888;'>⚠️ Error al enviar el mensaje</h3>
                    <p>Ocurrió un problema al intentar enviar el correo. Por favor, intenta de nuevo más tarde.</p>
                    <a href='/contacto' style='color:#bfa888;'>Volver</a>
                </div>
            """)

    # GET: servir página
    return render_with_user("contacto.html")


@app.route("/admin")
def admin():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_with_user("admin.html")


# ---- LOGIN ----
@app.route("/login", methods=["GET", "POST"])
@app.route("/login.html", methods=["GET", "POST"])
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
    template_path = os.path.join(app.template_folder or "templates", filename)
    if filename.endswith(".html") and os.path.isfile(template_path):
        return render_with_user(filename)
    return "Página no encontrada", 404


if __name__ == "__main__":
    app.run(debug=True)

