""" Unittests for rest api module """
import os
import json
import unittest
from project import app, db, basedir
from project.models.populate import populate_departments, populate_employees


class DepartmentsTest(unittest.TestCase):
    """ Unittests for the '/departments' part of api"""

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

    def test_get_all_departments(self):
        """ Return the list of all the departments in the database """
        response = self.client.get('/api/department/')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('departments' in data.keys())

    def test_get_department(self):
        """ Retrieve a single department """
        response = self.client.get('/api/department/Marketing')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'Marketing')

    def test_get_not_existing_department(self):
        """ Try accessing a department that doesn't exist """
        response = self.client.get('/api/department/Not Real')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertDictEqual(data, {'message': 'department with name \'Not Real\' does not exist'})

    def test_post_department(self):
        """ Create new department using post request """
        response = self.client.post('/api/department/New Department')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['name'], 'New Department')
        response = self.client.get('/api/department/New Department')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'New Department')

    def test_post_existing_department(self):
        """ Try create department that already exists """
        response = self.client.post('/api/department/Marketing')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(data, {'message': 'department with name \'Marketing\' already exists'})

    def test_put_new_department(self):
        """ Create new department using put request """
        response = self.client.post('/api/department/New Department')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['name'], 'New Department')

    def test_put_edit_department(self):
        """ Edit department data using post request"""
        response = self.client.put('/api/department/Marketing',
                                   data=json.dumps({'name': 'Changed Name'}),
                                   content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Changed Name')
        response = self.client.get('/api/department/Changed Name')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'Changed Name')

    def test_delete_department(self):
        """ Delete department """
        response = self.client.delete('/api/department/Marketing')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(data, {'message': 'department \'Marketing\' successfully removed'})

    def test_get_department_employees(self):
        """ Retrieve all employees of a certain department """
        response = self.client.get('/api/department/Marketing/employees')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['department']['name'], 'Marketing')
        self.assertTrue('employees' in data.keys())


class EmployeesTest(unittest.TestCase):
    """ Unittests for the '/employee' part of api"""

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

    def test_get_all_employees(self):
        """ Get data about all employees """
        response = self.client.get('/api/employee/')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('employees' in data.keys())

    def test_post_get_employee(self):
        """ Create new employee """
        response = self.client.post('/api/employee/',
                                    data=json.dumps({'name': 'Steve Newton',
                                                     'department': 'Marketing',
                                                     'birthdate': '05.05.2000',
                                                     'salary': 900}),
                                    content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['name'], 'Steve Newton')
        response = self.client.get('/api/employee/{}'.format(data['id']))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'Steve Newton')

    def test_post_invalid_birthdate_employee(self):
        """ Try creating employee with invalid birthday data """
        response = self.client.post('/api/employee/',
                                    data=json.dumps({'name': 'Steve Newton',
                                                     'department': 'Marketing',
                                                     'birthdate': '15.15.2000',
                                                     'salary': 900}),
                                    content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(data, {"message": "time data '15.15.2000'"
                                               "does not match format '%m.%d.%Y'"})

    def test_post_invalid_department_employee(self):
        """ Try creating employee with invalid department """
        response = self.client.post('/api/employee/',
                                    data=json.dumps({'name': 'Steve Newton',
                                                     'department': 'Does not Exist',
                                                     'birthdate': '05.05.2000',
                                                     'salary': 900}),
                                    content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(data, {"message": "department with name"
                                               "'Does not Exist' does not exist"})

    def test_post_new_put_edit_employee(self):
        """ Create new employee and edit his data using put request """
        response = self.client.post('/api/employee/',
                                    data=json.dumps({'name': 'Steve Newton',
                                                     'department': 'Marketing',
                                                     'birthdate': '05.05.2000',
                                                     'salary': 900}),
                                    content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['name'], 'Steve Newton')
        response = self.client.put('/api/employee/{}'.format(data['id']),
                                   data=json.dumps({'salary': 1200,
                                                    'department': 'Research'}),
                                   content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['salary'], 1200)
        self.assertEqual(data['department'], 'Research')

    def test_delete_employee(self):
        """ Delete employee """
        response = self.client.post('/api/employee/',
                                    data=json.dumps({'name': 'Steve Newton',
                                                     'department': 'Marketing',
                                                     'birthdate': '05.05.2000',
                                                     'salary': 900}),
                                    content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['name'], 'Steve Newton')
        response = self.client.delete('/api/employee/{}'.format(data['id']))
        id_ = data['id']
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {'message': 'employee with id {} successfully removed'.format(id_)})

    def test_delete_not_existing_employee(self):
        """ Try deleting employee that doesn't exist """
        id_ = 1000
        response = self.client.delete('/api/employee/{}'.format(id_))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertDictEqual(data, {'message': 'employee with id {} does not exist'.format(id_)})
