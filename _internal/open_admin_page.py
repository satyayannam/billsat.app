import tkinter as tk
import webbrowser
from tkinter import ttk

import addpro
import bill
import transactions


class MainApp(tk.Tk):
    def open_email(self):
        webbrowser.open_new("mailto:xensindo@gmail.com")

    def __init__(self):
        super().__init__()
        self.title("Home")
        self.geometry("800x600")
        self.minsize(height=800,width=800)
        self.style = ttk.Style()
        self.style.configure("Custom.TFrame", background="#b3ffcc")

        # Create a side menu bar
        self.side_menu = ttk.Frame(self, width=200, height=600,style='Custom.TFrame')
        self.side_menu.pack(side=tk.LEFT, fill=tk.Y)

        # Create buttons in the side menu
        self.button1 = ttk.Button(self.side_menu, text="Add Products", command=self.show_add_products)
        self.button1.pack(pady=10)
        self.button2 = ttk.Button(self.side_menu, text="Bill", command=self.show_other_module1)
        self.button2.pack(pady=10)
        self.button3 = ttk.Button(self.side_menu, text="Transactions", command=self.show_other_module2)
        self.button3.pack(pady=10)

        # Create a content area
        self.content_area = ttk.Frame(self, width=1200, height=1200)
        self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Instructions label
        self.instructions = ttk.Label(self.content_area, text="Welcome to the Billsat v1.0\n\n"
                                                               "Instructions:\n"
                                                               "• Click 'Add Products' to add new products.\n"
                                                               "• Click 'Bill' to create a new bill.\n"
                                                               "• Click 'Transactions' to view transaction history.\n"
                                                               "\nThank you for using our application!",
                                       justify="left", font=("AngsanaUPC", 8))
        self.instructions.pack(expand=True)
        self.label = ttk.Label(self.content_area, text="Have a question? Click below to email us:")
        self.label.pack(pady=10)

        self.button = ttk.Button(self.content_area, text="Email Us", command=self.open_email)
        self.button.pack(pady=10)


    def show_add_products(self):
        # Clear previous content
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Call the create_page function of addpro.py
        frame = addpro.create_page(self.content_area)
        frame.pack(fill="both", expand=True, padx=200, pady=100)


    def show_other_module1(self):
        # Clear previous content
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Call the create_page function of other_module1.py
        frame = bill.create_bill_page(self.content_area)
        frame.pack(fill=tk.BOTH, expand=True)

    def show_other_module2(self):
        # Clear previous content
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Call the create_page function of other_module2.py
        frame = transactions.display_transactions_page(self.content_area)
        frame.pack(fill=tk.BOTH, expand=True)
    #
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
