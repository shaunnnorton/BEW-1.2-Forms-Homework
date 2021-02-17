from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from grocery_app.config import Config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

bcrypt = Bcrypt(app)

manager = LoginManager() 
manager.login_view='auth.login'
manager.init_app(app)



db = SQLAlchemy(app)

from grocery_app.routes import main, auth

from grocery_app.models import User

@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

bcrypt = Bcrypt(app)

app.register_blueprint(main)
app.register_blueprint(auth)

with app.app_context():
    db.create_all()
