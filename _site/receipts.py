import csv
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from datetime import datetime, timedelta
import threading
import time
import random

TAX_RATE = 0.06
DISCOUNT_ITEM = "D083"

class GroceryReceiptApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grocery Store Receipt Generator")
        self.root.geometry("700x600")

        self.products_btn = tk.Button(root, text="Select products.csv", command=self.load_products)
        self.products_btn.pack(pady=5)

        self.request_btn = tk.Button(root, text="Select request.csv", command=self.load_request)
        self.request_btn.pack(pady=5)

        self.generate_btn = tk.Button(root, text="Generate Receipt", command=self.generate_receipt)
        self.generate_btn.pack(pady=10)

        self.output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=25, font=("Courier", 10))
        self.output.pack(padx=10, pady=10)

        self.products_file = None
        self.request_file = None

    def load_products(self):
        self.products_file = filedialog.askopenfilename(title="Open products.csv", filetypes=[("CSV Files", "*.csv")])
        if self.products_file:
            self.output.insert(tk.END, f"Loaded: {self.products_file}\n")

    def load_request(self):
        self.request_file = filedialog.askopenfilename(title="Open request.csv", filetypes=[("CSV Files", "*.csv")])
        if self.request_file:
            self.output.insert(tk.END, f"Loaded: {self.request_file}\n")

    def generate_receipt(self):
        if not self.products_file or not self.request_file:
            messagebox.showerror("Missing File", "Please select both products.csv and request.csv.")
            return
        self.output.insert(tk.END, "\nGenerating receipt...\n")
        self.output.see(tk.END)
        self.output.update()


        threading.Thread(target=self.run_receipt_logic).start()

    def run_receipt_logic(self):
        time.sleep(1)  
        self.output.insert(tk.END, "Loading data [")
        for _ in range(20):
            time.sleep(0.05)
            self.output.insert(tk.END, "█")
            self.output.update()
        self.output.insert(tk.END, "] Done!\n\n")
        self.output.update()

        try:
            products_dict = self.read_dictionary(self.products_file, 0)

            with open(self.request_file, mode="r", newline='', encoding="utf-8") as request_file:
                reader = csv.reader(request_file)
                next(reader)

                self.output.insert(tk.END, "Inkom Emporium\n\n")

                total_items = 0
                subtotal = 0.0
                purchased_items = []

                for row in reader:
                    try:
                        product_id, quantity = row[0], int(row[1])
                        product = products_dict[product_id]
                        name = product[1]
                        price = float(product[2])

                        if product_id == DISCOUNT_ITEM:
                            full_price_qty = quantity // 2 + quantity % 2
                            half_price_qty = quantity // 2
                            line_total = full_price_qty * price + half_price_qty * (price * 0.5)
                            self.output.insert(tk.END, f"{name}: {quantity} @ {price:.2f} (BOGO 50% applied)\n")
                        else:
                            line_total = quantity * price
                            self.output.insert(tk.END, f"{name}: {quantity} @ {price:.2f}\n")

                        subtotal += line_total
                        total_items += quantity
                        purchased_items.append((product_id, name))
                    except KeyError:
                        self.output.insert(tk.END, f"Error: unknown product ID {row[0]!r}\n")
                        return

                self.output.insert(tk.END, f"\nNumber of Items: {total_items}\n")
                self.output.insert(tk.END, f"Subtotal: {subtotal:.2f}\n")
                sales_tax = subtotal * TAX_RATE
                self.output.insert(tk.END, f"Sales Tax: {sales_tax:.2f}\n")
                total = subtotal + sales_tax
                self.output.insert(tk.END, f"Total: {total:.2f}\n")
                self.output.insert(tk.END, "Thank you for shopping at the Inkom Emporium.\n")

                now = datetime.now()
                self.output.insert(tk.END, f"{now:%a %b %d %I:%M:%S %Y}\n")

                return_by = now + timedelta(days=30)
                return_by = return_by.replace(hour=21, minute=0, second=0)
                self.output.insert(tk.END, f"Items may be returned until {return_by:%a %b %d %I:%M %p %Y}\n")

                new_year = datetime(now.year + 1, 1, 1)
                days_left = (new_year - now).days
                self.output.insert(tk.END, f"{days_left} days until the New Year's Sale!\n")

                if purchased_items:
                    coupon_item = random.choice(purchased_items)
                    self.output.insert(tk.END, f"\nCoupon: Save 10% on your next purchase of {coupon_item[1]}!\n")

        except FileNotFoundError as e:
            self.output.insert(tk.END, f"Error: missing file\n{e}\n")
        except PermissionError as e:
            self.output.insert(tk.END, f"Error: permission denied\n{e}\n")

    def read_dictionary(self, filename, key_column_index):
        dictionary = {}
        with open(filename, mode="r", newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                if len(row) > key_column_index:
                    key = row[key_column_index]
                    dictionary[key] = row
        return dictionary


if __name__ == "__main__":
    root = tk.Tk()
    app = GroceryReceiptApp(root)
    root.mainloop()
