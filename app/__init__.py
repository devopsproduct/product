"""
Package: app

Package for the application models and services
This module also sets up the logging to be used with gunicorn
"""

import logging
from flask import Flask
# Since we're using IBM DB2, we need to import the dependencies
import ibm_db_sa
from .vcap_services import get_database_uri

# Create Flask application
app = Flask(__name__)
# We'll just use SQLite here so we don't need an external database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db/development.db'

# HARDCODING THE URI
# app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'please, tell nobody... Shhhh'
app.config['LOGGING_LEVEL'] = logging.INFO

import service

# Set up logging for production
print 'Setting up logging for {}...'.format(__name__)
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    if gunicorn_logger:
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
    else:
        service.initialize_logging()
    service.init_db()  # make our sqlalchemy tables

app.logger.info('Logging established')
