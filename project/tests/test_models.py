""" Unittests for models module """
import os
import unittest
from project import app, db, basedir
from project.models.populate import Department, Employee,\
    populate_departments, populate_employees, drop_data


class ModelsTest(unittest.TestCase):
    """ Unittests for the models module """

    def setUp(self) -> None:
        """ Setup method that runs before each test """
        # Overriding flask app settings
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['WTF_CSRF_CHECK_DEFAULT'] = False

        # Using local sqlite db instead of the one used in the project
        db_path = os.path.join(*[basedir, 'tests', 'db_test.sqlite'])
        if os.path.exists(db_path):
            os.remove(db_path)

        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

        db.create_all()
        populate_departments()
        populate_employees()

        # Creating client for making requests
        self.client = app.test_client()

    def tearDown(self):
        # Dropping all data from the database
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_departments_created(self):
        """ Verify that 'department' table has been populated """
        self.assertEqual(len(Department.query.all()), 14)

    def test_employees_created(self):
        """ Verify that 'employee' table has been populated """
        self.assertNotEqual(len(Employee.query.all()), 0)

    def test_drop_data(self):
        """ Test that drop_data function drops all tables' data """
        drop_data()
        self.assertEqual(len(Department.query.all()), 0)
        self.assertEqual(len(Employee.query.all()), 0)
