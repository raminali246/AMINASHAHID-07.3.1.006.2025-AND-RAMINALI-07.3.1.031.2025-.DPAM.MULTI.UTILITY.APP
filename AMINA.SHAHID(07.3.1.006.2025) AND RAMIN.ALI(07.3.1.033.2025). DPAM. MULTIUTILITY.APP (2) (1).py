import tkinter as tk
from tkinter import ttk, messagebox
import math
import re

class MultiUtilitySuite:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Utility Suite")
        self.root.geometry("450x600")
        
        # Create Tabbed Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')
        
        # Create Frames for each Tab
        self.calc_frame = tk.Frame(self.notebook, bg="#87CEFA")
        self.temp_frame = tk.Frame(self.notebook)
        self.unit_frame = tk.Frame(self.notebook, bg="#dbeafe")
        self.phys_frame = tk.Frame(self.notebook)
        
        # Add frames to notebook
        self.notebook.add(self.calc_frame, text="Calculator")
        self.notebook.add(self.temp_frame, text="Temperature")
        self.notebook.add(self.unit_frame, text="Units")
        self.notebook.add(self.phys_frame, text="Physics Solver")
        
        # Initialize Tabs
        self.setup_calculator()
        self.setup_temperature()
        self.setup_units()
        self.setup_physics()

    # ----------------- 1. CALCULATOR -----------------
    def setup_calculator(self):
        self.calc_expr = ""
        self.angle_mode = "DEG"
        self.calc_var = tk.StringVar()
        
        entry = tk.Entry(self.calc_frame, textvariable=self.calc_var, font=('Arial', 20),
                         bd=10, insertwidth=2, width=16, borderwidth=4)
        entry.grid(row=0, column=0, columnspan=5, pady=10)
        
        self.mode_label = tk.Label(self.calc_frame, text=self.angle_mode, bg="#87CEFA", font=("Arial", 12))
        self.mode_label.grid(row=1, column=4)
        
        buttons = [
            ('C', 2, 0), ('⌫', 2, 1), ('%', 2, 2), ('^', 2, 3), 
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('÷', 3, 3), ('sin(', 3, 4),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('×', 4, 3), ('cos(', 4, 4),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('-', 5, 3), ('tan(', 5, 4),
            ('0', 6, 0), ('.', 6, 1), ('(', 6, 2), (')', 6, 3), ('+', 6, 4),
            ('x²', 7, 0), ('!', 7, 1), ('Mode', 7, 2), ('=', 7, 3)
        ]
        
        for btn in buttons:
            text, r, c = btn
            colspan = 2 if text == '=' else 1
            cmd = lambda t=text: self.calc_press(t)
            
            if text == 'C': cmd = self.calc_clear
            elif text == '⌫': cmd = self.calc_backspace
            elif text == 'Mode': cmd = self.calc_toggle_mode
            elif text == '=': cmd = self.calc_evaluate
            
            tk.Button(self.calc_frame, text=text, padx=10, pady=15, font=("Arial", 12),
                      command=cmd).grid(row=r, column=c, columnspan=colspan, sticky="nsew", padx=2, pady=2)
                      
        for i in range(8): self.calc_frame.grid_rowconfigure(i, weight=1)
        for i in range(5): self.calc_frame.grid_columnconfigure(i, weight=1)

    def calc_press(self, value):
        if value == 'x²': value = '**2'
        self.calc_expr += str(value)
        self.calc_var.set(self.calc_expr)

    def calc_clear(self):
        self.calc_expr = ""
        self.calc_var.set("")

    def calc_backspace(self):
        self.calc_expr = self.calc_expr[:-1]
        self.calc_var.set(self.calc_expr)

    def calc_toggle_mode(self):
        self.angle_mode = "RAD" if self.angle_mode == "DEG" else "DEG"
        self.mode_label.config(text=self.angle_mode)

    def calc_evaluate(self):
        try:
            expr = self.calc_expr.replace("^", "**").replace("×", "*").replace("÷", "/")
            while "!" in expr:
                expr = re.sub(r'(\d+|\([^()]*\))!', r'math.factorial(\1)', expr)
            
            def safe_sin(x): return math.sin(math.radians(x)) if self.angle_mode == "DEG" else math.sin(x)
            def safe_cos(x): return math.cos(math.radians(x)) if self.angle_mode == "DEG" else math.cos(x)
            def safe_tan(x): return math.tan(math.radians(x)) if self.angle_mode == "DEG" else math.tan(x)
            
            result = eval(expr, {"__builtins__": None}, 
                          {"math": math, "sin": safe_sin, "cos": safe_cos, "tan": safe_tan})
            
            self.calc_var.set(result)
            self.calc_expr = str(result)
        except Exception:
            self.calc_var.set("Error")
            self.calc_expr = ""

    # ----------------- 2. TEMPERATURE CONVERTER -----------------
    def setup_temperature(self):
        tk.Label(self.temp_frame, text="Temperature Converter", font=("Arial", 16, "bold")).pack(pady=20)
        
        self.temp_entry = tk.Entry(self.temp_frame, font=("Arial", 14), justify="center")
        self.temp_entry.pack(pady=10)
        
        frame = tk.Frame(self.temp_frame)
        frame.pack(pady=10)
        
        units = ["Celsius", "Fahrenheit", "Kelvin"]
        self.temp_from = ttk.Combobox(frame, values=units, state="readonly", width=12)
        self.temp_from.set("Celsius")
        self.temp_from.grid(row=0, column=0, padx=10)
        
        tk.Label(frame, text="to").grid(row=0, column=1)
        
        self.temp_to = ttk.Combobox(frame, values=units, state="readonly", width=12)
        self.temp_to.set("Fahrenheit")
        self.temp_to.grid(row=0, column=2, padx=10)
        
        tk.Button(self.temp_frame, text="Convert", command=self.convert_temp, font=("Arial", 12)).pack(pady=20)
        self.temp_result = tk.Label(self.temp_frame, text="Result: ", font=("Arial", 14, "bold"))
        self.temp_result.pack(pady=10)

    def convert_temp(self):
        try:
            val = float(self.temp_entry.get())
            f_unit = self.temp_from.get()
            t_unit = self.temp_to.get()

            # Convert input to Kelvin to validate against absolute zero (0 K)
            if f_unit == "Kelvin":
                kelvin_val = val
            elif f_unit == "Celsius":
                kelvin_val = val + 273.15
            elif f_unit == "Fahrenheit":
                kelvin_val = (val - 32) * 5/9 + 273.15

            if kelvin_val < 0:
                messagebox.showerror(
                    "Invalid Temperature",
                    "Temperature is below absolute zero (0 K / -273.15 °C / -459.67 °F).\n"
                    "Such a temperature is physically impossible."
                )
                return

            if f_unit == t_unit: res = val
            elif f_unit == "Celsius": res = (val * 9/5) + 32 if t_unit == "Fahrenheit" else val + 273.15
            elif f_unit == "Fahrenheit": res = (val - 32) * 5/9 if t_unit == "Celsius" else (val - 32) * 5/9 + 273.15
            elif f_unit == "Kelvin": res = val - 273.15 if t_unit == "Celsius" else (val - 273.15) * 9/5 + 32
            
            self.temp_result.config(text=f"Result: {round(res, 2)} {t_unit}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")

    # ----------------- 3. UNIT CONVERTER -----------------
    def setup_units(self):
        self.conversions = {
            "Length": {"m": 1, "km": 1000, "cm": 0.01, "mm": 0.001},
            "Mass": {"kg": 1, "g": 0.001, "lb": 0.453592},
            "Time": {"s": 1, "min": 60, "hr": 3600},
            "Speed": {"m/s": 1, "km/h": 0.277778, "mph": 0.44704},
            "Acceleration": {"m/s²": 1, "ft/s²": 0.3048}
        }
        
        tk.Label(self.unit_frame, text="Category", bg="#dbeafe", font=("Arial", 12)).pack(pady=5)
        self.unit_category = ttk.Combobox(self.unit_frame, values=list(self.conversions.keys()), state="readonly")
        self.unit_category.pack()
        self.unit_category.bind("<<ComboboxSelected>>", self.update_unit_dropdowns)
        
        tk.Label(self.unit_frame, text="Enter Value", bg="#dbeafe", font=("Arial", 12)).pack(pady=5)
        self.unit_entry = tk.Entry(self.unit_frame, font=("Arial", 12))
        self.unit_entry.pack()
        
        self.unit_from = ttk.Combobox(self.unit_frame, state="readonly")
        self.unit_from.pack(pady=5)
        
        self.unit_to = ttk.Combobox(self.unit_frame, state="readonly")
        self.unit_to.pack(pady=5)
        
        btn_frame = tk.Frame(self.unit_frame, bg="#dbeafe")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Convert", command=self.convert_unit, width=10).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Clear", command=lambda: self.unit_entry.delete(0, tk.END), width=10).grid(row=0, column=1, padx=5)
        
        self.unit_result = tk.Label(self.unit_frame, text="Result: ", bg="#dbeafe", font=("Arial", 14, "bold"))
        self.unit_result.pack(pady=10)
        
        self.unit_category.current(0)
        self.update_unit_dropdowns()

    def update_unit_dropdowns(self, event=None):
        units = list(self.conversions[self.unit_category.get()].keys())
        self.unit_from['values'] = units
        self.unit_to['values'] = units
        self.unit_from.current(0)
        self.unit_to.current(1 if len(units) > 1 else 0)

    def convert_unit(self):
        try:
            cat = self.unit_category.get()
            val = float(self.unit_entry.get())
            f_u, t_u = self.unit_from.get(), self.unit_to.get()

            # Time and Mass cannot be negative
            if cat in ("Time", "Mass") and val < 0:
                self.unit_result.config(text=f"Result: Error — {cat} cannot be negative")
                return

            base_val = val * self.conversions[cat][f_u]
            res = base_val / self.conversions[cat][t_u]
            self.unit_result.config(text=f"Result: {res:.4f}")
        except ValueError:
            self.unit_result.config(text="Result: Error")

    # ----------------- 4. PHYSICS SOLVER -----------------
    def setup_physics(self):
        self.phys_formulas = {
            "Final Velocity (v = u + at)": ("v0", "a", "t"),
            "Displacement (s = ut + ½at²)": ("v0", "a", "t"),
            "Velocity from v²": ("v0", "a", "s"),
            "Force (F = ma)": ("m", "a"),
            "Kinetic Energy (KE = ½mv²)": ("m", "v"),
            "Work Done (W = Fd cosθ)": ("F", "d", "θ")
        }

        # Parameters that must be non-negative (physically constrained)
        self.phys_non_negative = {"t", "m"}
        
        ttk.Label(self.phys_frame, text="Select Formula", font=("Arial", 12)).pack(pady=10)
        self.phys_combo = ttk.Combobox(self.phys_frame, values=list(self.phys_formulas.keys()), state="readonly", width=30)
        self.phys_combo.pack()
        self.phys_combo.bind("<<ComboboxSelected>>", self.update_phys_fields)
        
        self.phys_labels = []
        self.phys_entries = []
        
        for _ in range(3):
            lbl = ttk.Label(self.phys_frame, text="")
            lbl.pack(pady=(10, 0))
            self.phys_labels.append(lbl)
            
            entry = ttk.Entry(self.phys_frame)
            entry.pack()
            self.phys_entries.append(entry)
            
        tk.Button(self.phys_frame, text="Calculate", command=self.calc_physics, font=("Arial", 12)).pack(pady=20)
        self.phys_combo.current(0)
        self.update_phys_fields()

    def update_phys_fields(self, event=None):
        params = self.phys_formulas[self.phys_combo.get()]
        for i in range(3):
            if i < len(params):
                self.phys_labels[i].config(text=f"Enter {params[i]}:")
                self.phys_entries[i].config(state="normal")
            else:
                self.phys_labels[i].config(text="")
                self.phys_entries[i].delete(0, tk.END)
                self.phys_entries[i].config(state="disabled")

    def calc_physics(self):
        try:
            form = self.phys_combo.get()
            params = self.phys_formulas[form]
            vals = [float(self.phys_entries[i].get()) for i in range(len(params))]

            # Validate non-negative physical quantities
            for i, param in enumerate(params):
                if param in self.phys_non_negative and vals[i] < 0:
                    messagebox.showerror(
                        "Invalid Input",
                        f"'{param}' cannot be negative — it represents a physical quantity "
                        f"that must be zero or positive."
                    )
                    return

            # Mass must be positive (not just non-negative)
            if "m" in params:
                m_idx = params.index("m")
                if vals[m_idx] <= 0:
                    messagebox.showerror("Invalid Input", "Mass must be a positive value.")
                    return

            if "Final Velocity" in form: res = vals[0] + vals[1] * vals[2]
            elif "Displacement" in form: res = vals[0] * vals[2] + 0.5 * vals[1] * vals[2]**2
            elif "Velocity from v²" in form: 
                v2 = vals[0]**2 + 2 * vals[1] * vals[2]
                if v2 < 0: raise ValueError("Negative v²")
                res = math.sqrt(v2)
            elif "Force" in form: res = vals[0] * vals[1]
            elif "Kinetic Energy" in form: res = 0.5 * vals[0] * vals[1]**2
            elif "Work Done" in form: res = vals[0] * vals[1] * math.cos(math.radians(vals[2]))
            
            messagebox.showinfo("Physics Result", f"Result: {res:.3f}")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")

# ----------------- RUN APP -----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MultiUtilitySuite(root)
    root.mainloop()