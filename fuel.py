import tkinter as tk
from tkinter import ttk, messagebox
import threading
import re
import requests

try:
    from ttkthemes import ThemedTk
    HAS_THEMES = True
except ImportError:
    HAS_THEMES = False

# --- CONSTANTS ---
MPG_TO_L100KM = 235.215
BUDI_RATE = 1.99
KM_TO_MILES = 1.60934
L_TO_GALLONS = 0.264172
FALLBACK_PRICE = "2.60"
SCRAPE_URL = (
    "https://ringgitplus.com/en/blog/petrol-credit-card/"
    "petrol-price-malaysia-live-updates-ron95-ron97-diesel.html"
)

# --- API FETCHING ---
def fetch_fuel_price() -> str:
    """Fetch live RON95 price. Returns fallback string on any failure."""
    try:
        response = requests.get(SCRAPE_URL, timeout=5)
        response.raise_for_status()
        match = re.search(r"RON95\s*:\s*RM\s*(\d+\.\d{2})", response.text)
        if match:
            return match.group(1)
        print("[WARN] Could not parse RON95 price from page, using fallback.")
    except requests.RequestException as e:
        print(f"[WARN] Fuel price fetch failed: {e}")
    return FALLBACK_PRICE


def load_price_async():
    """Fetch fuel price in background, then update UI safely."""
    price = fetch_fuel_price()
    root.after(0, lambda: app.update_fuel_price(price))


# --- APP CLASS ---
class FuelCalcApp:
    INPUTS = [
        ("Current Market Rate (RM/L):", "market_price"),
        ("Distance Driven (KM):", "km"),
        ("Pump Meter Shows (RM):", "pump_display_rm"),
        ("Manual Liters (L):", "liters"),
        ("OR Input MPG:", "mpg"),
    ]
    OUTPUT_KEYS = ["liters", "paid", "market", "savings", "rm_km", "km_l", "l_100km", "mpg"]

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("BUDI95 Trip & MPG Calculator")
        self.root.protocol("WM_DELETE_WINDOW", root.destroy)
        self.root.resizable(False, False)

        self.fuel_price: str = FALLBACK_PRICE
        self.subsidized_var = tk.BooleanVar(value=False)
        self.results: dict[str, tk.StringVar] = {k: tk.StringVar() for k in self.OUTPUT_KEYS}
        self.entries: dict[str, ttk.Entry] = {}

        self._build_ui()

    # --- UI BUILDING ---
    def _build_ui(self):
        main = ttk.Frame(self.root, padding="15")
        main.grid(row=0, column=0, sticky="NSEW")

        # Live rate header (placeholder until async fetch completes)
        self.header_label = ttk.Label(
            main,
            text=f"Fetching live RON95 rate...",
            foreground="#d32f2f",
            font=("Roboto", 10, "bold"),
        )
        self.header_label.grid(row=0, columnspan=2, pady=5)

        # Input fields
        for i, (label, key) in enumerate(self.INPUTS, start=1):
            ttk.Label(main, text=label).grid(row=i, column=0, sticky="E", padx=5, pady=2)
            entry = ttk.Entry(main, width=15)
            entry.grid(row=i, column=1, sticky="W", padx=5)
            self.entries[key] = entry

        self.entries["market_price"].insert(0, self.fuel_price)

        # Subsidy checkbox
        ttk.Checkbutton(
            main,
            text="Eligible for BUDI95 (RM1.99 rate)",
            variable=self.subsidized_var,
        ).grid(row=6, columnspan=2, pady=10)

        # Calculate button
        ttk.Button(main, text="Calculate Efficiency", command=self.calculate).grid(
            row=7, columnspan=2, pady=10
        )

        # Result labels
        row_idx = 8
        for key in self.OUTPUT_KEYS:
            is_important = key in ("paid", "rm_km")
            lbl = ttk.Label(
                main,
                textvariable=self.results[key],
                font=("Roboto", 13 if is_important else 10, "bold" if is_important else "normal"),
                foreground="#2e7d32" if key == "paid" else "black",
            )
            lbl.grid(row=row_idx, columnspan=2, pady=2)
            row_idx += 1

        # Control buttons
        btn_frame = ttk.Frame(main)
        btn_frame.grid(row=row_idx, columnspan=2, pady=15)
        ttk.Button(btn_frame, text="Reset", command=self.reset).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Quit", command=self.root.destroy).pack(side="left", padx=5)

    # --- HELPERS ---
    def update_fuel_price(self, price: str):
        """Called from async thread to safely update UI with fetched price."""
        self.fuel_price = price
        self.header_label.config(text=f"Live RON95 Market Rate: RM{price}")
        self.entries["market_price"].delete(0, "end")
        self.entries["market_price"].insert(0, price)

    def _get_float(self, key: str) -> float | None:
        """Return float value of an entry or None if empty/invalid."""
        raw = self.entries[key].get().strip()
        if not raw:
            return None
        try:
            return float(raw)
        except ValueError:
            return None

    def _highlight_error(self, key: str):
        """Flash an entry red to indicate bad input."""
        entry = self.entries[key]
        entry.config(foreground="red")
        self.root.after(1500, lambda: entry.config(foreground="black"))

    # --- LOGIC ---
    def reset(self):
        for entry in self.entries.values():
            entry.delete(0, "end")
        self.entries["market_price"].insert(0, self.fuel_price)
        self.subsidized_var.set(False)
        for var in self.results.values():
            var.set("")

    def calculate(self):
        vals = {k: self._get_float(k) for k in self.entries}
        market_rate = vals["market_price"]

        if market_rate is None or market_rate <= 0:
            self._highlight_error("market_price")
            messagebox.showerror("Error", "Market price is required and must be a positive number.")
            return

        mpg = vals["mpg"]
        liters: float
        km: float

        # --- Priority 1: MPG input ---
        if mpg:
            if mpg <= 0:
                self._highlight_error("mpg")
                messagebox.showerror("Error", "MPG must be a positive number.")
                return
            l_100km = MPG_TO_L100KM / mpg
            liters = l_100km
            km = 100.0

        # --- Priority 2: Distance + liters/pump display ---
        else:
            km = vals["km"]
            if not km or km <= 0:
                self._highlight_error("km")
                messagebox.showerror("Error", "Distance (KM) is required when not using MPG input.")
                return

            pump_rm = vals["pump_display_rm"]
            manual_liters = vals["liters"]

            if manual_liters and manual_liters > 0:
                liters = manual_liters
            elif pump_rm and pump_rm > 0:
                liters = pump_rm / market_rate
            else:
                messagebox.showerror(
                    "Error", "Provide Liters, Pump Display (RM), or MPG to calculate."
                )
                return

        if liters <= 0:
            messagebox.showerror("Error", "Liters must be greater than zero.")
            return

        pump_market_value = liters * market_rate

        # --- Subsidy logic ---
        if self.subsidized_var.get():
            actual_paid = liters * BUDI_RATE
            savings = pump_market_value - actual_paid
        else:
            actual_paid = pump_market_value
            savings = 0.0

        # --- Derived metrics ---
        try:
            cost_per_km = actual_paid / km
            km_per_l = km / liters
            l_per_100km = (100 * liters) / km
            mpg_display = mpg if mpg else (km / KM_TO_MILES) / (liters * L_TO_GALLONS)
        except ZeroDivisionError:
            messagebox.showerror("Error", "Division by zero — check your inputs.")
            return

        # --- Update result labels ---
        updates = {
            "liters": f"Liters: {liters:.3f} L",
            "paid": f"Actual Paid: RM {actual_paid:.2f}",
            "market": f"Pump Value: RM {pump_market_value:.2f}",
            "savings": f"Total Savings: RM {savings:.2f}" if self.subsidized_var.get() else "",
            "rm_km": f"Cost: RM {cost_per_km:.2f} / km",
            "km_l": f"Efficiency: {km_per_l:.2f} km/L",
            "l_100km": f"L/100 km: {l_per_100km:.2f}",
            "mpg": f"MPG: {mpg_display:.2f}",
        }
        for key, value in updates.items():
            self.results[key].set(value)


# --- ENTRY POINT ---
if __name__ == "__main__":
    if HAS_THEMES:
        root = ThemedTk(theme="arc")
    else:
        root = tk.Tk()

    app = FuelCalcApp(root)

    # Fetch live price without blocking the UI
    threading.Thread(target=load_price_async, daemon=True).start()

    root.mainloop()
