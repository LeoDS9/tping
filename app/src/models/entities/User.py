from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, email, password, id = None, username=None, first_name=None, last_name=None, age=None, id_rol=None, telefono=None) -> None:
        self.email = email
        self.password = password
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.id_rol = id_rol
        self.telefono = telefono


    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)
    
    @classmethod
    def generate_hash(self, passw):
        return generate_password_hash(passw)
    
    def get_info(self):
        user_info = {
            'email': self.email,
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'id_rol': self.id_rol,
            'telefono': self.telefono
        }
        return user_info
    
    def get_string_info(self):
        user_info = self.get_info()
        string_info = ""
        for key, value in user_info.items():
            string_info += f"{key}: {value}\n"
        return string_info

#print(generate_password_hash("hola"))