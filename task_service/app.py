from flask import Flask
from flask_jwt_extended import JWTManager
from db import db
from routes import task_bp
import config
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
# CORS(app)
# cors_allowed_origin = config.CORS_ALLOWED_ORIGIN
# # Configure CORS with dynamic allowed origin
CORS(app, origins=["*"], methods=["GET", "POST", "DELETE", "PUT"])
# 
# CORS(app)


app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY

db.init_app(app)

jwt = JWTManager(app)
migrate = Migrate(app, db)
app.register_blueprint(task_bp, url_prefix="/v1")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5002, debug=True)
