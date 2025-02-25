import os
from flask import Flask

app = Flask(__name__)

from app import views

if __name__ == '__main__':
    app.run(debug=True)
    app.config['SECRET_KEY'] =os.environ.get('SECRET_KEY')