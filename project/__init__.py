import os
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api


# App Setup

app = Flask(__name__)
version = '0.0.1'
load_dotenv()
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


# Database Setup

basedir = os.path.abspath(os.path.dirname(__file__))
migration_dir = os.path.join(basedir, 'migrations')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db, directory=migration_dir)


# Rest API

api = Api(app)

from project.rest import DepartmentAPI, AllDepartmentsAPI,\
    EmployeeAPI, AllEmployeesAPI, DepartmentEmployeesAPI

api.add_resource(AllDepartmentsAPI, '/api/department/')
api.add_resource(DepartmentAPI, '/api/department/<string:name>')
api.add_resource(DepartmentEmployeesAPI, '/api/department/<string:name>/employees')
api.add_resource(AllEmployeesAPI, '/api/employee/')
api.add_resource(EmployeeAPI, '/api/employee/<int:pk>')


# Blueprint Registration

from project.views import core
from project.views.handlers import error_pages

app.register_blueprint(core)
app.register_blueprint(error_pages)
