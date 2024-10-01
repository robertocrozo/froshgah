
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

def BackEnd():
    x = sqlite3.connect('backend.db')
    cursor = x.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL,
            quantity INTEGER
        )
    ''')
    x.commit()
    x.close()


class froshghah:
    def __init__(self, root):
        self.root = root
        self.root.title("FrontEnd")
        self.root.geometry("250x320")
        self.root.config(bg="navy")
        
        
        # فریم ورودی
        frame = tk.Frame(self.root,bg="navy")
        frame.pack(pady=10)

        
        # ورودی نام کالا
        self.name_label = tk.Label(frame, text="name mahsol:",bg="cyan")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(frame,bg="dodger blue")
        self.name_entry.grid(row=0, column=1)
        
        # ورودی قیمت کالا
        self.price_label = tk.Label(frame, text="ghaymat:",bg="cyan")
        self.price_label.grid(row=1, column=0)
        self.price_entry = tk.Entry(frame ,bg="dodger blue")
        self.price_entry.grid(row=1, column=1)
        
        # ورودی تعداد کالا
        self.quantity_label = tk.Label(frame, text="meghdar:",bg="cyan")
        self.quantity_label.grid(row=2, column=0)
        self.quantity_entry = tk.Entry(frame ,bg="dodger blue")
        self.quantity_entry.grid(row=2, column=1)
        
        # دکمه‌ها
        self.add_button = tk.Button(frame, text="Add Product", command=self.add_product ,bg="cyan")
        self.add_button.grid(row=3, column=0)
        
        self.search_button = tk.Button(frame, text="Search Product", command=self.search_product ,bg="cyan")
        self.search_button.grid(row=3, column=1)
        
        self.edit_button = tk.Button(frame, text="Edit Product", command=self.edit_product ,bg="cyan")
        self.edit_button.grid(row=4, column=0)
        
        self.delete_button = tk.Button(frame, text="Delete Product", command=self.delete_product ,bg="cyan")
        self.delete_button.grid(row=4, column=1)

        self.close_button = tk.Button(frame, text="Close", command=self.root.quit ,bg="cyan")
        self.close_button.grid(row=5, columnspan=2)
        
        # لیست باکس
        self.product_list = tk.Listbox(self.root,bg="dodger blue")
        self.product_list.pack(pady=10)
        
        self.scrollbar = tk.Scrollbar(self.root,bg="dodger blue")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.product_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.product_list.yview)

        self.product_list.bind('<<ListboxSelect>>', self.on_product_select)

        self.load_products()

    def load_products(self):
        self.product_list.delete(0, tk.END)
        x = sqlite3.connect('backend.db')
        cursor = x.cursor()
        cursor.execute("SELECT name FROM products")
        products = cursor.fetchall()
        for product in products:
            self.product_list.insert(tk.END, product[0])
        x.close()

    def on_product_select(self, event):
        selected_product = self.product_list.get(self.product_list.curselection())
        x = sqlite3.connect('backend.db')
        cursor = x.cursor()
        cursor.execute("SELECT * FROM products WHERE name=?", (selected_product,))
        product = cursor.fetchone()
        x.close()
        if product:
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, product[1])
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, product[2])
            self.quantity_entry.delete(0, tk.END)
            self.quantity_entry.insert(0, product[3])

    def add_product(self):
        name = self.name_entry.get()
        price = float(self.price_entry.get())
        quantity = int(self.quantity_entry.get())
        x = sqlite3.connect('backend.db')
        cursor = x.cursor()
        cursor.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
        x.commit()
        x.close()
        self.load_products()
        messagebox.showinfo("Success", "Product added successfully!")

    def search_product(self):
        name = self.name_entry.get()
        x = sqlite3.connect('backend.db')
        cursor = x.cursor()
        cursor.execute("SELECT * FROM products WHERE name=?", (name,))
        product = cursor.fetchone()
        x.close()
        if product:
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, product[2])
            self.quantity_entry.delete(0, tk.END)
            self.quantity_entry.insert(0, product[3])
            messagebox.showinfo("Found", "Product found!")
        else:
            messagebox.showwarning("Not Found", "Product not found!")

    def edit_product(self):
        selected_product = self.product_list.get(self.product_list.curselection())
        name = self.name_entry.get()
        price = float(self.price_entry.get())
        quantity = int(self.quantity_entry.get())
        x = sqlite3.connect('supermarket.db')
        cursor = x.cursor()
        cursor.execute("UPDATE products SET name=?, price=?, quantity=? WHERE name=?", (name, price, quantity, selected_product))
        x.commit()
        x.close()
        self.load_products()
        messagebox.showinfo("Success", "Product edited successfully!")

    def delete_product(self):
        selected_product = self.product_list.get(self.product_list.curselection())
        x = sqlite3.connect('backend.db')
        cursor = x.cursor()
        cursor.execute("DELETE FROM products WHERE name=?", (selected_product,))
        x.commit()
        x.close()
        self.load_products()
        messagebox.showinfo("Success", "Product deleted successfully!")

# ایجاد پایگاه داده و اجرای برنامه
BackEnd()
root = tk.Tk()
app = froshghah(root)
root.mainloop()
