class Customer:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email

class Product:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

class Invoice:
    def __init__(self, customer_id, date, total):
        self.customer_id = customer_id
        self.date = date
        self.total = total

class InvoiceItem:
    def __init__(self, invoice_id, product_id, quantity):
        self.invoice_id = invoice_id
        self.product_id = product_id
        self.quantity = quantity
        
class Service:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost 
