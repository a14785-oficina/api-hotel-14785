from con_sql import bd


class UserModel(bd.Model):
    __tablename__ = 'users'
    user_id = bd.Column(bd.String(80), primary_key=True, autoincrement=True)
    username = bd.Column(bd.String(80), nullable=False)
    password = bd.Column(bd.String(120), nullable=False)
    
    # Class Constructor (Mapped Class Essential Components - https://docs.sqlalchemy.org/en/21/orm/mapping_styles.html#orm-mapper-configuration-overview)
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    # Method to return the user data in JSON format
    def json(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password": self.password,
        }
        
    @classmethod
    def find_user(cls, username):
        user = cls.query.filter_by(username=username).first()  # SELECT * FROM users WHERE username=username LIMIT 1
        if user:
            return user
        return None
    
    def save_user(self):
        bd.session.add(self)  # Add the user to the session
        bd.session.commit()  # Commit the session to save the user in the database
        
    def delete_user(self):
        bd.session.delete(self)  # Delete the user from the session
        bd.session.commit()  # Commit the session to delete the user from the database