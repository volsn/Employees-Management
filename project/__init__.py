"""
Top level init file that configures the project and puts everything together
"""
import os
import logging
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from flask_restful import Resource, Api


# App Setup

app = Flask(__name__)
version = '0.0.1'
load_dotenv()
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
basedir = os.path.abspath(os.path.dirname(__file__))


# Creating Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(name)s:%(levelname)s:%(message)s')

file_handler = logging.FileHandler(os.path.join(basedir, 'logs', 'app.log'))
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger.info('Logger created.')


# Database Setup
migration_dir = os.path.join(basedir, 'migrations')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite://db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db, directory=migration_dir)


# Testing Database connection
try:
    db.engine.execute('SELECT 1')
except OperationalError:
    logger.error('Unable to connect to the Database')


# Rest API
api = Api(app)

from project.rest import DepartmentAPI, AllDepartmentsAPI,\
    EmployeeAPI, AllEmployeesAPI, DepartmentEmployeesAPI

api.add_resource(AllDepartmentsAPI, '/api/department/')
api.add_resource(DepartmentAPI, '/api/department/<string:name>')
api.add_resource(DepartmentEmployeesAPI, '/api/department/<string:name>/employees')
api.add_resource(AllEmployeesAPI, '/api/employee/')
api.add_resource(EmployeeAPI, '/api/employee/<int:pk>')
logger.info('Started REST API')


# Blueprint Registration

from project.views import core
from project.views.handlers import error_pages

app.register_blueprint(core)
app.register_blueprint(error_pages)
logger.info('Started Web Application')
