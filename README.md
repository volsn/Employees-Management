# Departments and Employees 

[![Build Status](https://travis-ci.com/volsn/epam-final-project.svg?branch=master)](https://travis-ci.com/volsn/epam-final-project) [![Coverage Status](https://coveralls.io/repos/github/volsn/epam-final-project/badge.svg?branch=master)](https://coveralls.io/github/volsn/epam-final-project?branch=master)

This is a Repository for my EPAM Python Course Final Project

## Table of contents
0. [Installation](#installation)
1. [Application Structure](#flask-application-structure)
2. [Running Project](#run-flask)
    1. [Using Flask Server](#run-flask-for-develop)
    2. [Serving with Nginx](#run-flask-for-production)
3. [Unittesting](#unittesting)
   1. [Without coverage](#without-coverage)
   2. [Including coverage](#including-coverage)
4. [Reference](#reference)
5. [Changelog](#changelog)


Technologies used in this Project:

- Flask: [Docs](http://flask.pocoo.org/)
- Restful: [Flask-restful](https://flask-restful.readthedocs.io/en/latest/)
- SQLAlchemy ORM: [Flask-SQLalchemy](http://flask-sqlalchemy.pocoo.org/2.1/)
- Bootstrap: [Docs](http://getbootstrap.com)
- Faker: [Docs](https://faker.readthedocs.io)

## Installation
___

Install with pip:

```bash
$ pip install -r requirements.txt
```

## Flask Application Structure
___

```
.
|──────app.py
|──────project/
| |────__init__.py
| |────logs/
| |────migrations/
| |────models/
| | |────__init__.py
| | |────populate.py
| |────rest/
| | |────__init__.py
| | |────departments.py
| | |────employees.py
| |────static/
| |────templates/
| |────tests/
| | |────__init__.py
| | |────test_models.py
| | |────test_rest.py
| | |────test_views.py
| |────views/
| | |────__init__.py
| | |────handlers.py
|──────documentation/
| |────html_prototype/
| |────Mockups/
| |────SRS
|──────gunicorn_config.py
|──────setup.py
|──────nginx.conf
```

## Run Flask
___
### Run Flask for develop
```bash
$ python app.py
```
In flask, Default port is `5000`

Default page:  `http://127.0.0.1:5000/`

### Run Flask for production

** Run with gunicorn **

In core directory

```bash
$ gunicorn -c gunicorn_config.py app:app
```

* -c: config files

* by default runs at localhost/ when deploying with nginx

## Unittesting
___
### Without Coverage
```bash
$ python -m unittest
```

### Including Coverage
```bash
$ coverage run --include 'project/*' -m unittest
$ coverage report
$ coveralls  # sending report to coveralls.io
```

## Reference
___
Offical Website

- [Flask](http://flask.pocoo.org/)
- [Flask-Restful](https://flask-restful.readthedocs.io/en/latest/)
- [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
- [Faker](https://faker.readthedocs.io)
- [gunicorn](http://gunicorn.org/)
- [nginx](http://nginx.org)
- [Travis-CI](https://travis-ci.com)
- [Coveralls](https://coveralls.io/)

Tutorials

- [Flask Bootcamp](https://www.udemy.com/course/python-and-flask-bootcamp-create-websites-using-flask/)
- [REST APIs with Flask](https://www.udemy.com/course/rest-api-flask-and-python/)

[Wiki Page](https://github.com/volsn/epam-final-project/wiki)

## Changelog
___
- Version 1.0 : REST API and Web Application
