
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "qwertyuiolkjhgfdszsdvbn"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["UPLOAD_FOLDER"] = "static"



db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
