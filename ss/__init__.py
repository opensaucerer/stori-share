
# importing the required modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
import os
# importing the required modules end


# Instantiatig the App and other classes
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('TEST_DATABASE_URL') if os.environ.get(
    'ENVIRONMENT') == "development" else os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
CORS(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'danger'
login_manager.login_message = 'Please Log In to Access That Page'
# Instantiatig the App and other classes end

# importing below to avoid circular import
from ss import routes
# importing below to avoid circular import end
