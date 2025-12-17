import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import math
from datetime import datetime

# --- COLOR PALETTE ---
COLOR_BG = "#121212"       # Deep Black
COLOR_FG = "#D4AF37"       # Metallic Gold
COLOR_ENTRY_BG = "#FFFFFF" # White
COLOR_ENTRY_FG = "#000000" # Black Text
FONT_HEADER = ("Times New Roman", 14, "bold")
FONT_BODY = ("Helvetica", 10)
FONT_RESULT = ("Times New Roman", 13, "bold")

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Financial Suite-Gold Edition-by Walter Clinton-Shakinmyhead LLC.")
        self.root.geometry("700x750") # Slightly taller for the budget list
        self.root.configure(bg=COLOR_BG)

        # --- STYLE CONFIGURATION ---
        style = ttk.Style()
        style.theme_use('clam') 

        # Generic Widget Styles
        style.configure(".", background=COLOR_BG, foreground=COLOR_FG, font=FONT_BODY)
        style.configure("TLabel", background=COLOR_BG, foreground=COLOR_FG)
        style.configure("TFrame", background=COLOR_BG)
        
        # Label Frames
        style.configure("TLabelframe", background=COLOR_BG, foreground=COLOR_FG, bordercolor=COLOR_FG)
        style.configure("TLabelframe.Label", background=COLOR_BG, foreground=COLOR_FG, font=("Times New Roman", 11, "italic"))

        # Input Entries
        style.configure("TEntry", fieldbackground=COLOR_ENTRY_BG, foreground=COLOR_ENTRY_FG, insertcolor="black")
        
        # Buttons
        style.configure("TButton", 
                        background=COLOR_FG, 
                        foreground="#000000", 
                        font=("Helvetica", 10, "bold"),
                        borderwidth=1)
        style.map("TButton", background=[('active', '#B59530')])

        # Tabs
        style.configure("TNotebook", background=COLOR_BG, borderwidth=0)
        style.configure("TNotebook.Tab", 
                        background="#333333", 
                        foreground=COLOR_FG, 
                        padding=[10, 5], 
                        font=("Times New Roman", 11))
        style.map("TNotebook.Tab", 
                  background=[("selected", COLOR_FG)], 
                  foreground=[("selected", "#000000")])

        # Radio Buttons
        style.configure("TRadiobutton", background=COLOR_BG, foreground=COLOR_FG, indicatorcolor=COLOR_FG)
        style.map("TRadiobutton", indicatorcolor=[('selected', COLOR_FG)])

        # Treeview (The List for the Budget)
        style.configure("Treeview", 
                        background="white", 
                        foreground="black", 
                        fieldbackground="white",
                        font=("Helvetica", 10))
        style.configure("Treeview.Heading", 
                        background=COLOR_FG, 
                        foreground="black", 
                        font=("Times New Roman", 10, "bold"))

        # Create Tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=20, padx=20, expand=True, fill='both')

        # Initialize Frames
        self.create_simple_interest_tab()
        self.create_compound_interest_tab()
        self.create_fv_pv_tab()
        self.create_loan_tab()
        self.create_budget_tab() # <--- NEW TAB

    # --- HELPERS ---
    def get_total_time_in_years(self, y_entry, m_entry, d_entry):
        try:
            years = float(y_entry.get()) if y_entry.get() else 0
            months = float(m_entry.get()) if m_entry.get() else 0
            days = float(d_entry.get()) if d_entry.get() else 0
            if years == 0 and months == 0 and days == 0: return 0
            return years + (months / 12.0) + (days / 365.0)
        except ValueError: return 0

    def save_simple_csv(self, data_dict, filename="result.csv"):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=filename, filetypes=[("CSV files", "*.csv")])
            if not file_path: return
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Parameter", "Value"])
                for key, value in data_dict.items(): writer.writerow([key, value])
                writer.writerow(["Date Calculated", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            messagebox.showinfo("Success", f"Data saved to {file_path}")
        except Exception as e: messagebox.showerror("Error", f"Could not save file: {e}")

    def save_loan_schedule_csv(self, summary_dict, schedule_list, filename="loan_schedule.csv"):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=filename, filetypes=[("CSV files", "*.csv")])
            if not file_path: return
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["--- LOAN SUMMARY ---"])
                for key, value in summary_dict.items(): writer.writerow([key, value])
                writer.writerow([])
                writer.writerow(["--- AMORTIZATION SCHEDULE ---"])
                writer.writerow(["Month", "Start Balance", "Payment", "Principal", "Interest", "End Balance"])
                for row in schedule_list: writer.writerow(row)
            messagebox.showinfo("Success", f"Schedule saved to {file_path}")
        except Exception as e: messagebox.showerror("Error", f"Could not save file: {e}")

    # --- TABS ---

    def create_simple_interest_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Simple Interest")

        ttk.Label(frame, text="Principal Amount ($):", font=FONT_HEADER).grid(row=0, column=0, padx=10, pady=(20, 10), sticky="w")
        p_entry = ttk.Entry(frame); p_entry.grid(row=0, column=1, padx=10, pady=(20, 10))
        ttk.Label(frame, text="Annual Rate (%):", font=FONT_HEADER).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        r_entry = ttk.Entry(frame); r_entry.grid(row=1, column=1, padx=10, pady=10)

        time_frame = ttk.LabelFrame(frame, text=" Duration ")
        time_frame.grid(row=2, column=0, columnspan=2, pady=20, padx=20, sticky="ew")
        y_entry = ttk.Entry(time_frame, width=5); y_entry.pack(side="left", padx=5, pady=10); ttk.Label(time_frame, text="Y").pack(side="left")
        m_entry = ttk.Entry(time_frame, width=5); m_entry.pack(side="left", padx=5, pady=10); ttk.Label(time_frame, text="M").pack(side="left")
        d_entry = ttk.Entry(time_frame, width=5); d_entry.pack(side="left", padx=5, pady=10); ttk.Label(time_frame, text="D").pack(side="left")

        result_label = ttk.Label(frame, text="Result: -", font=FONT_RESULT, foreground="#FFFFFF")
        result_label.grid(row=4, column=0, columnspan=2, pady=30)

        def calculate():
            try:
                P = float(p_entry.get()); R = float(r_entry.get()); T = self.get_total_time_in_years(y_entry, m_entry, d_entry)
                interest = P * (R / 100) * T; total = P + interest
                result_label.config(text=f"Interest: ${interest:,.2f}\nTotal: ${total:,.2f}")
                return {"Type": "Simple Interest", "Principal": P, "Rate (%)": R, "Time (Years)": f"{T:.2f}", "Interest Earned": interest, "Total Amount": total}
            except ValueError: return None

        def on_export():
            data = calculate()
            if data: self.save_simple_csv(data, "simple_interest.csv")

        btn_frame = ttk.Frame(frame); btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Calculate", command=calculate).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Download CSV", command=on_export).pack(side="left", padx=10)

    def create_compound_interest_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Compound Interest")

        ttk.Label(frame, text="Principal Amount ($):", font=FONT_HEADER).grid(row=0, column=0, padx=10, pady=(20,10), sticky="w")
        p_entry = ttk.Entry(frame); p_entry.grid(row=0, column=1, padx=10, pady=(20,10))
        ttk.Label(frame, text="Annual Rate (%):", font=FONT_HEADER).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        r_entry = ttk.Entry(frame); r_entry.grid(row=1, column=1, padx=10, pady=10)
        ttk.Label(frame, text="Compounds / Year:", font=FONT_HEADER).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        n_entry = ttk.Entry(frame); n_entry.insert(0, "12"); n_entry.grid(row=2, column=1, padx=10, pady=10)

        time_frame = ttk.LabelFrame(frame, text=" Duration ")
        time_frame.grid(row=3, column=0, columnspan=2, pady=20, padx=20, sticky="ew")
        y_entry = ttk.Entry(time_frame, width=5); y_entry.pack(side="left", padx=5, pady=10); ttk.Label(time_frame, text="Y").pack(side="left")
        m_entry = ttk.Entry(time_frame, width=5); m_entry.pack(side="left", padx=5, pady=10); ttk.Label(time_frame, text="M").pack(side="left")
        d_entry = ttk.Entry(time_frame, width=5); d_entry.pack(side="left", padx=5, pady=10); ttk.Label(time_frame, text="D").pack(side="left")

        result_label = ttk.Label(frame, text="Result: -", font=FONT_RESULT, foreground="#FFFFFF")
        result_label.grid(row=5, column=0, columnspan=2, pady=30)

        def calculate():
            try:
                P = float(p_entry.get()); R = float(r_entry.get()) / 100; N = float(n_entry.get()); T = self.get_total_time_in_years(y_entry, m_entry, d_entry)
                amount = P * math.pow((1 + (R / N)), (N * T)); interest = amount - P
                result_label.config(text=f"Total: ${amount:,.2f}\nInterest: ${interest:,.2f}")
                return {"Type": "Compound Interest", "Principal": P, "Rate": R*100, "Compounds/Yr": N, "Years": f"{T:.2f}", "Total Amount": amount, "Total Interest": interest}
            except ValueError: return None

        def on_export():
            data = calculate()
            if data: self.save_simple_csv(data, "compound_interest.csv")

        btn_frame = ttk.Frame(frame); btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Calculate", command=calculate).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Download CSV", command=on_export).pack(side="left", padx=10)

    def create_fv_pv_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="FV / PV")

        mode_var = tk.StringVar(value="FV")
        rb_frame = ttk.Frame(frame); rb_frame.grid(row=0, column=0, columnspan=2, pady=20)
        ttk.Radiobutton(rb_frame, text="Future Value (FV)", variable=mode_var, value="FV").pack(side="left", padx=10)
        ttk.Radiobutton(rb_frame, text="Present Value (PV)", variable=mode_var, value="PV").pack(side="left", padx=10)

        ttk.Label(frame, text="Amount ($):", font=FONT_HEADER).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        amt_entry = ttk.Entry(frame); amt_entry.grid(row=2, column=1, padx=10, pady=10)
        ttk.Label(frame, text="Annual Rate (%):", font=FONT_HEADER).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        r_entry = ttk.Entry(frame); r_entry.grid(row=3, column=1, padx=10, pady=10)

        time_frame = ttk.LabelFrame(frame, text=" Duration ")
        time_frame.grid(row=4, column=0, columnspan=2, pady=20, padx=20, sticky="ew")
        y_entry = ttk.Entry(time_frame, width=5); y_entry.pack(side="left", padx=5, pady=10); ttk.Label(time_frame, text="Y").pack(side="left")
        m_entry = ttk.Entry(time_frame, width=5); m_entry.pack(side="left", padx=5, pady=10); ttk.Label(time_frame, text="M").pack(side="left")
        d_entry = ttk.Entry(time_frame, width=5); d_entry.pack(side="left", padx=5, pady=10); ttk.Label(time_frame, text="D").pack(side="left")

        result_label = ttk.Label(frame, text="Result: -", font=FONT_RESULT, foreground="#FFFFFF")
        result_label.grid(row=6, column=0, columnspan=2, pady=30)

        def calculate():
            try:
                amt = float(amt_entry.get()); r = float(r_entry.get()) / 100; t = self.get_total_time_in_years(y_entry, m_entry, d_entry)
                mode = mode_var.get()
                if mode == "FV": res = amt * math.pow((1 + r), t); txt = f"Future Value: ${res:,.2f}"
                else: res = amt / math.pow((1 + r), t); txt = f"Present Value: ${res:,.2f}"
                result_label.config(text=txt)
                return {"Type": f"{mode} Calculation", "Input Amount": amt, "Rate": r*100, "Years": f"{t:.2f}", "Result": res}
            except ValueError: return None

        def on_export():
            data = calculate()
            if data: self.save_simple_csv(data, "fv_pv_result.csv")

        btn_frame = ttk.Frame(frame); btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Calculate", command=calculate).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Download CSV", command=on_export).pack(side="left", padx=10)

    def create_loan_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Loan / Annuity")

        ttk.Label(frame, text="Loan Amount ($):", font=FONT_HEADER).grid(row=0, column=0, padx=10, pady=(20,10), sticky="w")
        p_entry = ttk.Entry(frame); p_entry.grid(row=0, column=1, padx=10, pady=(20,10))
        ttk.Label(frame, text="Annual Rate (%):", font=FONT_HEADER).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        r_entry = ttk.Entry(frame); r_entry.grid(row=1, column=1, padx=10, pady=10)

        time_frame = ttk.LabelFrame(frame, text=" Term Duration ")
        time_frame.grid(row=2, column=0, columnspan=2, pady=20, padx=20, sticky="ew")
        y_entry = ttk.Entry(time_frame, width=5); y_entry.pack(side="left", padx=5, pady=10); ttk.Label(time_frame, text="Y").pack(side="left")
        m_entry = ttk.Entry(time_frame, width=5); m_entry.pack(side="left", padx=5, pady=10); ttk.Label(time_frame, text="M").pack(side="left")
        d_entry = ttk.Entry(time_frame, width=5); d_entry.pack(side="left", padx=5, pady=10); ttk.Label(time_frame, text="D").pack(side="left")

        result_label = ttk.Label(frame, text="Result: -", font=FONT_RESULT, foreground="#FFFFFF")
        result_label.grid(row=4, column=0, columnspan=2, pady=30)

        self.loan_summary = {}; self.loan_schedule = []

        def calculate():
            try:
                P = float(p_entry.get()); annual_rate = float(r_entry.get()) / 100; years = self.get_total_time_in_years(y_entry, m_entry, d_entry)
                if years == 0: return
                r_monthly = annual_rate / 12; n_months = int(years * 12)
                if r_monthly == 0: pmt = P / n_months
                else: pmt = (P * r_monthly * math.pow((1 + r_monthly), n_months)) / (math.pow((1 + r_monthly), n_months) - 1)
                
                total_paid = pmt * n_months; total_interest = total_paid - P
                result_label.config(text=f"Monthly Payment: ${pmt:,.2f}\nTotal Interest: ${total_interest:,.2f}\nTotal Cost: ${total_paid:,.2f}")

                schedule = []; balance = P
                for i in range(1, n_months + 1):
                    interest_payment = balance * r_monthly; principal_payment = pmt - interest_payment; start_balance = balance; balance -= principal_payment
                    schedule.append([i, f"{start_balance:.2f}", f"{pmt:.2f}", f"{principal_payment:.2f}", f"{interest_payment:.2f}", f"{abs(balance):.2f}"])

                self.loan_summary = {"Loan Amount": P, "Rate": f"{annual_rate*100}%", "Months": n_months, "PMT": f"{pmt:.2f}", "Total Interest": f"{total_interest:.2f}", "Total Cost": f"{total_paid:.2f}"}
                self.loan_schedule = schedule
            except ValueError: messagebox.showerror("Error", "Invalid Input")

        def on_export():
            calculate()
            if self.loan_summary: self.save_loan_schedule_csv(self.loan_summary, self.loan_schedule)
            else: messagebox.showwarning("Warning", "Calculate first.")

        btn_frame = ttk.Frame(frame); btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Calculate", command=calculate).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Download Schedule", command=on_export).pack(side="left", padx=10)

    # ===========================
    # 5. NEW BUDGET TAB
    # ===========================
    def create_budget_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Budget Manager")

        # Top Section: Input
        input_frame = ttk.LabelFrame(frame, text=" Add Item ")
        input_frame.pack(pady=10, padx=20, fill="x")

        ttk.Label(input_frame, text="Description:").grid(row=0, column=0, padx=5, pady=5)
        desc_entry = ttk.Entry(input_frame, width=20)
        desc_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Amount ($):").grid(row=0, column=2, padx=5, pady=5)
        amt_entry = ttk.Entry(input_frame, width=10)
        amt_entry.grid(row=0, column=3, padx=5, pady=5)

        type_var = tk.StringVar(value="Expense")
        ttk.Radiobutton(input_frame, text="Expense", variable=type_var, value="Expense").grid(row=0, column=4, padx=5)
        ttk.Radiobutton(input_frame, text="Income", variable=type_var, value="Income").grid(row=0, column=5, padx=5)

        # Middle Section: The List (Treeview)
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(pady=10, padx=20, expand=True, fill="both")

        columns = ("Type", "Description", "Amount")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        tree.heading("Type", text="Type")
        tree.heading("Description", text="Description")
        tree.heading("Amount", text="Amount")
        
        # Column formatting
        tree.column("Type", width=80, anchor="center")
        tree.column("Description", width=200, anchor="w")
        tree.column("Amount", width=100, anchor="e")
        tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)

        # Bottom Section: Totals
        summary_frame = ttk.Frame(frame)
        summary_frame.pack(pady=10, padx=20, fill="x")

        total_income_lbl = ttk.Label(summary_frame, text="Income: $0.00", font=("Times New Roman", 12))
        total_income_lbl.pack(side="left", padx=10)
        
        total_expense_lbl = ttk.Label(summary_frame, text="Expenses: $0.00", font=("Times New Roman", 12))
        total_expense_lbl.pack(side="left", padx=10)
        
        net_lbl = ttk.Label(summary_frame, text="Net: $0.00", font=("Times New Roman", 12, "bold"), foreground="white")
        net_lbl.pack(side="right", padx=10)

        # Data Storage
        self.budget_items = []

        def update_totals():
            income = sum(item['amount'] for item in self.budget_items if item['type'] == "Income")
            expenses = sum(item['amount'] for item in self.budget_items if item['type'] == "Expense")
            net = income - expenses
            
            total_income_lbl.config(text=f"Income: ${income:,.2f}")
            total_expense_lbl.config(text=f"Expenses: ${expenses:,.2f}")
            net_lbl.config(text=f"Net Balance: ${net:,.2f}")

            # Color coding the net balance
            if net >= 0: net_lbl.configure(foreground="#00FF00") # Green for positive
            else: net_lbl.configure(foreground="#FF0000")       # Red for negative

        def add_item():
            try:
                desc = desc_entry.get()
                amt = float(amt_entry.get())
                t = type_var.get()
                
                if not desc:
                    messagebox.showwarning("Input", "Please enter a description.")
                    return

                self.budget_items.append({"type": t, "desc": desc, "amount": amt})
                tree.insert("", "end", values=(t, desc, f"${amt:,.2f}"))
                
                # Clear inputs
                desc_entry.delete(0, tk.END)
                amt_entry.delete(0, tk.END)
                update_totals()
            except ValueError:
                messagebox.showerror("Error", "Amount must be a number.")

        def export_budget():
            if not self.budget_items:
                messagebox.showwarning("Warning", "No items to export.")
                return
            
            try:
                file_path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile="budget.csv", filetypes=[("CSV files", "*.csv")])
                if not file_path: return
                
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Type", "Description", "Amount"])
                    for item in self.budget_items:
                        writer.writerow([item['type'], item['desc'], item['amount']])
                    
                    # Write Totals at the bottom
                    income = sum(item['amount'] for item in self.budget_items if item['type'] == "Income")
                    expenses = sum(item['amount'] for item in self.budget_items if item['type'] == "Expense")
                    writer.writerow([])
                    writer.writerow(["SUMMARY", "", ""])
                    writer.writerow(["Total Income", "", income])
                    writer.writerow(["Total Expenses", "", expenses])
                    writer.writerow(["Net Balance", "", income - expenses])
                
                messagebox.showinfo("Success", f"Budget saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")

        # Buttons
        ttk.Button(input_frame, text="Add", command=add_item).grid(row=0, column=6, padx=10)
        
        # Export Button at bottom
        ttk.Button(frame, text="Download Budget (CSV)", command=export_budget).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
