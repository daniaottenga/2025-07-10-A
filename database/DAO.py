from database.DB_connect import DBConnect
from model.categoria import Categoria
from model.prodotto import Prodotto


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def getAllCategories():

        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)

        query = """select * from categories"""

        cursor.execute(query)

        for row in cursor:
            results.append(Categoria(**row))

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last


    @staticmethod
    def getProdottiCategoria(categoria):

        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)

        query = """select product_id, product_name, brand_id, category_id, model_year, list_price 
from products 
where category_id = %s"""

        cursor.execute(query, (categoria,))

        for row in cursor:
            results.append(Prodotto(**row))

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getEdges(categoria, inizio, fine):

        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)

        query = """select oi.product_id pId, count(oi.product_id) n 
from order_items oi, orders o, categories c, products p 
where o.order_id = oi.order_id and 
o.order_date BETWEEN %s and %s and 
p.category_id = c.category_id and 
p.product_id = oi.product_id and 
p.category_id = %s 
group by oi.product_id"""

        cursor.execute(query, (inizio, fine, categoria))

        for row in cursor:
            results.append((row["pId"], row["n"]))

        cursor.close()
        conn.close()
        return results
