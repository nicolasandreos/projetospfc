from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = '76de173de227420f653cf3c10a713543'
if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projetospfc.db'

database = SQLAlchemy(app)
criptografia = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'loginspfc'
login_manager.login_message = 'Por favor para continuar, faça Login.'
login_manager.login_message_category = 'alert-info'

from spfcproject import routes
