import os
from flask import Flask

app = Flask(__name__)

from app import views


app.run()
app.config['SECRET_KEY'] =os.environ.get('SECRET_KEY')