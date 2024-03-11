from .entities.Product import Product


class ModelProduct:

    @classmethod
    def get_by_name(cls, db, name):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT name, description, trueque, vendedor, id FROM product WHERE name = %s"
            cursor.execute(sql, (name,))
            row = cursor.fetchone()
            if row is not None:
                print(*row)
                return Product(*row)
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_product_by_id(cls, db, product_id):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT name, description, trueque, vendedor, id FROM product 
                    WHERE id = '{}'""".format(product_id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row:
                return Product(*row)
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @staticmethod
    def create_product(db, product):
        try:
            cursor = db.connection.cursor()
            sql = "INSERT INTO product (name, description, trueque, vendedor) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (product.name, product.description, product.trueque, product.vendedor))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @staticmethod
    def get_all_products(db):
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()
        cursor.close()
        return products
