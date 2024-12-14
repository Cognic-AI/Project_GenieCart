# app/queries.py
def fetch_previous_orders(user_id, connection):
    """
    Fetch previous orders of a user from the database.
    :param user_id: ID of the user
    :param connection: MySQL connection object
    :return: List of orders
    """
    query = """
    SELECT order_id, product_name, price, order_date
    FROM orders
    WHERE user_id = %s
    ORDER BY order_date DESC;
    """
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query, (user_id,))
        return cursor.fetchall()

def fetch_suggestions(user_id, connection):
    """
    Fetch platform suggestions for a user based on their previous orders.
    :param user_id: ID of the user
    :param connection: MySQL connection object
    :return: List of suggested products
    """
    query = """
    SELECT suggestion_id, suggested_product, reason
    FROM suggestions
    WHERE user_id = %s;
    """
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query, (user_id,))
        return cursor.fetchall()
