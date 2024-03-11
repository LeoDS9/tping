from .entities.User import User


class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT email, password, id, username, first_name, last_name, age, id_rol, telefono FROM user 
                    WHERE email = '{}'""".format(user.email)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], User.check_password(row[1], user.password), row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT email, password, id, username, first_name, last_name, age, id_rol, telefono FROM user WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[3], row[4], row[5], row[6], row[7], row[8])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_by_email(cls, db, email):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT email, password, id, username, first_name, last_name, age, id_rol, telefono FROM user WHERE email = '{}'".format(email)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], None, row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_id(cls, db, email):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id FROM user WHERE email = '{}'".format(email)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return row[0]
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @staticmethod
    def create_user(db, user):
        cursor = db.connection.cursor()
        cursor.execute("INSERT INTO user (email, password, username, first_name, last_name, age, id_rol) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (user.email, user.generate_hash(user.password), user.username, user.first_name, user.last_name, user.age, user.id_rol))
        db.connection.commit()

    @staticmethod
    def update_profile(db, email, first_name, last_name, age):
        try:
            cursor = db.connection.cursor()
            sql = "UPDATE user SET email = %s, first_name = %s, last_name = %s, age = %s WHERE email = %s"
            cursor.execute(sql, (email, first_name, last_name, age, email))
            db.connection.commit()
            return True
        except Exception as ex:
            print("Error updating profile:", ex)
            return False