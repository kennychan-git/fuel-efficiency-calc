import tkinter as tk
from tkinter import ttk, messagebox
import threading
import requests

try:
    from ttkthemes import ThemedTk
    HAS_THEMES = True
except ImportError:
    HAS_THEMES = False


# --- CONSTANTS ---
MPG_TO_L100KM = 235.215
FALLBACK_BUDI_RATE = 1.99
KM_TO_MILES = 1.60934
L_TO_GALLONS = 0.264172
FALLBACK_PRICE_95 = "3.27"
FALLBACK_PRICE_97 = "4.55"
FALLBACK_PRICE_DIESEL = "4.72"
FALLBACK_PRICE_DIESEL_EM = "2.15"
FALLBACK_BUDI_RATE = 1.99
# Returns the single most recent weekly record, sorted descending by date
API_URL = "https://api.data.gov.my/data-catalogue?id=fuelprice&limit=1&sort=-date"


# --- PRICE FETCHING ---
def fetch_fuel_prices() -> tuple[str, str, str, str, float]:
    """Fetch latest RON95, RON97, diesel prices and BUDI95 rate from data.gov.my.
    Returns fallback values on any failure."""
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()

        if not data:
            print("[WARN] data.gov.my returned empty response, using fallback.")
            return (FALLBACK_PRICE_95, FALLBACK_PRICE_97, FALLBACK_PRICE_DIESEL, FALLBACK_PRICE_DIESEL_EM, FALLBACK_BUDI_RATE)

        latest = data[0]
        price95 = f"{latest['ron95']:.2f}" if "ron95" in latest else None
        price97 = f"{latest['ron97']:.2f}" if "ron97" in latest else None
        price_diesel = f"{latest['diesel']:.2f}" if "diesel" in latest else None
        price_diesel_em = f"{latest['diesel_eastmsia']:.2f}" if "diesel_eastmsia" in latest else None
        budi_rate = float(latest["ron95_budi95"]) if "ron95_budi95" in latest else None

        if not price95:
            print("[WARN] RON95 field missing in API response, using fallback.")
        if not price97:
            print("[WARN] RON97 field missing in API response, using fallback.")
        if not price_diesel:
            print("[WARN] Diesel field missing in API response, using fallback.")
        if not price_diesel_em:
            print("[WARN] diesel_eastmsia field missing in API response, using fallback.")
        if budi_rate is None:
            print("[WARN] ron95_budi95 field missing in API response, using fallback.")

        effective_date = latest.get("date", "")
        if effective_date:
            print(f"[INFO] Fuel prices effective: {effective_date}")

        return (
            price95 or FALLBACK_PRICE_95,
            price97 or FALLBACK_PRICE_97,
            price_diesel or FALLBACK_PRICE_DIESEL,
            price_diesel_em or FALLBACK_PRICE_DIESEL_EM,
            budi_rate if budi_rate is not None else FALLBACK_BUDI_RATE,
        )

    except (requests.RequestException, KeyError, ValueError, IndexError) as e:
        print(f"[WARN] Fuel price fetch failed: {e}")

    return (FALLBACK_PRICE_95, FALLBACK_PRICE_97, FALLBACK_PRICE_DIESEL, FALLBACK_PRICE_DIESEL_EM, FALLBACK_BUDI_RATE)


def load_prices_async():
    """Fetch all fuel prices in background, then update UI safely."""
    price95, price97, price_diesel, price_diesel_em, budi_rate = fetch_fuel_prices()
    root.after(0, lambda: app.update_fuel_prices(price95, price97, price_diesel, price_diesel_em, budi_rate))


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

        self.price_ron95: str = FALLBACK_PRICE_95
        self.price_ron97: str = FALLBACK_PRICE_97
        self.price_diesel: str = FALLBACK_PRICE_DIESEL
        self.price_diesel_em: str = FALLBACK_PRICE_DIESEL_EM
        self.budi_rate: float = FALLBACK_BUDI_RATE

        self.subsidized_var = tk.BooleanVar(value=False)
        self.ron97_var = tk.BooleanVar(value=False)
        self.diesel_var = tk.BooleanVar(value=False)
        self.region_var = tk.StringVar(value="wm")  # "wm" or "em"
        self.results: dict[str, tk.StringVar] = {k: tk.StringVar() for k in self.OUTPUT_KEYS}
        self.entries: dict[str, ttk.Entry] = {}
        self._resetting = False  # Guard to suppress toggle side-effects during reset

        self._build_ui()

        # Attach toggle handlers after UI is built
        self.ron97_var.trace_add("write", lambda *_: self._on_fuel_toggle("ron97"))
        self.diesel_var.trace_add("write", lambda *_: self._on_fuel_toggle("diesel"))
        self.subsidized_var.trace_add("write", lambda *_: self._on_subsidy_toggle())

    # --- UI BUILDING ---
    def _build_ui(self):
        main = ttk.Frame(self.root, padding="15")
        main.grid(row=0, column=0, sticky="NSEW")

        # Live rate header
        self.header_label = ttk.Label(
            main,
            text="Fetching live fuel rates...",
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

        self.entries["market_price"].insert(0, self.price_ron95)

        # --- Fuel type checkboxes ---
        fuel_frame = ttk.LabelFrame(main, text="Fuel Type", padding="5")
        fuel_frame.grid(row=6, columnspan=2, pady=(10, 2), sticky="EW", padx=5)

        self.ron97_check = ttk.Checkbutton(
            fuel_frame, text="RON97", variable=self.ron97_var
        )
        self.ron97_check.pack(side="left", padx=10)

        self.diesel_check = ttk.Checkbutton(
            fuel_frame, text="Diesel", variable=self.diesel_var
        )
        self.diesel_check.pack(side="left", padx=10)

        # --- Region radio buttons ---
        region_frame = ttk.LabelFrame(main, text="Region", padding="5")
        region_frame.grid(row=7, columnspan=2, pady=(2, 2), sticky="EW", padx=5)

        ttk.Radiobutton(
            region_frame, text="West Malaysia",
            variable=self.region_var, value="wm",
            command=self._on_region_toggle,
        ).pack(side="left", padx=10)
        ttk.Radiobutton(
            region_frame, text="East Malaysia",
            variable=self.region_var, value="em",
            command=self._on_region_toggle,
        ).pack(side="left", padx=10)

        # BUDI95 subsidy checkbox (RON95 only, both regions)
        self.subsidy_check = ttk.Checkbutton(
            main,
            text="Eligible for BUDI95 subsidised rate",
            variable=self.subsidized_var,
        )
        self.subsidy_check.grid(row=8, columnspan=2, pady=(2, 10))

        # Calculate button
        ttk.Button(main, text="Calculate Efficiency", command=self.calculate).grid(
            row=9, columnspan=2, pady=10
        )

        # Result labels
        row_idx = 10
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
    def update_fuel_prices(self, price95: str, price97: str, price_diesel: str, price_diesel_em: str, budi_rate: float):
        """Called from async thread to safely update UI with fetched prices."""
        self.price_ron95 = price95
        self.price_ron97 = price97
        self.price_diesel = price_diesel
        self.price_diesel_em = price_diesel_em
        self.budi_rate = budi_rate
        self.header_label.config(
            text=f"RON95: RM{price95}  |  RON97: RM{price97}  |  Diesel: RM{price_diesel} (WM) / RM{price_diesel_em} (EM)"
        )
        self._sync_market_rate()

    def _active_fuel(self) -> str:
        """Return the currently selected fuel type: 'ron95', 'ron97', or 'diesel'."""
        if self.ron97_var.get():
            return "ron97"
        if self.diesel_var.get():
            return "diesel"
        return "ron95"

    def _is_east_malaysia(self) -> bool:
        return self.region_var.get() == "em"

    def _sync_market_rate(self):
        """Update the market rate entry to match the currently selected fuel and region."""
        fuel = self._active_fuel()
        if fuel == "diesel" and self._is_east_malaysia():
            price = self.price_diesel_em
        else:
            price_map = {
                "ron95": self.price_ron95,
                "ron97": self.price_ron97,
                "diesel": self.price_diesel,
            }
            price = price_map[fuel]
        self.entries["market_price"].delete(0, "end")
        self.entries["market_price"].insert(0, price)

    def _on_fuel_toggle(self, changed: str):
        """Enforce mutual exclusion across fuel checkboxes and manage subsidy state."""
        if self._resetting:
            return  # Reset handles all state itself — skip side-effects

        # If the changed checkbox was just ticked, untick the other one
        if changed == "ron97" and self.ron97_var.get():
            self.diesel_var.set(False)
        elif changed == "diesel" and self.diesel_var.get():
            self.ron97_var.set(False)

        fuel = self._active_fuel()

        # BUDI95 applies to RON95 regardless of region
        if fuel == "ron95":
            self.subsidy_check.config(state="normal")
        else:
            self.subsidized_var.set(False)
            self.subsidy_check.config(state="disabled")

        # Disable the other fuel checkbox to prevent both being ticked simultaneously
        if fuel == "ron97":
            self.diesel_check.config(state="disabled")
            self.ron97_check.config(state="normal")
        elif fuel == "diesel":
            self.ron97_check.config(state="disabled")
            self.diesel_check.config(state="normal")
        else:
            # RON95 (neither ticked) — re-enable both
            self.ron97_check.config(state="normal")
            self.diesel_check.config(state="normal")

        self._sync_market_rate()

    def _on_region_toggle(self):
        """Handle region toggle: sync market rate (diesel price changes by region)."""
        self._sync_market_rate()

    def _on_subsidy_toggle(self):
        """Swap market rate field between BUDI rate and actual market rate."""
        if self._resetting:
            return
        if self.subsidized_var.get():
            self.entries["market_price"].delete(0, "end")
            self.entries["market_price"].insert(0, f"{self.budi_rate:.2f}")
        else:
            self._sync_market_rate()  # Restore market rate for selected fuel

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
        self._resetting = True
        try:
            # Clear all input fields
            for entry in self.entries.values():
                entry.delete(0, "end")
            # Reset checkboxes (traces are suppressed by _resetting guard)
            self.subsidized_var.set(False)
            self.ron97_var.set(False)
            self.diesel_var.set(False)
            # Re-enable all checkboxes
            self.ron97_check.config(state="normal")
            self.diesel_check.config(state="normal")
            self.subsidy_check.config(state="normal")
            # Reset region to West Malaysia
            self.region_var.set("wm")
            # Populate market rate once, cleanly
            self.entries["market_price"].insert(0, self.price_ron95)
            for var in self.results.values():
                var.set("")
        finally:
            self._resetting = False

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

        # --- Subsidy logic (RON95 only) ---
        fuel = self._active_fuel()
        if fuel == "ron95" and self.subsidized_var.get():
            actual_paid = liters * self.budi_rate
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
        fuel_label = {"ron95": "RON95", "ron97": "RON97", "diesel": "Diesel"}[fuel]
        updates = {
            "liters": f"Liters: {liters:.3f} L  ({fuel_label})",
            "paid": f"Actual Paid: RM {actual_paid:.2f}",
            "market": f"Pump Value: RM {pump_market_value:.2f}",
            "savings": f"Total Savings: RM {savings:.2f}" if (fuel == "ron95" and self.subsidized_var.get()) else "",
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

    # Fetch live prices without blocking the UI
    threading.Thread(target=load_prices_async, daemon=True).start()

    root.mainloop()
