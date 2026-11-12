import os
import time
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv 

load_dotenv()

app = Flask(__name__)

db_url = os.getenv('DATABASE_URL', '')
if db_url.startswith('postgresql://'):
    db_url = db_url.replace('postgresql://', 'postgresql+psycopg://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app.models import Contacto
from app.routes.contacto import contacto_bp

with app.app_context():
    for intento in range(10):
        try:
            db.create_all()
            break
        except OperationalError:
            time.sleep(3)

app.register_blueprint(contacto_bp, url_prefix='/contactos')

@app.route('/')
def index():
    contactos = Contacto.query.all()
    return render_template('index.html', contactos=contactos)