from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from app.config import BaseConfig
from flask_jwt_extended import JWTManager


app = Flask(__name__)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config.from_object(BaseConfig)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'


from app import endpoints
