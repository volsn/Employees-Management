import os
import unittest
from project import app, db, basedir
from project.models.populate import populate_departments,\
    populate_employees


class ViewsTest(unittest.TestCase):

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

    def test_departments(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_department(self):
        response = self.client.get('/department/Marketing')
        self.assertEqual(response.status_code, 200)

    def test_employees(self):
        response = self.client.get('/employees')
        self.assertEqual(response.status_code, 200)

    def test_employee(self):
        response = self.client.get('/employee/1')
        self.assertEqual(response.status_code, 200)

    def test_404(self):
        response = self.client.get('/department/Does not exist')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Page not found', str(response.data))
