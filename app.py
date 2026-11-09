from flask import Flask
from flask_restful import Api
from resources.hotel import Hotel, Hotels
from resources.user import UserRegister, UserLogin, UserLogout
from con_sql import bd
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST

# Variable representing the Flask application
app = Flask(__name__)

# Variable representing the Flask-RESTful API
api = Api(app)
jwt = JWTManager(app)

# Configurations for the database connection
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hotels.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "a_minha_palavra_secreta_para_a_minha_api_vai_ser_forte"
app.config["JWT_BLACKLIST_ENABLED"] = True

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST  # Check if the JWT token is in the blocklist

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return {"message": "You don't have permission to access this resource. Please log in again."}, 401  # Unauthorized

# Route for the Hotels resource
api.add_resource(Hotels, "/hotels")
api.add_resource(Hotel, "/hotels/<string:id_hotel>")
api.add_resource(User, "/users/<string:username>")
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")

if __name__ == "__main__":
    bd.init_app(app)
    with app.app_context():
        bd.create_all()  # Create the database tables if they don't exist
    app.run(host="127.0.0.1", port=5000, debug=True) # Run the Flask application on localhost (127.0.0.1) with debugging enabled