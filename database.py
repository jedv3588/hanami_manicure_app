import sqlite3

def init_db():
    conn = sqlite3.connect('manicurist.db')
    c = conn.cursor()
    
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS customers
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, email TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, stock INTEGER)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS services
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, cost REAL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS invoices
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INTEGER, date TEXT, total REAL,
                  FOREIGN KEY(customer_id) REFERENCES customers(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS invoice_items
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, invoice_id INTEGER, product_id INTEGER, service_id INTEGER, quantity INTEGER,
                  FOREIGN KEY(invoice_id) REFERENCES invoices(id),
                  FOREIGN KEY(product_id) REFERENCES products(id),
                  FOREIGN KEY(service_id) REFERENCES services(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL);''')
    
    conn.commit()
    conn.close()

def execute_query(query, params=()):
    conn = sqlite3.connect('manicurist.db')
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    conn.close()

def fetch_query(query, params=()):
    conn = sqlite3.connect('manicurist.db')
    c = conn.cursor()
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows