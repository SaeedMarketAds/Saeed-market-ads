import sqlite3
import os

DB_NAME = 'saeed_market.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, description TEXT)''')
    conn.commit()
    conn.close()

def add_product(name, price, description):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO products (name, price, description) VALUES (?, ?, ?)", 
              (name, float(price), description))
    conn.commit()
    conn.close()

def get_products():
    if not os.path.exists(DB_NAME):
        return []
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    data = c.fetchall()
    conn.close()
    return data

def delete_product(product_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    # الكود الخاص بالرد على الرسالة
