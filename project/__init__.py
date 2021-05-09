import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# App Setup

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


# Database Setup

basedir = os.path.abspath(os.path.dirname(__file__))
migration_dir = os.path.join(basedir, 'migrations')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db, directory=migration_dir)


# Blueprint Registration

from project.views import core

app.register_blueprint(core)
