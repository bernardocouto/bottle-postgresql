import os

APPLICATION_DEBUG = os.environ.get('APPLICATION_DEBUG')
APPLICATION_HOST = os.environ.get('APPLICATION_HOST')
APPLICATION_PORT = os.environ.get('APPLICATION_PORT')
APPLICATION_RELOADER = os.environ.get('APPLICATION_RELOADER')

DATABASE_CONNECTION_TIMEOUT = os.environ.get('DATABASE_CONNECTION_TIMEOUT')
DATABASE_HOST = os.environ.get('DATABASE_HOST')
DATABASE_MAX_CONNECTION = os.environ.get('DATABASE_MAX_CONNECTION')
DATABASE_NAME = os.environ.get('DATABASE_NAME')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE_PORT = os.environ.get('DATABASE_PORT')
DATABASE_PRINT_SQL = os.environ.get('DATABASE_PRINT_SQL')
DATABASE_USERNAME = os.environ.get('DATABASE_USERNAME')
