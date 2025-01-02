'''Package initializer'''
from flask import Flask # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore


app = Flask(__name__)
app.config['SECRET_KEY'] = '53a34e7bc708d253a8bd7ab2707947f073c2da9db774e9f2e1b84cf1c9604760'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# Create database instance
db = SQLAlchemy(app)

from gitpeek import routes
