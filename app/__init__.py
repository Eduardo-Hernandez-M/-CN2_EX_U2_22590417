import os
import time
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv 

# Cargar las variables de entorno
load_dotenv()

# Crear instancia
app = Flask(__name__)

# Obtener URL y asegurar que use el driver psycopg (v3) instalado en requirements.txt
db_url = os.getenv('DATABASE_URL', '')
if db_url.startswith('postgresql://'):
    db_url = db_url.replace('postgresql://', 'postgresql+psycopg://', 1)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Importar modelos para que SQLAlchemy los reconozca
from app.models import Contacto

# Importar y registrar blueprints
from app.routes.contacto import contacto_bp

# Crear las tablas esperando a que el contenedor Postgres del Worker termine de iniciar
with app.app_context():
    for intento in range(10):
        try:
            db.create_all()
            print("Conexión exitosa a PostgreSQL y tablas verificadas.")
            break
        except OperationalError as e:
            print(f"Esperando a la base de datos en el Worker (intento {intento + 1}/10)...")
            time.sleep(3)

app.register_blueprint(contacto_bp, url_prefix='/contactos')

# Ruta principal home
@app.route('/')
def index():
    contactos = Contacto.query.all()
    return render_template('index.html', contactos=contactos)