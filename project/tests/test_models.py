import os
import unittest
from project import app, db, basedir
from project.models.populate import Department, Employee,\
    populate_departments, populate_employees


class ModelsTest(unittest.TestCase):

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['WTF_CSRF_CHECK_DEFAULT'] = False

        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(*[basedir, 'tests', 'db_test.sqlite'])

        db.create_all()
        populate_departments()
        populate_employees()

        self.client = app.test_client()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_departments_created(self):
        self.assertEqual(len(Department.query.all()), 14)

    def test_employees_created(self):
        self.assertNotEqual(len(Employee.query.all()), 0)