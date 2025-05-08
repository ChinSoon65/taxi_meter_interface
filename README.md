### Persistent Balance
    Save the balance to a file (like a .json or .txt) and load it when the app starts.

### Top-Up via Simulated QR Code

    Show a top-up menu with $10, $20, $50, $100, and custom input.

    When an amount is chosen, generate a placeholder QR code image.

    On clicking the QR code, simulate a successful transaction, update the balance, and save it.

### Deduction with Ctrl + P

    Bind Ctrl + P to a function that randomly deducts between $0.60 and $5.36.

    Play a beep sound using winsound.Beep() before deduction.

    If the balance would drop below zero, show a warning popup instead.

### Prevent Balance from Reaching $0.00

    Before any deduction, check if the balance is sufficient.

    If not, show a tk.messagebox.showwarning().

Would you like help implementing the persistent balance and top-up menu first?

✅ Step 1: Add Persistent Balance Storage
We'll use a simple balance.txt file to store the balance.

🔧 Modify __init__ to load the balance:

python
Copy code

self.balance_file = "balance.txt"
self.balance = self.load_balance()
🔧 Add this function to load the balance:

python
Copy code

def load_balance(self):
    try:
        with open(self.balance_file, "r") as file:
            return float(file.read())
    except (FileNotFoundError, ValueError):
        return 0.00  # Default starting balance
🔧 Add this function to save the balance:

python
Copy code

def save_balance(self):
    with open(self.balance_file, "w") as file:
        file.write(str(self.balance))

✅ Step 2: Show Balance in Label Dynamically
Replace your hardcoded balance string like balance_amount = "$0.00" with:

python
Copy code

balance_amount = f"${self.balance:.2f}"
You can also assign the label once (e.g. self.balance_label = tk.Label(...)) and then later update it like:

python
Copy code

self.balance_label.config(text=f"${self.balance:.2f}")



### Done till this part

✅ Step 3: Add Top-Up Menu (Fixed Amounts)
Create a function to show top-up options:

python
Copy code

def show_top_up_menu(self):
    self.clear_screen()

    amounts = [10, 20, 50, 100]

    for amount in amounts:
        btn = tk.Button(self, text=f"Top Up ${amount}", command=lambda amt=amount: self.simulate_qr_code(amt))
        btn.pack(pady=5)

    custom_btn = tk.Button(self, text="Custom Amount", command=self.custom_top_up_prompt)
    custom_btn.pack(pady=10)

✅ Step 4: Simulate QR Code & Complete Top-Up

python
Copy code

def simulate_qr_code(self, amount):
    self.clear_screen()

    # Placeholder for QR code (you can load an image)
    label = tk.Label(self, text="(QR Code Placeholder)", font=("Helvetica", 14), fg="white", bg="#000033")
    label.pack(pady=20)

    # Clicking simulates successful payment
    label.bind("<Button-1>", lambda e: self.complete_top_up(amount))

python
Copy code

def complete_top_up(self, amount):
    self.balance += amount
    self.save_balance()
    self.show_main_menu()