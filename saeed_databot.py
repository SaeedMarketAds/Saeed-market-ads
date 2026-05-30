import sqlite3

def init_db():
    conn = sqlite3.connect('saeed_market.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products 
                 (id INTEGER PRIMARY KEY, name TEXT, price REAL, description TEXT)''')
    conn.commit()
    conn.close()

def add_product(name, price, description):
    conn = sqlite3.connect('saeed_market.db')
    c = conn.cursor()
    c.execute("INSERT INTO products (name, price, description) VALUES (?, ?, ?)", 
              (name, price, description))
    conn.commit()
    conn.close()

def get_products():
    conn = sqlite3.connect('saeed_market.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    data = c.fetchall()
    conn.close()
    return data
