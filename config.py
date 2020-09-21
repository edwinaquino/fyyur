import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgres://edwin:test123@localhost:5432/fyyur3'

#Suggestion: Add SQLALCHEMY_TRACK_MODIFICATIONS as False to avoid significant overhead. It will be disabled by default in the future
SQLALCHEMY_TRACK_MODIFICATIONS = False