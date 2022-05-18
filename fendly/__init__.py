from datetime import timedelta
from flask import Flask
import os

# from fendly.config import UPLOAD_FOLDER
# from config import UPLOAD_FOLDER

app = Flask(__name__)
# app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET')
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

from fendly import routes