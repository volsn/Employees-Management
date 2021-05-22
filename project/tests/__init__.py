"""
Package with unittests covering the whole project
"""
import os
from project import app, db, basedir
from project.models.populate import populate_departments, populate_employees


class UnittestSetup:
    """ Class for defining setUp and tearDown methods for unittesting """
    def setUp(self) -> None:
        """ Setup method that runs before each test """
        # Overriding flask app settings
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['WTF_CSRF_CHECK_DEFAULT'] = False

        # Using local sqlite db instead of the one used in the project
        db_path = os.path.join(basedir, 'tests', 'db_test.sqlite')
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
