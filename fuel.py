import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk 

def calculate_efficiency():
    liters = float(entry_liters.get()) if entry_liters.get() else None
    km = float(entry_km.get()) if entry_km.get() else None
    fuel_price = float(entry_fuel_price.get()) if entry_fuel_price.get() else None
    pump_price = float(entry_pump_price.get()) if entry_pump_price.get() else None

    if not liters:
        liters = pump_price / fuel_price
    if not km:
        km = (100 * liters) / fuel_price
    if not fuel_price:
        fuel_price = pump_price / liters
    if not pump_price:
        pump_price = liters * fuel_price

    result_l_100km = (100 * liters) / km
    result_rm_km = (pump_price) / km
    result_km_l = km / liters

    result_liters_var.set(f"Liters: {liters:.2f}")
    result_km_var.set(f"Kilometers: {km:.2f}")
    result_fuel_price_var.set(f"Fuel price (RM/L): {fuel_price:.2f}")
    result_pump_price_var.set(f"Pump price (RM): {pump_price:.2f}")
    result_l_100km_var.set(f"L/100 km: {result_l_100km:.2f}")
    result_rm_km_var.set(f"RM/km: {result_rm_km:.2f}")
    result_km_l_var.set(f"km/L: {result_km_l:.2f}")

# Replace the following line:
# root = tk.Tk()
# with:
root = ThemedTk(theme="arc")  # Replace 'arc' with your desired theme
root.title("Fuel Efficiency Converter")
# Create a custom font
custom_font = ("Helvetica", 12)

# Create a style for the Frame
style = ttk.Style()
style.configure("Custom.TFrame", background="white")


mainframe = ttk.Frame(root, padding="10", style="Custom.TFrame")
mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))


root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Configure the mainframe's column and row weights
for i in range(3):
    mainframe.columnconfigure(i, weight=1)
for i in range(9):
    mainframe.rowconfigure(i, weight=1)



# Update grid options for all widgets inside the mainframe
# Replace sticky=(tk.W) with sticky=(tk.N, tk.S, tk.E, tk.W) for all widgets
# For example, change the following line:
# entry_x.grid(row=1, column=0, sticky=(tk.W), padx=5, pady=5)
# to:
ttk.Label(mainframe, text="Liters:", font=custom_font, foreground="blue", background="white").grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), padx=5, pady=5)
entry_liters = ttk.Entry(mainframe, width=7, font=custom_font)
entry_liters.grid(row=0, column=1, padx=5, pady=5)

#ttk.Label(mainframe, text="Liters:").grid(row=0, column=0, sticky=(tk.E), padx=5)
#entry_liters = ttk.Entry(mainframe, width=7)
#entry_liters.grid(row=0, column=1, padx=5)

ttk.Label(mainframe, text="Kilometers:",font=custom_font, foreground="blue", background="white").grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), padx=5)
entry_km = ttk.Entry(mainframe, width=7)
entry_km.grid(row=1, column=1, padx=5)

ttk.Label(mainframe, text="Fuel price (RM/L):",font=custom_font, foreground="blue", background="white").grid(row=2, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), padx=5)
entry_fuel_price = ttk.Entry(mainframe, width=7)
entry_fuel_price.grid(row=2, column=1, padx=5)

ttk.Label(mainframe, text="Pump price (RM):",font=custom_font, foreground="blue", background="white").grid(row=3, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), padx=5)
entry_pump_price = ttk.Entry(mainframe, width=7)
entry_pump_price.grid(row=3, column=1, padx=5)

calculate_button = ttk.Button(mainframe, text="Calculate", command=calculate_efficiency)
calculate_button.grid(row=4, column=0, columnspan=4, pady=10)

result_liters_var = tk.StringVar()
result_liters_label = ttk.Label(mainframe, textvariable=result_liters_var)
result_liters_label.grid(row=5, column=0, columnspan=4)

result_km_var = tk.StringVar()
result_km_label = ttk.Label(mainframe, textvariable=result_km_var)
result_km_label.grid(row=6, column=0, columnspan=4)

result_fuel_price_var = tk.StringVar()
result_fuel_price_label = ttk.Label(mainframe, textvariable=result_fuel_price_var)
result_fuel_price_label.grid(row=7, column=0, columnspan=4)

result_pump_price_var = tk.StringVar()
result_pump_price_label = ttk.Label(mainframe, textvariable=result_pump_price_var)
result_pump_price_label.grid(row=8, column=0, columnspan=4)

result_l_100km_var = tk.StringVar()
result_l_100km_label = ttk.Label(mainframe, textvariable=result_l_100km_var)
result_l_100km_label.grid(row=9, column=0, columnspan=4)

result_rm_km_var = tk.StringVar()
result_rm_km_label = ttk.Label(mainframe, textvariable=result_rm_km_var)
result_rm_km_label.grid(row=10, column=0, columnspan=4)

result_km_l_var = tk.StringVar()
result_km_l_label = ttk.Label(mainframe, textvariable=result_km_l_var)
result_km_l_label.grid(row=11, column=0, columnspan=4)


# Add an image to a Label or Button (optional)
#photo = tk.PhotoImage(file="https://www.pexels.com/photo/gas-pump-nozzle-273543/")
#label = ttk.Label(mainframe, image=photo, background="white")
#label.grid(row=12, column=0, columnspan=4)

root.mainloop()
