import tkinter as tk
from tkinter import ttk, messagebox
from logic import (
    LineItem,
    compute_totals,
    SCOOP_PRICE,
    SUNDAE3_PRICE,
    SHAKE_SMALL,
    CANDY_PRICE,
)

class IceCreamApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Monroe Ice Cream Parlor")
        self.geometry("850x600")
        self.items = []
        self.create_widgets()

    def create_widgets(self):
        info_frame = ttk.LabelFrame(self, text="Customer Info")
        info_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(info_frame, text="Order ID:").grid(row=0, column=0, padx=5, pady=3)
        self.order_id_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.order_id_var, width=20).grid(row=0, column=1)

        ttk.Label(info_frame, text="Customer Name:").grid(row=0, column=2, padx=5)
        self.cmr_name_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.cmr_name_var, width=20).grid(row=0, column=3)

        ttk.Label(info_frame, text="Student ID:").grid(row=1, column=0, padx=5)
        self.student_id_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.student_id_var, width=20).grid(row=1, column=1)

        self.senior_var = tk.BooleanVar()
        self.student_var = tk.BooleanVar()
        ttk.Checkbutton(info_frame, text="Senior (15%)", variable=self.senior_var).grid(row=1, column=2)
        ttk.Checkbutton(info_frame, text="Student (10%)", variable=self.student_var).grid(row=1, column=3)

        item_frame = ttk.LabelFrame(self, text="Add Item")
        item_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(item_frame, text="Category:").grid(row=0, column=0, padx=5, pady=3)
        self.category_var = tk.StringVar(value="Scoops")
        categories = ["Scoops", "Sundae", "Shake", "Candy", "Other"]
        ttk.Combobox(item_frame, textvariable=self.category_var, values=categories, width=12).grid(row=0, column=1)

        ttk.Label(item_frame, text="Description:").grid(row=0, column=2, padx=5)
        self.desc_var = tk.StringVar()
        ttk.Entry(item_frame, textvariable=self.desc_var, width=35).grid(row=0, column=3)

        ttk.Label(item_frame, text="Price ($):").grid(row=0, column=4)
        self.price_var = tk.StringVar()
        ttk.Entry(item_frame, textvariable=self.price_var, width=10).grid(row=0, column=5)

        ttk.Button(item_frame, text="Quick Price", command=self.quick_price).grid(row=1, column=1, pady=3)
        ttk.Button(item_frame, text="Add Item", command=self.add_item).grid(row=1, column=3)

        list_frame = ttk.LabelFrame(self, text="Order Items")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(list_frame, columns=("category", "description", "price"), show="headings", height=8)
        self.tree.heading("category", text="Category")
        self.tree.heading("description", text="Description")
        self.tree.heading("price", text="Price ($)")
        self.tree.column("category", width=120)
        self.tree.column("description", width=450)
        self.tree.column("price", width=80)
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        ttk.Button(list_frame, text="Remove Item", command=self.remove_item).pack(pady=5)

        bottom_frame = ttk.LabelFrame(self, text="Payment")
        bottom_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(bottom_frame, text="Payment ($):").grid(row=0, column=0, padx=5)
        self.payment_var = tk.StringVar()
        ttk.Entry(bottom_frame, textvariable=self.payment_var, width=12).grid(row=0, column=1)

        ttk.Button(bottom_frame, text="Calculate Total", command=self.calculate_total).grid(row=0, column=2, padx=10)

        self.result_text = tk.Text(bottom_frame, width=90, height=8, state="disabled")
        self.result_text.grid(row=1, column=0, columnspan=4, padx=5, pady=10)

    def quick_price(self):
        c = self.category_var.get()
        if c == "Scoops":
            self.price_var.set(f"{SCOOP_PRICE:.2f}")
        elif c == "Sundae":
            self.price_var.set(f"{SUNDAE3_PRICE:.2f}")
        elif c == "Shake":
            self.price_var.set(f"{SHAKE_SMALL:.2f}")
        elif c == "Candy":
            self.price_var.set(f"{CANDY_PRICE:.2f}")

    def add_item(self):
        cat = self.category_var.get()
        desc = self.desc_var.get()
        price_str = self.price_var.get()

        if desc == "" or price_str == "":
            messagebox.showerror("Error", "Description and price required.")
            return

        try:
            price = float(price_str)
        except:
            messagebox.showerror("Error", "Price must be a number.")
            return

        item = LineItem(cat, desc, round(price, 2))
        self.items.append(item)
        self.tree.insert("", "end", values=(cat, desc, f"{price:.2f}"))

        self.desc_var.set("")
        self.price_var.set("")

    def remove_item(self):
        selected = self.tree.selection()
        if not selected:
            return
        idx = self.tree.index(selected[0])
        self.tree.delete(selected[0])
        self.items.pop(idx)

    def calculate_total(self):
        cmrName = self.cmr_name_var.get().strip()
        if cmrName == "":
            messagebox.showerror("Error", "Customer name required.")
            return

        if not self.items:
            messagebox.showerror("Error", "Add at least one item.")
            return

        try:
            paymentAmt = float(self.payment_var.get())
        except:
            messagebox.showerror("Error", "Payment must be valid number.")
            return

        senior = "Y" if self.senior_var.get() else "N"
        student = "Y" if self.student_var.get() else "N"
        sid = self.student_id_var.get().strip()

        try:
            totals = compute_totals(self.items, senior, student, sid, paymentAmt)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)

        self.result_text.insert(tk.END, f"Customer: {cmrName}\n")
        if sid:
            self.result_text.insert(tk.END, f"Student ID: {sid}\n")
        self.result_text.insert(tk.END, "-"*60 + "\n")

        for it in self.items:
            self.result_text.insert(tk.END, f"{it.category}: {it.description} - ${it.price:.2f}\n")

        self.result_text.insert(tk.END, "-"*60 + "\n")
        self.result_text.insert(tk.END, f"Subtotal: ${totals['subTotal']:.2f}\n")
        if totals['discSenior'] > 0:
            self.result_text.insert(tk.END, f"Senior 15%: -${totals['discSenior']:.2f}\n")
        if totals['discFivePlus'] > 0:
            self.result_text.insert(tk.END, f">5 Items 10%: -${totals['discFivePlus']:.2f}\n")
        if totals['discStudent'] > 0:
            self.result_text.insert(tk.END, f"Student 10%: -${totals['discStudent']:.2f}\n")

        self.result_text.insert(tk.END, f"Subtotal After Discounts: ${totals['subTotalAfterDiscounts']:.2f}\n")
        self.result_text.insert(tk.END, f"Tax: ${totals['taxAmount']:.2f}\n")
        self.result_text.insert(tk.END, f"TOTAL: ${totals['totalAmount']:.2f}\n")
        self.result_text.insert(tk.END, f"Payment: ${totals['paymentAmt']:.2f}\n")
        self.result_text.insert(tk.END, f"Change: ${totals['changeDue']:.2f}\n")

        self.result_text.config(state="disabled")

if __name__ == "__main__":
    app = IceCreamApp()
    app.mainloop()
