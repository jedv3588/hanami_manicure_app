import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from services import *
from models import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import os
import datetime

class ManicuristApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hanami - Manicure")
        self.style = ttk.Style(theme="cosmo")
        
        # Start the app maximized
        self.root.state("zoomed")
        
        # Set the window icon
        logo_path = os.path.join(os.path.dirname(__file__), 'images', 'logo.ico')
        if os.path.exists(logo_path):
            self.root.iconbitmap(logo_path)  # Set the icon for the root window
        else:
            print(f"Warning: Icon not found at {logo_path}")
        
        # Load logo and banner images from the project folder
        self.load_images()
        
        # Notebook for Tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=BOTH, expand=True)
        
        # Dashboard Tab
        self.dashboard_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_tab, text="Dashboard")
        self.setup_dashboard()
        
        # Customers Tab
        self.customers_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.customers_tab, text="Clientes")
        self.setup_customers()
        
        # Products Tab
        self.products_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.products_tab, text="Productos")
        self.setup_products()
        
        # Services Tab
        self.services_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.services_tab, text="Servicios")
        self.setup_services()
        
        # Invoices Tab
        self.invoices_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.invoices_tab, text="Generar factura")
        self.setup_invoices()
        
        # Daily close
        self.daily_close_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.daily_close_tab, text="Cierre diario")
        self.setup_daily_close()

    def load_images(self):
        # Get the absolute path to the project directory
        project_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Load logo
        logo_path = os.path.join(project_dir, "images", "logo-slogan.png")
        if os.path.exists(logo_path):
            self.logo_image = Image.open(logo_path).resize((250, 250))  # Resize logo
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        else:
            print(f"Warning: Logo image not found at {logo_path}")
            self.logo_photo = None  # Set to None if image is missing

        # Load banner
        banner_path = os.path.join(project_dir, "images", "banner.png")
        if os.path.exists(banner_path):
            self.banner_image = Image.open(banner_path).resize((800, 250))  # Resize banner
            self.banner_photo = ImageTk.PhotoImage(self.banner_image)
        else:
            print(f"Warning: Banner image not found at {banner_path}")
            self.banner_photo = None  # Set to None if image is missing
            
        # Load right-side image
        right_image_path = os.path.join(project_dir, "images", "female_feethands.png")
        print(f"Absolute right image path: {right_image_path}")
        if os.path.exists(right_image_path):
            self.right_image = Image.open(right_image_path).resize((350, 250))  # Resize right image
            self.right_photo = ImageTk.PhotoImage(self.right_image)
        else:
            print(f"Warning: Right image not found at {right_image_path}")
            self.right_photo = None  # Set to None if image is missing
    
    def setup_dashboard(self):
        # Configure the dashboard_tab grid
        self.dashboard_tab.grid_rowconfigure(0, weight=0)  # Row 0: image_frame (fixed height)
        self.dashboard_tab.grid_rowconfigure(1, weight=1)  # Row 1: chart_frame (expandable)
        self.dashboard_tab.grid_columnconfigure(0, weight=1)  # Column 0: expandable

        # Create a frame for the images
        image_frame = ttk.Frame(self.dashboard_tab)
        image_frame.grid(row=0, column=0, sticky=W+E, padx=10, pady=10)

        # Configure the grid to resize proportionally
        image_frame.grid_columnconfigure(0, weight=1)  # Logo column
        image_frame.grid_columnconfigure(1, weight=3)  # Banner column
        image_frame.grid_columnconfigure(2, weight=1)  # Right image column

        # Add logo (if available)
        if self.logo_photo:
            logo_label = ttk.Label(image_frame, image=self.logo_photo)
            logo_label.grid(row=0, column=0, sticky=W+E)
        else:
            logo_label = ttk.Label(image_frame, text="Logo Not Found", bootstyle=DANGER)
            logo_label.grid(row=0, column=0, sticky=W+E)

        # Add banner (if available)
        if self.banner_photo:
            banner_label = ttk.Label(image_frame, image=self.banner_photo)
            banner_label.grid(row=0, column=1, sticky=W+E)
        else:
            banner_label = ttk.Label(image_frame, text="Banner Not Found", bootstyle=DANGER)
            banner_label.grid(row=0, column=1, sticky=W+E)

        # Add right-side image (if available)
        if self.right_photo:
            right_image_label = ttk.Label(image_frame, image=self.right_photo)
            right_image_label.grid(row=0, column=2, sticky=W+E)
        else:
            right_image_label = ttk.Label(image_frame, text="Right Image Not Found", bootstyle=DANGER)
            right_image_label.grid(row=0, column=2, sticky=W+E)

        # Add charts and performance indicators
        self.setup_charts()

    def setup_charts(self):
        # Create a frame for charts
        chart_frame = ttk.LabelFrame(self.dashboard_tab, text="Gráficos de comportamiento", bootstyle=INFO)
        chart_frame.grid(row=1, column=0, sticky=W+E+N+S, padx=10, pady=10)

        # Configure the grid to resize proportionally
        chart_frame.grid_columnconfigure(0, weight=1)  # Line chart column
        chart_frame.grid_columnconfigure(1, weight=1)  # Bar chart column
        chart_frame.grid_columnconfigure(2, weight=1)  # Pie chart column
        chart_frame.grid_rowconfigure(0, weight=1)  # First row of charts
        chart_frame.grid_rowconfigure(1, weight=1)  # Second row of charts

        # Add existing charts
        self.setup_line_chart(chart_frame)
        self.setup_bar_chart(chart_frame)
        self.setup_pie_chart(chart_frame)

        # Add new charts below the existing ones
        self.setup_income_expenses_chart(chart_frame)
        self.setup_popular_services_chart(chart_frame)
        self.setup_customer_demographics_chart(chart_frame)

    def setup_line_chart(self, parent):
        # Example: Total Customers Over Time
        fig, ax = plt.subplots(figsize=(4, 2))  # Smaller size
        dates = ["2023-10-01", "2023-10-02", "2023-10-03"]
        total_customers = [10, 15, 20]

        # Use Hanami colors
        ax.plot(dates, total_customers, marker="o", color="#FFB7C5", linewidth=2, markersize=8)
        ax.set_title("Total de clientes en el tiempo", color="#DDA0DD", fontsize=10)
        ax.set_xlabel("Fecha", color="#DDA0DD", fontsize=8)
        ax.set_ylabel("Total de Clientes", color="#DDA0DD", fontsize=8)
        ax.tick_params(axis='x', labelsize=7)
        ax.tick_params(axis='y', labelsize=7)
        ax.set_facecolor("#FFFFFF")  # Background color
        fig.patch.set_facecolor("#E6E6FA")  # Outer background color

        # Embed the chart in the dashboard
        chart_canvas = FigureCanvasTkAgg(fig, master=parent)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().grid(row=0, column=0, sticky=W+E+N+S, padx=5, pady=5)

    def setup_bar_chart(self, parent):
        # Example: Product Sales
        fig, ax = plt.subplots(figsize=(4, 2))  # Smaller size
        products = ["Producto A", "Producto B", "Producto C"]
        sales = [25, 40, 30]

        # Use Hanami colors
        colors = ["#FFB7C5", "#F4C2C2", "#DDA0DD"]
        ax.bar(products, sales, color=colors)
        ax.set_title("Ventas de Productos", color="#DDA0DD", fontsize=10)
        ax.set_xlabel("Producto", color="#DDA0DD", fontsize=8)
        ax.set_ylabel("Ventas", color="#DDA0DD", fontsize=8)
        ax.tick_params(axis='x', labelsize=7)
        ax.tick_params(axis='y', labelsize=7)
        ax.set_facecolor("#FFFFFF")  # Background color
        fig.patch.set_facecolor("#E6E6FA")  # Outer background color

        # Embed the chart in the dashboard
        chart_canvas = FigureCanvasTkAgg(fig, master=parent)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().grid(row=0, column=1, sticky=W+E+N+S, padx=5, pady=5)

    def setup_pie_chart(self, parent):
        # Example: Service Usage
        fig, ax = plt.subplots(figsize=(4, 2))  # Smaller size
        services = ["Servicio A", "Servicio B", "Servicio C"]
        usage = [30, 50, 20]

        # Use Hanami colors
        colors = ["#FFB7C5", "#F4C2C2", "#DDA0DD"]
        ax.pie(usage, labels=services, autopct="%1.1f%%", startangle=90, colors=colors, textprops={'fontsize': 7})
        ax.set_title("Uso de Servicios", color="#DDA0DD", fontsize=10)
        ax.tick_params(axis='x', labelsize=7)
        ax.tick_params(axis='y', labelsize=7)
        fig.patch.set_facecolor("#E6E6FA")  # Outer background color

        # Embed the chart in the dashboard
        chart_canvas = FigureCanvasTkAgg(fig, master=parent)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().grid(row=0, column=2, sticky=W+E+N+S, padx=5, pady=5)

    def setup_income_expenses_chart(self, parent):
        # Example: Income and Expenses Over Time
        fig, ax = plt.subplots(figsize=(4, 2))  # Smaller size
        dates = ["2023-10-01", "2023-10-02", "2023-10-03"]
        income = [1000, 1500, 2000]
        expenses = [300, 500, 700]

        # Use Hanami colors
        ax.plot(dates, income, marker="o", color="#FFB7C5", linewidth=2, markersize=8, label="Ingreso")
        ax.plot(dates, expenses, marker="o", color="#DDA0DD", linewidth=2, markersize=8, label="Gastos")
        ax.set_title("Ingresos vs Gastos en el tiempo", color="#DDA0DD", fontsize=10)
        ax.set_xlabel("Fecha", color="#DDA0DD", fontsize=8)
        ax.set_ylabel("Importe", color="#DDA0DD", fontsize=8)
        ax.tick_params(axis='x', labelsize=7)
        ax.tick_params(axis='y', labelsize=7)
        ax.set_facecolor("#FFFFFF")  # Background color
        fig.patch.set_facecolor("#E6E6FA")  # Outer background color
        ax.legend()

        # Embed the chart in the dashboard
        chart_canvas = FigureCanvasTkAgg(fig, master=parent)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().grid(row=1, column=0, sticky=W+E+N+S, padx=5, pady=5)

    def setup_popular_services_chart(self, parent):
        # Example: Most Popular Services
        fig, ax = plt.subplots(figsize=(4, 2))  # Smaller size
        services = ["Servicio A", "Servicio B", "Servicio C", "Servicio D"]
        popularity = [30, 50, 25, 60]

        # Use Hanami colors
        colors = ["#FFB7C5", "#F4C2C2", "#DDA0DD", "#E6E6FA"]
        ax.barh(services, popularity, color=colors)
        ax.set_title("Servicios más populares", color="#DDA0DD", fontsize=10)
        ax.set_xlabel("Popularidad", color="#DDA0DD", fontsize=8)
        ax.set_ylabel("Servicio", color="#DDA0DD", fontsize=8)
        ax.tick_params(axis='x', labelsize=7)
        ax.tick_params(axis='y', labelsize=7)
        ax.set_facecolor("#FFFFFF")  # Background color
        fig.patch.set_facecolor("#E6E6FA")  # Outer background color

        # Embed the chart in the dashboard
        chart_canvas = FigureCanvasTkAgg(fig, master=parent)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().grid(row=1, column=1, sticky=W+E+N+S, padx=5, pady=5)

    def setup_customer_demographics_chart(self, parent):
        # Example: Customer Demographics
        fig, ax = plt.subplots(figsize=(4, 2))  # Smaller size
        demographics = ["Hombre", "Mujer", "Otro"]
        percentages = [40, 55, 5]

        # Use Hanami colors
        colors = ["#FFB7C5", "#F4C2C2", "#DDA0DD"]
        ax.pie(percentages, labels=demographics, autopct="%1.1f%%", startangle=90, colors=colors, textprops={'fontsize': 7})
        ax.set_title("Datos demográficos de los clientes", color="#DDA0DD", fontsize=10)
        ax.tick_params(axis='x', labelsize=7)
        ax.tick_params(axis='y', labelsize=7)
        fig.patch.set_facecolor("#E6E6FA")  # Outer background color

        # Embed the chart in the dashboard
        chart_canvas = FigureCanvasTkAgg(fig, master=parent)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().grid(row=1, column=2, sticky=W+E+N+S, padx=5, pady=5)
    
    def setup_customers(self):
        # CRUD Form for Customers
        form_frame = ttk.Frame(self.customers_tab)
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NW)
        
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.customer_name_entry = ttk.Entry(form_frame)
        self.customer_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Phone:").grid(row=1, column=0, padx=5, pady=5)
        self.customer_phone_entry = ttk.Entry(form_frame)
        self.customer_phone_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        self.customer_email_entry = ttk.Entry(form_frame)
        self.customer_email_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(form_frame, text="Add Customer", command=self.add_customer).grid(row=3, column=0, pady=10)
        ttk.Button(form_frame, text="Edit Customer", command=self.edit_customer).grid(row=3, column=1, pady=10)
        ttk.Button(form_frame, text="Delete Customer", command=self.delete_customer).grid(row=3, column=2, pady=10)
        
        # Table to display customers
        columns = ("ID", "Name", "Phone", "Email")
        self.customer_table = ttk.Treeview(self.customers_tab, columns=columns, show="headings")
        for col in columns:
            self.customer_table.heading(col, text=col)
        self.customer_table.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)
        
        # Load customer data into the table
        self.load_customers()
    
    def add_customer(self):
        name = self.customer_name_entry.get()
        phone = self.customer_phone_entry.get()
        email = self.customer_email_entry.get()
        customer = Customer(name, phone, email)
        add_customer(customer)
        self.load_customers()
    
    def edit_customer(self):
        selected_item = self.customer_table.selection()
        if not selected_item:
            return
        customer_id = self.customer_table.item(selected_item, "values")[0]
        name = self.customer_name_entry.get()
        phone = self.customer_phone_entry.get()
        email = self.customer_email_entry.get()
        update_customer(customer_id, name, phone, email)
        self.load_customers()
    
    def delete_customer(self):
        selected_item = self.customer_table.selection()
        if not selected_item:
            return
        customer_id = self.customer_table.item(selected_item, "values")[0]
        delete_customer(customer_id)
        self.load_customers()
    
    def load_customers(self):
        for row in self.customer_table.get_children():
            self.customer_table.delete(row)
        customers = get_customers()
        for customer in customers:
            self.customer_table.insert("", END, values=customer)
    
    def setup_products(self):
        # CRUD Form for Products
        form_frame = ttk.Frame(self.products_tab)
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NW)
        
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.product_name_entry = ttk.Entry(form_frame)
        self.product_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Price:").grid(row=1, column=0, padx=5, pady=5)
        self.product_price_entry = ttk.Entry(form_frame)
        self.product_price_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Stock:").grid(row=2, column=0, padx=5, pady=5)
        self.product_stock_entry = ttk.Entry(form_frame)
        self.product_stock_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(form_frame, text="Add Product", command=self.add_product).grid(row=3, column=0, pady=10)
        ttk.Button(form_frame, text="Edit Product", command=self.edit_product).grid(row=3, column=1, pady=10)
        ttk.Button(form_frame, text="Delete Product", command=self.delete_product).grid(row=3, column=2, pady=10)
        
        # Table to display products
        columns = ("ID", "Name", "Price", "Stock")
        self.product_table = ttk.Treeview(self.products_tab, columns=columns, show="headings")
        for col in columns:
            self.product_table.heading(col, text=col)
        self.product_table.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)
        
        # Load product data into the table
        self.load_products()
    
    def add_product(self):
        name = self.product_name_entry.get()
        price = float(self.product_price_entry.get())
        stock = int(self.product_stock_entry.get())
        product = Product(name, price, stock)
        add_product(product)
        self.load_products()
    
    def edit_product(self):
        selected_item = self.product_table.selection()
        if not selected_item:
            return
        product_id = self.product_table.item(selected_item, "values")[0]
        name = self.product_name_entry.get()
        price = float(self.product_price_entry.get())
        stock = int(self.product_stock_entry.get())
        update_product(product_id, name, price, stock)
        self.load_products()
    
    def delete_product(self):
        selected_item = self.product_table.selection()
        if not selected_item:
            return
        product_id = self.product_table.item(selected_item, "values")[0]
        delete_product(product_id)
        self.load_products()
    
    def load_products(self):
        for row in self.product_table.get_children():
            self.product_table.delete(row)
        products = get_products()
        for product in products:
            self.product_table.insert("", END, values=product)
    
    def setup_services(self):
        # CRUD Form for Services
        form_frame = ttk.Frame(self.services_tab)
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NW)
        
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.service_name_entry = ttk.Entry(form_frame)
        self.service_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Cost:").grid(row=1, column=0, padx=5, pady=5)
        self.service_cost_entry = ttk.Entry(form_frame)
        self.service_cost_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(form_frame, text="Add Service", command=self.add_service).grid(row=2, column=0, pady=10)
        ttk.Button(form_frame, text="Edit Service", command=self.edit_service).grid(row=2, column=1, pady=10)
        ttk.Button(form_frame, text="Delete Service", command=self.delete_service).grid(row=2, column=2, pady=10)
        
        # Table to display services
        columns = ("ID", "Name", "Cost")
        self.service_table = ttk.Treeview(self.services_tab, columns=columns, show="headings")
        for col in columns:
            self.service_table.heading(col, text=col)
        self.service_table.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)
        
        # Load service data into the table
        self.load_services()
    
    def add_service(self):
        name = self.service_name_entry.get()
        cost = float(self.service_cost_entry.get())
        service = Service(name, cost)
        add_service(service)
        self.load_services()
    
    def edit_service(self):
        selected_item = self.service_table.selection()
        if not selected_item:
            return
        service_id = self.service_table.item(selected_item, "values")[0]
        name = self.service_name_entry.get()
        cost = float(self.service_cost_entry.get())
        update_service(service_id, name, cost)
        self.load_services()
    
    def delete_service(self):
        selected_item = self.service_table.selection()
        if not selected_item:
            return
        service_id = self.service_table.item(selected_item, "values")[0]
        delete_service(service_id)
        self.load_services()
    
    def load_services(self):
        for row in self.service_table.get_children():
            self.service_table.delete(row)
        services = get_services()
        for service in services:
            self.service_table.insert("", END, values=service)
    
    def setup_invoices(self):
        # Generate Invoices View
        form_frame = ttk.Frame(self.invoices_tab)
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NW)
        
        ttk.Label(form_frame, text="Customer ID:").grid(row=0, column=0, padx=5, pady=5)
        self.invoice_customer_id_entry = ttk.Entry(form_frame)
        self.invoice_customer_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Product ID:").grid(row=1, column=0, padx=5, pady=5)
        self.invoice_product_id_entry = ttk.Entry(form_frame)
        self.invoice_product_id_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Quantity:").grid(row=2, column=0, padx=5, pady=5)
        self.invoice_product_quantity_entry = ttk.Entry(form_frame)
        self.invoice_product_quantity_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Service ID:").grid(row=3, column=0, padx=5, pady=5)
        self.invoice_service_id_entry = ttk.Entry(form_frame)
        self.invoice_service_id_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Button(form_frame, text="Add Item", command=self.add_invoice_item).grid(row=4, column=0, pady=10)
        ttk.Button(form_frame, text="Generate Invoice", command=self.generate_invoice).grid(row=4, column=1, pady=10)
        
        # Table to display invoice items
        columns = ("Type", "ID", "Quantity", "Price")
        self.invoice_table = ttk.Treeview(self.invoices_tab, columns=columns, show="headings")
        for col in columns:
            self.invoice_table.heading(col, text=col)
        self.invoice_table.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)
        
        # List to store invoice items
        self.invoice_items = []
    
    def add_invoice_item(self):
        product_id = self.invoice_product_id_entry.get()
        service_id = self.invoice_service_id_entry.get()
        quantity = int(self.invoice_product_quantity_entry.get())
        
        if product_id:
            query = "SELECT price FROM products WHERE id = ?"
            price = fetch_query(query, (product_id,))[0][0]
            self.invoice_items.append({"product_id": int(product_id), "quantity": quantity, "price": price})
            self.invoice_table.insert("", END, values=("Product", product_id, quantity, price))
        elif service_id:
            query = "SELECT cost FROM services WHERE id = ?"
            price = fetch_query(query, (service_id,))[0][0]
            self.invoice_items.append({"service_id": int(service_id), "quantity": 1, "price": price})
            self.invoice_table.insert("", END, values=("Service", service_id, 1, price))
    
    def generate_invoice(self):
        customer_id = int(self.invoice_customer_id_entry.get())
        invoice_id = create_invoice(customer_id, self.invoice_items)
        generate_pdf_invoice(invoice_id)
        self.invoice_items.clear()
        for row in self.invoice_table.get_children():
            self.invoice_table.delete(row)
        ttk.messagebox.showinfo("Success", "Invoice generated successfully!")
        
    def setup_daily_close(self):
        # Frame for the summary
        summary_frame = ttk.Frame(self.daily_close_tab)
        summary_frame.pack(fill="x", padx=10, pady=10)

        # Labels for total income, expenses, and net income
        ttk.Label(summary_frame, text="Total Income:").grid(row=0, column=0, padx=5, pady=5)
        self.total_income_label = ttk.Label(summary_frame, text="$0.00")
        self.total_income_label.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(summary_frame, text="Total Expenses:").grid(row=1, column=0, padx=5, pady=5)
        self.total_expenses_label = ttk.Label(summary_frame, text="$0.00")
        self.total_expenses_label.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(summary_frame, text="Net Income:").grid(row=2, column=0, padx=5, pady=5)
        self.net_income_label = ttk.Label(summary_frame, text="$0.00")
        self.net_income_label.grid(row=2, column=1, padx=5, pady=5)

        # Button to calculate daily close
        ttk.Button(summary_frame, text="Calculate Daily Close", command=self.calculate_daily_close).grid(row=3, column=0, columnspan=2, pady=10)

        # Frame for adding expenses
        expense_frame = ttk.Frame(self.daily_close_tab)
        expense_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(expense_frame, text="Description:").grid(row=0, column=0, padx=5, pady=5)
        self.expense_description_entry = ttk.Entry(expense_frame)
        self.expense_description_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(expense_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        self.expense_amount_entry = ttk.Entry(expense_frame)
        self.expense_amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(expense_frame, text="Add Expense", command=self.add_expense).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Table to display invoices for the day
        columns = ("Invoice ID", "Customer", "Total Amount", "Date")
        self.invoice_table = ttk.Treeview(self.daily_close_tab, columns=columns, show="headings")
        for col in columns:
            self.invoice_table.heading(col, text=col)
        self.invoice_table.pack(fill="both", expand=True, padx=10, pady=10)
        
    def calculate_daily_close(self):
        # Get today's date
        today = datetime.datetime.now().strftime("%Y-%m-%d")

        # Fetch all invoices for today
        query = "SELECT id, customer_id, total_amount, invoice_date FROM invoices WHERE invoice_date = ?"
        invoices = fetch_query(query, (today,))

        # Calculate total income
        total_income = sum(invoice[2] for invoice in invoices)

        # Fetch all expenses for today (assuming an expenses table exists)
        query = "SELECT amount FROM expenses WHERE date = ?"
        expenses = fetch_query(query, (today,))
        total_expenses = sum(expense[0] for expense in expenses)

        # Calculate net income
        net_income = total_income - total_expenses

        # Update labels
        self.total_income_label.config(text=f"${total_income:.2f}")
        self.total_expenses_label.config(text=f"${total_expenses:.2f}")
        self.net_income_label.config(text=f"${net_income:.2f}")

        # Clear the invoice table
        for row in self.invoice_table.get_children():
            self.invoice_table.delete(row)

        # Populate the invoice table
        for invoice in invoices:
            invoice_id, customer_id, total_amount, invoice_date = invoice
            customer_name = self.get_customer_name(customer_id)
            self.invoice_table.insert("", "end", values=(invoice_id, customer_name, f"${total_amount:.2f}", invoice_date))
            
    def get_customer_name(self, customer_id):
        query = "SELECT name FROM customers WHERE id = ?"
        result = fetch_query(query, (customer_id,))
        return result[0][0] if result else "Unknown"
    
    def add_expense(self, description, amount, date):
        query = "INSERT INTO expenses (description, amount, date) VALUES (?, ?, ?)"
        execute_query(query, (description, amount, date))
        
    def add_expense(self):
        description = self.expense_description_entry.get()
        amount = float(self.expense_amount_entry.get())
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        # Add the expense to the database
        self.add_expense(description, amount, date)

        # Clear the entry fields
        self.expense_description_entry.delete(0, "end")
        self.expense_amount_entry.delete(0, "end")

        # Recalculate the daily close
        self.calculate_daily_close()

if __name__ == "__main__":
    root = ttk.Window(themename="cosmo")
    app = ManicuristApp(root)
    root.mainloop()