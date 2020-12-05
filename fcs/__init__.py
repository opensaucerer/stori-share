
# importing the required modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
# importing the required modules end


# Instantiatig the App and other classes
app = Flask(__name__)
app.config['SECRET_KEY'] = "b8acd37382011732dc7b2ecadf6497a7"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
CORS(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'danger'
login_manager.login_message = 'Please Log In to Access That Page'
# Instantiatig the App and other classes end

# importing below to avoid circular import
from fcs import routes
# importing below to avoid circular import end
