import tkinter as tk
from tkinter import ttk, messagebox
from logic import LineItem, compute_totals, SCOOP_PRICE, SUNDAE3_PRICE, SHAKE_SMALL, CANDY_PRICE

class IceCreamApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Monroe Ice Cream Parlor")
        self.geometry("800x550")
        self.items = []
        self.create_widgets()

    # … (same widget + helper methods we wrote before) …

if __name__ == "__main__":
    app = IceCreamApp()
    app.mainloop()
