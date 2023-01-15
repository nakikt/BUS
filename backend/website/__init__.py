from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .methods import mine_block
db = SQLAlchemy()
DB_NAME = "database.db"



from .blockchain import Blockchain

blockchain = Blockchain()
blockchain1 = Blockchain()

mine_block(blockchain, 0, "address0", "name_surname0", "condition0" )
mine_block(blockchain1, 1, "address1", "name_surname1", "condition1")

blocks = [blockchain, blockchain1]
for b in blocks:
    b.add_node("http://127.0.0.1:5000")
    b.add_node("http://127.0.0.1:5001")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)


    from .views import views
    from .auth import auth
    from .blockchain_func import blockchain_func

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(blockchain_func, url_prefix="/")

    from .models import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app
