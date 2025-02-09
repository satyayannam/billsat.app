import tkinter as tk
from tkinter import messagebox
import pandas as pd

def display_transactions_page(parent):
    # Read transactions from Excel file
    try:
        transactions_df = pd.read_excel("transaction_details.xlsx")
        transactions_df = transactions_df.sort_values(by="Transaction Time", ascending=False)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read transactions: {e}")
        return

    # Create a frame for the transactions page
    frame = tk.Frame(parent, width=600, height=400)
    frame.pack_propagate(False)  # Prevent the frame from resizing
    frame.pack(pady=20)  # Place the frame in the center with padding

    # Create a label for the transactions
    label_transactions = tk.Label(frame, text="Transaction Details")
    label_transactions.pack()

    # Create a text widget to display the transactions
    text_transactions = tk.Text(frame, height=10, width=50)
    text_transactions.pack()

    # Display transactions
    for index, transaction in transactions_df.iterrows():
        text_transactions.insert(tk.END, f"Transaction Time: {transaction['Transaction Time']}\n")
        text_transactions.insert(tk.END, f"Total Amount: {transaction['Total Amount']}\n")
        for product in eval(transaction['Products']):
            text_transactions.insert(tk.END, f"{product['Name']} x{product.get('Quantity', 1)} - {product['Price']} - {product['Discount'] + '%'}\n")
        text_transactions.insert(tk.END, "\n")

    return frame

