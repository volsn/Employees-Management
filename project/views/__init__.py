from flask import Blueprint
from project.models import Department, Employee

core = Blueprint('core', __name__)


@core.route('/')
def index():
    return 'Hello world'
