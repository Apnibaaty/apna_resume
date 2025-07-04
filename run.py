from flask import Flask
from flask_login import LoginManager
from app.models import db, User
from app.main.routes import main
from app.auth.routes import auth

def create_app():
    app = Flask(
        __name__,
        template_folder='app/templates',
        static_folder='app/static'
    )
    app.secret_key = 'your-secret-key'

    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Setup login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app

if __name__ == "__main__":
    app = create_app()
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    app.run(debug=True)
