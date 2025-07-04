from flask import Flask
from app.main.routes import main
from app.auth.routes import auth  # Assuming you have auth working

def create_app():
    app = Flask(
        __name__,
        template_folder='app/templates',  # 👈 tells Flask where templates are
        static_folder='app/static'       # 👈 tells Flask where static files are
    )
    app.secret_key = 'your-secret-key'  # Needed for flash messages

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
