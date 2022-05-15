""" global.py """
import os
from flask import Flask
from decouple import config
from google.cloud import datastore
from database import Database

# Application
app = Flask(__name__)
# Secret Key
app.secret_key = os.urandom(24)
database = Database()
# Authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "team6merchable-beb259177176.json"
# Datastore client to grab the user's email address
datastore_client = datastore.Client()
# Default image used for stands and posts
DEFAULT_IMAGE_NAME = "https://storage.googleapis.com/team6merchable.appspot.com/default.png"
# Cloud Storage Bucket for images
CLOUD_STORAGE_BUCKET = "team6merchable"
