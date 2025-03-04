from database import execute_query, fetch_query
from models import Customer, Product, Invoice, InvoiceItem
from fpdf import FPDF
import pandas as pd
import datetime

# CRUD Operations
def add_customer(customer):
    query = "INSERT INTO customers (name, phone, email) VALUES (?, ?, ?)"
    execute_query(query, (customer.name, customer.phone, customer.email))

def get_customers():
    query = "SELECT * FROM customers"
    return fetch_query(query)

def update_customer(customer_id, name, phone, email):
    query = "UPDATE customers SET name = ?, phone = ?, email = ? WHERE id = ?"
    execute_query(query, (name, phone, email, customer_id))

def delete_customer(customer_id):
    query = "DELETE FROM customers WHERE id = ?"
    execute_query(query, (customer_id,))

def add_product(product):
    query = "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)"
    execute_query(query, (product.name, product.price, product.stock))

def get_products():
    query = "SELECT * FROM products"
    return fetch_query(query)

def update_product(product_id, name, price, stock):
    query = "UPDATE products SET name = ?, price = ?, stock = ? WHERE id = ?"
    execute_query(query, (name, price, stock, product_id))

def delete_product(product_id):
    query = "DELETE FROM products WHERE id = ?"
    execute_query(query, (product_id,))

# CRUD Operations for Services
def add_service(service):
    query = "INSERT INTO services (name, cost) VALUES (?, ?)"
    execute_query(query, (service.name, service.cost))

def get_services():
    query = "SELECT * FROM services"
    return fetch_query(query)

def update_service(service_id, name, cost):
    query = "UPDATE services SET name = ?, cost = ? WHERE id = ?"
    execute_query(query, (name, cost, service_id))

def delete_service(service_id):
    query = "DELETE FROM services WHERE id = ?"
    execute_query(query, (service_id,))

# Invoice Generation
def generate_pdf_invoice(invoice_id):
    query = "SELECT * FROM invoices WHERE id = ?"
    invoice = fetch_query(query, (invoice_id,))[0]
    
    query = "SELECT * FROM invoice_items WHERE invoice_id = ?"
    items = fetch_query(query, (invoice_id,))
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Invoice", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Date: {invoice[2]}", ln=True)
    pdf.cell(200, 10, txt=f"Total: ${invoice[3]}", ln=True)
    
    for item in items:
        if item[2]:  # Product
            query = "SELECT name FROM products WHERE id = ?"
            product_name = fetch_query(query, (item[2],))[0][0]
            pdf.cell(200, 10, txt=f"Product: {product_name}, Quantity: {item[4]}", ln=True)
        elif item[3]:  # Service
            query = "SELECT name FROM services WHERE id = ?"
            service_name = fetch_query(query, (item[3],))[0][0]
            pdf.cell(200, 10, txt=f"Service: {service_name}", ln=True)
    
    pdf.output(f"invoice_{invoice_id}.pdf")

# Invoice Creation
def create_invoice(customer_id, items):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    total = sum(item['price'] * item['quantity'] for item in items)
    
    query = "INSERT INTO invoices (customer_id, date, total) VALUES (?, ?, ?)"
    execute_query(query, (customer_id, date, total))
    invoice_id = fetch_query("SELECT last_insert_rowid()")[0][0]
    
    for item in items:
        if 'product_id' in item:
            query = "INSERT INTO invoice_items (invoice_id, product_id, quantity) VALUES (?, ?, ?)"
            execute_query(query, (invoice_id, item['product_id'], item['quantity']))
        elif 'service_id' in item:
            query = "INSERT INTO invoice_items (invoice_id, service_id, quantity) VALUES (?, ?, ?)"
            execute_query(query, (invoice_id, item['service_id'], item['quantity']))
    
    return invoice_id
