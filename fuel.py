import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
import re
import requests
from datetime import date

# --- API FETCHING ---
def fetch_fuel_price():
    fallback = "2.05" 
    try:
        url = "https://ringgitplus.com/en/blog/petrol-credit-card/petrol-price-malaysia-live-updates-ron95-ron97-diesel.html"
        response = requests.get(url, timeout=5)
        match = re.search(r"RON95 : RM(\d+\.\d+) per litre", response.text)
        return match.group(1) if match else fallback
    except:
        return fallback

fuel_price_api = fetch_fuel_price()

# --- LOGIC ---
def reset():
    for entry in entries.values():
        entry.delete(0, 'end')
    entries['market_price'].insert(0, fuel_price_api)
    subsidized_var.set(False)
    for var in results.values():
        var.set("")

def calculate_efficiency():
    try:
        vals = {k: (float(e.get()) if e.get() else None) for k, e in entries.items()}
        market_rate = vals['market_price'] or float(fuel_price_api)
        budi_rate = 1.99
        
        # Priority 1: MPG Input
        if vals['mpg']:
            mpg = vals['mpg']
            # Convert MPG to L/100km: 235.215 / MPG
            l_100km = 235.215 / mpg
            liters = l_100km
            km = 100.0
            pump_market_value = liters * market_rate
        # Priority 2: Pump Display / Manual Liters
        else:
            km = vals['km'] or 1.0
            pump_market_value = vals['pump_display_rm']
            liters = vals['liters'] or (pump_market_value / market_rate if pump_market_value else 0)
            pump_market_value = liters * market_rate

        # Apply Subsidy Logic
        if subsidized_var.get():
            actual_paid = liters * budi_rate
            savings = pump_market_value - actual_paid
        else:
            actual_paid = pump_market_value
            savings = 0

        # Efficiency Math
        res = {
            'liters': f"Liters: {liters:.3f} L",
            'paid': f"Actual Paid: RM {actual_paid:.2f}",
            'market': f"Pump Value: RM {pump_market_value:.2f}",
            'savings': f"Total Savings: RM {savings:.2f}" if subsidized_var.get() else "",
            'rm_km': f"Cost: RM {actual_paid / km:.2f} / km",
            'km_l': f"Efficiency: {km / liters:.2f} km/L",
            'l_100km': f"L/100 km: {(100 * liters) / km:.2f}",
            'mpg': f"MPG: {vals['mpg'] if vals['mpg'] else (km / 1.60934) / (liters * 0.264172):.2f}"
        }

        for key, value in res.items():
            results[key].set(value)

    except (ValueError, TypeError, ZeroDivisionError):
        messagebox.showerror("Error", "Check your inputs. Ensure Market Price and at least one metric is filled.")

# --- UI SETUP ---
root = ThemedTk(theme="arc")
root.title("BUDI95 Trip & MPG Calculator")
root.protocol("WM_DELETE_WINDOW", root.destroy)

main = ttk.Frame(root, padding="15")
main.grid(row=0, column=0, sticky="NSEW")

INPUTS = [
    ("Current Market Rate (RM/L):", "market_price"),
    ("Distance Driven (KM):", "km"),
    ("Pump Meter Shows (RM):", "pump_display_rm"),
    ("Manual Liters (L):", "liters"),
    ("OR Input MPG:", "mpg")
]

OUTPUT_KEYS = ['liters', 'paid', 'market', 'savings', 'rm_km', 'km_l', 'l_100km', 'mpg']
results = {k: tk.StringVar() for k in OUTPUT_KEYS}
entries = {}

# Header
ttk.Label(main, text=f"Live RON95 Market Rate: RM{fuel_price_api}", foreground="#d32f2f", font=("Roboto", 10, "bold")).grid(row=0, columnspan=2, pady=5)

for i, (label, key) in enumerate(INPUTS, start=1):
    ttk.Label(main, text=label).grid(row=i, column=0, sticky="E", padx=5, pady=2)
    entries[key] = ttk.Entry(main, width=15)
    entries[key].grid(row=i, column=1, sticky="W", padx=5)

entries['market_price'].insert(0, fuel_price_api)

subsidized_var = tk.BooleanVar(value=False)
ttk.Checkbutton(main, text="Eligible for BUDI95 (RM1.99 rate)", variable=subsidized_var).grid(row=6, columnspan=2, pady=10)

ttk.Button(main, text="Calculate Efficiency", command=calculate_efficiency).grid(row=7, columnspan=2, pady=10)

# Build Result Labels
row_idx = 8
for key in OUTPUT_KEYS:
    is_important = key in ['paid', 'rm_km']
    lbl = ttk.Label(main, textvariable=results[key], 
                    font=("Roboto", 13 if is_important else 10, "bold" if is_important else "normal"),
                    foreground="#2e7d32" if key == 'paid' else "black")
    lbl.grid(row=row_idx, columnspan=2, pady=2)
    row_idx += 1

# Controls
btn_frame = ttk.Frame(main)
btn_frame.grid(row=row_idx, columnspan=2, pady=15)
ttk.Button(btn_frame, text="Reset", command=reset).pack(side="left", padx=5)
ttk.Button(btn_frame, text="Quit", command=root.destroy).pack(side="left", padx=5)

root.mainloop()
