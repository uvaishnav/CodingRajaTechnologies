import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Get the database connection details from environment variables
try:
    conn = psycopg2.connect(
        host=os.getenv("HOST"),
        port=os.getenv("PORT"),
        database=os.getenv("DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
except psycopg2.Error as e:
    print("Error connecting to the PostgreSQL database:", e)
    conn = None



def get_order_status(order_id):
    try:
        # Create a cursor object to interact with the database
        cur = conn.cursor()

        # Execute SQL queries
        cur.execute("SELECT * FROM order_tracking WHERE order_id = %s", (order_id,))
        row = cur.fetchone()

        # Close the cursor
        cur.close()

        if row is not None:
            return row[1]
        else:
            return None
    except psycopg2.Error as e:
        print("Error retrieving order status:", e)
        return None


def get_max_order_id():
    try:
        cur = conn.cursor()
        cur.execute("SELECT MAX(order_id) FROM orders")
        row = cur.fetchone()
        cur.close()
        if row[0] is not None:
            return row[0] + 1
        else:
            return 1
    except psycopg2.Error as e:
        print("Error retrieving maximum order ID:", e)
        return None

def get_price(item:str):
    try:
        cur = conn.cursor()
        cur.execute("SELECT price FROM food_items WHERE name = %s", (item,))
        row = cur.fetchone()
        cur.close()
        if row is not None:
            return row[0]
        else:
            return None
    except psycopg2.Error as e:
        print("Error retrieving price for item:", e)
        return None

def get_item_id(item:str):
    try:
        cur = conn.cursor()
        cur.execute("SELECT item_id FROM food_items WHERE name = %s", (item,))
        row = cur.fetchone()
        cur.close()
        if row is not None:
            return row[0]
        else:
            return None
    except psycopg2.Error as e:
        print("Error retrieving item ID:", e)
        return None

def update_order_status(order_id, status):
    try:
        cur = conn.cursor()
        cur.execute("UPDATE order_tracking SET status = %s WHERE order_id = %s", (status, order_id))
        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        print("Error updating order status:", e)

def add_order_status(order_id, status):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)", (order_id, status))
        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        print("Error adding order status:", e)

def add_order_to_db(order_items: dict):
    try:
        cur = conn.cursor()

        order_price = 0

        # Get Maximum order ID
        order_id = get_max_order_id()

        # Adding the order to the orders table
        for item, quantity in order_items.items():
            # Get the price of the item
            price = get_price(item)
            if price is None:
                raise ValueError(f"Price not found for item: {item}")

            total_price = float(price) * quantity
            order_price += total_price

            # Get the item ID
            item_id = get_item_id(item)
            if item_id is None:
                raise ValueError(f"Item ID not found for item: {item}")

            cur.execute("INSERT INTO orders (order_id, item_id, quantity, total_price) VALUES (%s, %s, %s, %s)",
                        (order_id, item_id, quantity, total_price))

        conn.commit()
        cur.close()

        add_order_status(order_id, "In Progress")

        return {
            'order_id': order_id,
            'total_price': order_price,
            'delivery_time': 30
        }
    except psycopg2.Error as e:
        print("Error adding order to database:", e)
        return None
    except ValueError as e:
        print("Error adding order to database:", e)
        return None


# Close the  connection
# conn.close()

