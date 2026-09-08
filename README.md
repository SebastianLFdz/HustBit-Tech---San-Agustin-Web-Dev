# San Agustín Cocinas

Sitio web Flask de San Agustín Cocinas.

## Ejecución local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

La aplicación queda disponible en `http://127.0.0.1:5000`.

## Despliegue en Vercel

El proyecto incluye `vercel.json` y `api/index.py`, que indican a Vercel que debe ejecutar la aplicación Flask. En el proyecto de Vercel configura estas variables de entorno:

- `SECRET_KEY`: una clave aleatoria para las sesiones.
- `EMAIL_USER`, `EMAIL_PASS` y, opcionalmente, `RECEIVER_EMAIL`: para el formulario de contacto.

No es necesario establecer un framework desde el panel: Vercel detecta la función Python definida en `api/index.py`.

La aplicación conserva SQLite para desarrollo local. Vercel no ofrece almacenamiento persistente en el sistema de archivos de una función serverless, así que las altas de reseñas y cualquier cambio en `sanagustin.db` no deben considerarse permanentes en producción. Para conservar esos datos hay que conectar una base de datos externa antes de habilitar esa funcionalidad en producción.