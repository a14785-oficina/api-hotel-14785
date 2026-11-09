from flask_restful import Resource, reqparse
from models import hotel
from models.user import UserModel
from hmac import compare_digest
from flask_jwt_extended import create_acess_token, jwt_required, get_jwt
from blocklist import BLOCKLIST

# List, insert, update and delete a hotel in specific
class Hotel(Resource):
    def get(self, username):
        user_found = UserModel.find_user(username)
        if user_found:
            return user_found.json(), 200  # OK
        return {"message": "Hotel was not found!"}, 404  # Not Found
        
    @jwt_required()
    def delete(self, username) -> dict[str, str]: # Delete the hotel with the specified ID.
        user_found = UserModel.find_user(username)
        if user_found:
            user_found.delete_hotel()
            return {"message": f"{str(username).capitalize()} Hotel has been deleted!"}
        return {"message": "Hotel not found!"}, 404  # Not Found

class UserRegister(Resource):
    args = reqparse.RequestParser()
    args.add_argument("username", type=str, required=True, help="The field 'username' cannot be left blank!")
    args.add_argument("password", type=str, required=True, help="The field 'password' cannot be left blank!")
    
    def post(self):
        data = UserRegister.args.parse_args()  # Dictionary with the data sent in the request
        user_found = UserModel.find_user(data["username"])
        if user_found:
            return {"message": f"User '{data['username']}' already exists!"}, 404  # Not Found
        new_user = UserModel(**data)
        new_user.save_user()
        return new_user.json(), 200  # Created

class UserLogin(Resource):
    args = reqparse.RequestParser()
    args.add_argument("username", type=str, required=True, help="The field 'username' cannot be left blank!")
    args.add_argument("password", type=str, required=True, help="The field 'password' cannot be left blank!")
    
    def post(self):
        data = UserLogin.args.parse_args()
        user = UserModel.find_user(data["username"])
        
        if user and compare_digest(user.password, data ["password"]):
            token = create_acess_token(identity=user.username)
        return{ "acess_token": token}
    return{ "message" : "Username or password is invalid!"}

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()["jti"]  # JWT Token Identifier
        BLOCKLIST.add(jwt_id)  # Add the JWT token to the blocklist
        return {"message": "Successfully logged out!"}, 200  # OK