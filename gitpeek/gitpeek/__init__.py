'''Package initializer'''
from flask import Flask # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from dotenv import load_dotenv # type: ignore
import os


load_dotenv()
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")


app = Flask(__name__)
app.config['SECRET_KEY'] = '53a34e7bc708d253a8bd7ab2707947f073c2da9db774e9f2e1b84cf1c9604760'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://gitspeakadmin:DB146eeeagp#@localhost:5432/gitspeak"

# Create database instance
db = SQLAlchemy(app)

# from gitpeek import routes
from gitpeek import routes