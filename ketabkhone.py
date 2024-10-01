import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

def back_end():
    with sqlite3.connect('backend.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                price REAL,
                quantity INTEGER
            )
        ''')

class ProductManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Product Manager")
        self.root.geometry("300x400")
        self.root.config(bg="navy")

        frame = tk.Frame(self.root, bg="navy")
        frame.pack(pady=10)

        self.name_label = tk.Label(frame, text="Product Name:", bg="cyan")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(frame, bg="dodger blue")
        self.name_entry.grid(row=0, column=1)

        self.price_label = tk.Label(frame, text="Price:", bg="cyan")
        self.price_label.grid(row=1, column=0)
        self.price_entry = tk.Entry(frame, bg="dodger blue")
        self.price_entry.grid(row=1, column=1)

        self.quantity_label = tk.Label(frame, text="Quantity:", bg="cyan")
        self.quantity_label.grid(row=2, column=0)
        self.quantity_entry = tk.Entry(frame, bg="dodger blue")
        self.quantity_entry.grid(row=2, column=1)

        self.add_button = tk.Button(frame, text="Add Product", command=self.add_product, bg="cyan")
        self.add_button.grid(row=3, column=0)

        self.search_button = tk.Button(frame, text="Search Product", command=self.search_product, bg="cyan")
        self.search_button.grid(row=3, column=1)

        self.edit_button = tk.Button(frame, text="Edit Product", command=self.edit_product, bg="cyan")
        self.edit_button.grid(row=4, column=0)

        self.delete_button = tk.Button(frame, text="Delete Product", command=self.delete_product, bg="cyan")
        self.delete_button.grid(row=4, column=1)

        self.close_button = tk.Button(frame, text="Close", command=self.root.quit, bg="cyan")
        self.close_button.grid(row=5, columnspan=2)

        self.product_list = tk.Listbox(self.root, bg="dodger blue")
        self.product_list.pack(pady=10)

        self.scrollbar = tk.Scrollbar(self.root, bg="dodger blue")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.product_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.product_list.yview)

        self.product_list.bind('<<ListboxSelect>>', self.on_product_select)

        self.load_products()

    def load_products(self):
        self.product_list.delete(0, tk.END)
        with sqlite3.connect('backend.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM products")
            products = cursor.fetchall()
            for product in products:
                self.product_list.insert(tk.END, product[0])

    def on_product_select(self, event):
        if self.product_list.curselection():
            selected_product = self.product_list.get(self.product_list.curselection())
            with sqlite3.connect('backend.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM products WHERE name=?", (selected_product,))
                product = cursor.fetchone()
            if product:
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, product[1])
                self.price_entry.delete(0, tk.END)
                self.price_entry.insert(0, product[2])
                self.quantity_entry.delete(0, tk.END)
                self.quantity_entry.insert(0, product[3])

    def add_product(self):
        name = self.name_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()

        if not name or not price or not quantity:
            messagebox.showwarning("Input Error", "All fields must be filled out.")
            return

        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            messagebox.showwarning("Input Error", "Price must be a number and Quantity must be an integer.")
            return

        with sqlite3.connect('backend.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))

        self.load_products()
        messagebox.showinfo("Success", "Product added successfully!")
        self.clear_entries()

    def search_product(self):
        name = self.name_entry.get()
        with sqlite3.connect('backend.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE name=?", (name,))
            product = cursor.fetchone()

        if product:
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, product[2])
            self.quantity_entry.delete(0, tk.END)
            self.quantity_entry.insert(0, product[3])
            messagebox.showinfo("Found", "Product found!")
        else:
            messagebox.showwarning("Not Found", "Product not found!")

    def edit_product(self):
        if self.product_list.curselection():
            selected_product = self.product_list.get(self.product_list.curselection())
            name = self.name_entry.get()
            price = self.price_entry.get()
            quantity = self.quantity_entry.get()

            if not name or not price or not quantity:
                messagebox.showwarning("Input Error", "All fields must be filled out.")
                return

            try:
                price = float(price)
                quantity = int(quantity)
            except ValueError:
                messagebox.showwarning("Input Error", "Price must be a number and Quantity must be an integer.")
                return

            with sqlite3.connect('backend.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE products SET name=?, price=?, quantity=? WHERE name=?", (name, price, quantity, selected_product))

            self.load_products()
            messagebox.showinfo("Success", "Product edited successfully!")
            self.clear_entries()

    def delete_product(self):
        if self.product_list.curselection():
            selected_product = self.product_list.get(self.product_list.curselection())
            with sqlite3.connect('backend.db') as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM products WHERE name=?", (selected_product,))

            self.load_products()
            messagebox.showinfo("Success", "Product deleted successfully!")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)

if __name__ == "__main__":
    back_end()
    root = tk.Tk()
    app = ProductManager(root)
    root.mainloop()
