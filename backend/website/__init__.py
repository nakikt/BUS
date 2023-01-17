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
blockchain2 = Blockchain()
blockchain3 = Blockchain()

mine_block(blockchain, 0,"Funny Street 6", "Ellen Geller", "bad")
mine_block(blockchain1, 1, "Forest Street 13", "John Silva", "good")
mine_block(blockchain2, 2, "Sunny Street 101", "James Bond", "medium")
mine_block(blockchain3, 3, "Garden Street 90", "Harrison Capybara", "excellent")


blocks = [blockchain, blockchain1, blockchain2, blockchain3]
for b in blocks:
    b.add_node("http://127.0.0.1:5000")
    b.add_node("http://127.0.0.1:5001")
    b.add_node("http://127.0.0.1:5002")
    b.add_node("http://127.0.0.1:5003")
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
