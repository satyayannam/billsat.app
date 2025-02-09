import os
import tkinter as tk
from tkinter import messagebox
from addpro import read_products
import pandas as pd
from datetime import datetime
from PIL import ImageTk, Image

def create_bill_page(parent):
    # Create a frame for the bill page
    frame = tk.Frame(parent, width=600, height=400)
    frame.pack_propagate(False)  # Prevent the frame from resizing
    frame.pack(pady=20)  # Place the frame in the center with padding

    def add_product_to_bill(product):
        text_bill.insert(tk.END, f"{product['Name']} - {product['Price']} - {product['Discount']}\n")

    def add_product_dropdown():
        selected_product = option_var.get()
        product = get_product_by_name(selected_product)
        if product:
            add_product_to_bill(product)
        else:
            messagebox.showerror("Error", "Product not found")

    # Create a label for the bill
    label_bill = tk.Label(frame, text="Bill Details")
    label_bill.pack()

    # Create a text widget to display the bill
    text_bill = tk.Text(frame, height=10, width=50)
    text_bill.pack()

    # Function to get product details by name
    def get_product_by_name(name):
        products_df = read_products()
        if products_df is not None:
            product = products_df[products_df["Name"] == name]
            if not product.empty:
                return {"Name": product.iloc[0]["Name"], "Price": product.iloc[0]["Price"],
                        "Discount": product.iloc[0]["Discount"]}
        return None

    # Create a dropdown menu for product selection
    products_df = read_products()
    if products_df is not None:
        product_names = products_df["Name"].tolist()
        option_var = tk.StringVar(frame)
        option_var.set(product_names[0])  # Default value
        option_menu = tk.OptionMenu(frame, option_var, *product_names)
        option_menu.pack()

        # Add Product button for dropdown selection
        btn_add_product_dropdown = tk.Button(frame, text="Add Selected Product", command=add_product_dropdown)
        btn_add_product_dropdown.pack()


    # Function to remove a product from the bill
    def remove_product_from_bill():
        text_bill.delete("end-2l", tk.END)  # Delete the last line

    # Remove Product button
    btn_remove_product = tk.Button(frame, text="Remove Last Product", command=remove_product_from_bill)
    btn_remove_product.pack()

    # Function to calculate and show the total bill amount
    def calculate_total():
        total = 0
        products = []
        for line in text_bill.get("1.0", tk.END).splitlines():
            if line:
                name, price, discount = line.split(" - ")
                total += float(price) * (1 - float(discount) / 100)
                products.append({"Name": name, "Price": price, "Discount": discount})
        # Show cash or UPI buttons
        btn_done.config(state=tk.DISABLED)
        btn_cash = tk.Button(frame, text="Pay with Cash", command=lambda: show_payment("Cash", total, products),foreground='#339933')
        btn_cash.pack()
        btn_upi = tk.Button(frame, text="Pay with UPI", command=lambda: show_payment("UPI", total, products),foreground='#0033cc')
        btn_upi.pack()

    # Done button to calculate the total bill amount
    btn_done = tk.Button(frame, text="Done", command=calculate_total)
    btn_done.pack()

    # Function to show payment options
    def show_payment(method, total, products):
        if method == "Cash":
            messagebox.showinfo("Payment", f"Total Amount: {total}")


            btn_payment_completed = tk.Button(frame, text="Payment Completed?",
                                              command=lambda: store_transaction_details(total, products),foreground='#00cc00')
            btn_payment_completed.pack()
        elif method == "UPI":
            # Show image, total amount, and payment completed button
            upi_image = Image.open("upi.jpg")
            upi_image = upi_image.resize((200, 200), Image.BICUBIC)  # Use Image.BICUBIC or Image.LANCZOS for resizing
            upi_image = ImageTk.PhotoImage(upi_image)
            label_image = tk.Label(frame, image=upi_image)
            label_image.image = upi_image
            label_image.pack()
            label_total = tk.Label(frame, text=f"Total Amount: {total}")
            label_total.pack()
            btn_payment_completed = tk.Button(frame, text="Payment Completed?",
                                              command=lambda: store_transaction_details(total, products),foreground='#00cc00')
            btn_payment_completed.pack()

    # Function to store transaction details in an Excel file
    # def store_transaction_details(total, products):
    #     transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     product_data = []
    #     for product in products:
    #         product_data.append({"Name": product['Name'], "Price": product['Price'], "Discount": product['Discount']})
    # #     transaction_df = pd.DataFrame(
    # #         {"Transaction Time": [transaction_time], "Total Amount": [total], "Products": [product_data]})
    #     try:
    #         transaction_df.to_excel("transaction_details.xlsx", index=False,
    #                                 header=not os.path.exists("transaction_details.xlsx"))
    #         messagebox.showinfo("Success", "Transaction details stored successfully")
    #     except Exception as e:
    #         messagebox.showerror("Error", f"Failed to store transaction details: {e}")

    def store_transaction_details(total, products):
        transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_transaction = pd.DataFrame(
            {"Transaction Time": [transaction_time], "Total Amount": [total], "Products": [products]})
        try:
            if os.path.exists("transaction_details.xlsx"):
                existing_data = pd.read_excel("transaction_details.xlsx")
                updated_data = pd.concat([existing_data, new_transaction], ignore_index=True)
                updated_data.to_excel("transaction_details.xlsx", index=False)
            else:
                new_transaction.to_excel("transaction_details.xlsx", index=False)
            messagebox.showinfo("Success", "Transaction details stored successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to store transaction details: {e}")

    return frame
