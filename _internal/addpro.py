import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd

# Function to read products from an Excel file
def read_products():
    try:
        products_df = pd.read_excel("products.xlsx")
        return products_df
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read products: {e}")
        return None

# Function to add a new product
def add_product(code, name, price, discount):
    if code and name and price and discount:
        try:
            products_df = pd.read_excel("products.xlsx")
        except FileNotFoundError:
            products_df = pd.DataFrame(columns=["Code", "Name", "Price", "Discount"])

        if code in products_df["Code"].values:
            messagebox.showerror("Error", "Product with this code already exists.")
        else:
            products_df = pd.concat([products_df, pd.DataFrame([{"Code": code, "Name": name, "Price": price, "Discount": discount}])], ignore_index=True)

            products_df.to_excel("products.xlsx", index=False)
            messagebox.showinfo("Success", "Product added successfully.")
            return True
    else:
        messagebox.showerror("Error", "Please fill in all fields.")
        return False

# Function to remove a product
def remove_product(code):
    try:
        # Load the Excel file into a DataFrame
        products_df = pd.read_excel("products.xlsx")
        
        # Check if the product code exists before attempting to remove
        if code not in products_df["Code"].values:
            print(f"Product with code {code} not found.")
            return False
        
        # Filter out the product with the matching code
        products_df = products_df[products_df["Code"] != code]
        
        # Save the updated DataFrame back to the Excel file
        products_df.to_excel("products.xlsx", index=False)
        print(f"Product with code {code} removed successfully.")
        return True

    except FileNotFoundError:
        print("The Excel file 'products.xlsx' does not exist.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Function to create the content of the addpro page
def create_page(parent):
    frame = ttk.Frame(parent)

    def add_product_click():
        code = entry_code.get()
        name = entry_name.get()
        price = entry_price.get()
        discount = entry_discount.get()
        add_product(code, name, price, discount)
        update_product_list()

    def remove_product_click():
        selected_index = product_list.curselection()
        if selected_index:
            selected_product = product_list.get(selected_index)
            selected_code = selected_product.split()[0]  # Extract code from the selected product
            remove_product(selected_code)
            update_product_list()


    label_code = ttk.Label(frame, text="Product Code:")
    label_code.grid(row=0, column=0)
    entry_code = ttk.Entry(frame)
    entry_code.grid(row=0, column=1)

    label_name = ttk.Label(frame, text="Product Name:")
    label_name.grid(row=1, column=0)
    entry_name = ttk.Entry(frame)
    entry_name.grid(row=1, column=1)

    label_price = ttk.Label(frame, text="Price:")
    label_price.grid(row=2, column=0)
    entry_price = ttk.Entry(frame)
    entry_price.grid(row=2, column=1)

    label_discount = ttk.Label(frame, text="Discount:")
    label_discount.grid(row=3, column=0)
    entry_discount = ttk.Entry(frame)
    entry_discount.grid(row=3, column=1)

    btn_add_product = ttk.Button(frame, text="Add Product", command=add_product_click)
    btn_add_product.grid(row=4, column=0, columnspan=2)
    style = ttk.Style()
    style.configure("Custom.TButton",foreground='#ff3300')
    btn_remove_product = ttk.Button(frame, text="Remove Product", command=remove_product_click,style='Custom.TButton')
    btn_remove_product.grid(row=5, column=0, columnspan=2)

    label_existing = ttk.Label(frame, text="Existing Products:")
    label_existing.grid(row=6, column=0, columnspan=2)

    product_list = tk.Listbox(frame, height=10, width=50)
    product_list.grid(row=10, column=0, columnspan=2)

    def update_product_list():
        product_list.delete(0, tk.END)
        product_list.insert(tk.END, "Code - Name - Price - Discount")
        try:
            products_df = pd.read_excel("products.xlsx")
            for _, product in products_df.iterrows():
                product_info = f"{product['Code']} - {product['Name']} - {product['Price']} - {product['Discount']}"
                product_list.insert(tk.END, product_info)
        except FileNotFoundError:
            pass

    update_product_list()

    return frame
