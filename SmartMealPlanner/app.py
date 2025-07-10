from flask import Flask
from routes import api
from models import db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
app.register_blueprint(api)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)