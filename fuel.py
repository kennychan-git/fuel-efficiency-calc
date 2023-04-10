import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk 

######################################################
#                      RESET BUTTON ACTIONS CLEAR EVERYTHING 
######################################################
def reset():
    # Clear all the input fields
    entry_liters.delete(0, 'end')
    entry_km.delete(0, 'end')
    entry_fuel_price.delete(0, 'end')
    entry_pump_price.delete(0, 'end')
    entry_mpg.delete(0, 'end')

    # Clear all the result fields
    result_liters_var.set("")
    result_km_var.set("")
    result_fuel_price_var.set("")
    result_pump_price_var.set("")
    result_l_100km_var.set("")
    result_rm_km_var.set("")
    result_km_l_var.set("")
    result_mpg_var.set("")


######################################################
#                      ERROR MESSAGE HANDLING
######################################################
import tkinter as tk
from tkinter import messagebox

def handle_error():
    # Show error message in a pop-up window
    messagebox.showerror("Error", "use either MPG or input more parameters for conversion.")
    
    reset()

# Create a button to trigger the error
#error_button = tk.Button(root, text="Input error", command=handle_error)
#error_button.pack()



######################################################
#                      CALCULATION FOR METRIC AND IMPERIAL 
######################################################

import tkinter as tk
from tkinter import ttk, messagebox

def calculate_efficiency():
    try:
        mpg = float(entry_mpg.get()) if entry_mpg.get() else None
        if mpg:
            km_per_gallon = 1.60934 / 3.78541 * mpg
            liters = 100 / km_per_gallon
            km = 100

            result_l_100km = (100 * liters) / km
            result_km_l = km / liters

            result_liters_var.set(f"Liters: {liters:.2f}")
            result_km_var.set(f"Kilometers: {km:.2f}")
            result_l_100km_var.set(f"L/100 km: {result_l_100km:.2f}")
            result_km_l_var.set(f"km/L: {result_km_l:.2f}")
        else:
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
            result_mpg = (km / 1.60934) / (liters * 0.264172)
            result_mpg_var.set(f"MPG: {result_mpg:.2f}")
    except Exception as e:
        messagebox.showerror(title="Error", message="Use either MPG or input more parameters for conversion.")




def calculate_efficiency_working():
    mpg = float(entry_mpg.get()) if entry_mpg.get() else None
    if mpg:
        km_per_gallon = 1.60934 / 3.78541 * mpg
        liters = 100 / km_per_gallon
        km = 100
        #fuel_price = float(entry_fuel_price.get()) if entry_fuel_price.get() else None
        #pump_price = liters * fuel_price
        
        result_l_100km = (100 * liters) / km
        #result_rm_km = (pump_price) / km
        result_km_l = km / liters
    
        result_liters_var.set(f"Liters: {liters:.2f}")
        result_km_var.set(f"Kilometers: {km:.2f}")
        #result_fuel_price_var.set(f"Fuel price (RM/L): {fuel_price:.2f}")
        #result_pump_price_var.set(f"Pump price (RM): {pump_price:.2f}")
        result_l_100km_var.set(f"L/100 km: {result_l_100km:.2f}")
        #result_rm_km_var.set(f"RM/km: {result_rm_km:.2f}")
        result_km_l_var.set(f"km/L: {result_km_l:.2f}")
    else:
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
        result_mpg = (km / 1.60934) / (liters * 0.264172)
        result_mpg_var.set(f"MPG: {result_mpg:.2f}")




# Replace the following line:
# root = tk.Tk()
# with:
root = ThemedTk(theme="arc")  # Replace 'arc' with your desired theme
root.title("Fuel Efficiency Converter")
# Create a custom font
custom_font = ("Roboto", 12)
custom_font2 = ("Roboto",12)
custom_fontimportant = ("Roboto",16)
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

######################################################
#                      LABELLING FOR TITLE AND HOWTO
######################################################
#ttk.Label(mainframe, text="Enter MPG only or other metrics", font=custom_font, foreground="blue", background="white").grid(row=0, column=0, columnspan=4, sticky="NSEW", padx=5, pady=5)
ttk.Label(mainframe, text="Enter MPG only or other metrics", font=custom_font, foreground="blue", background="white").grid(row=0, column=0, columnspan=4, sticky=(tk.E), padx=5, pady=5)

#ttk.Label(mainframe, text="Enter MPG only or other metrics", font=custom_font, foreground="blue", background="white").grid(row=0, column=0, columnspan=4, sticky=(tk.N, tk.S, tk.E, tk.W), padx=5, pady=5)

#ttk.Label(mainframe, text="Enter MPG only or other metrics", font=custom_font, foreground="blue", background="white").grid(row=0, column=0, sticky=(tk.E), padx=5, pady=5)
#entry_liters = ttk.Entry(mainframe, width=7, font=custom_font)
#entry_liters.grid(row=0, column=1, padx=5, pady=5)


# Update grid options for all widgets inside the mainframe
# Replace sticky=(tk.W) with sticky=(tk.N, tk.S, tk.E, tk.W) for all widgets
# For example, change the following line:
# entry_x.grid(row=1, column=0, sticky=(tk.W), padx=5, pady=5)
# to:
######################################################
#                      INITIATE DISPLAYS FOR INPUTS AND BUTTONS
######################################################
for sohairow2 in range (2,3):
    ttk.Label(mainframe, text="Liters only:", font=custom_font, foreground="blue", background="white").grid(row=sohairow2, column=0, sticky=(tk.E), padx=5, pady=5)
    entry_liters = ttk.Entry(mainframe, width=7, font=custom_font)
    entry_liters.grid(row=sohairow2, column=1, padx=5, pady=5)
    sohairow2 +=1
    
    ttk.Label(mainframe, text="Kilometers only:",font=custom_font, foreground="blue", background="white").grid(row=sohairow2, column=0, sticky=(tk.E), padx=5)
    entry_km = ttk.Entry(mainframe, width=7)
    entry_km.grid(row=sohairow2, column=1, padx=5)
    sohairow2 +=1
    ttk.Label(mainframe, text="Fuel price (RM/L):",font=custom_font, foreground="blue", background="white").grid(row=sohairow2, column=0, sticky=(tk.E), padx=5)
    entry_fuel_price = ttk.Entry(mainframe, width=7)
    entry_fuel_price.grid(row=sohairow2, column=1, padx=5)
    sohairow2 +=1
    ttk.Label(mainframe, text="Pump price (RM):",font=custom_font, foreground="blue", background="white").grid(row=sohairow2, column=0, sticky=(tk.E), padx=5)
    entry_pump_price = ttk.Entry(mainframe, width=7)
    entry_pump_price.grid(row=sohairow2, column=1, padx=5)
    sohairow2 +=1
    ttk.Label(mainframe, text="MPG :",font=custom_font, foreground="blue", background="white").grid(row=sohairow2, column=0, sticky=(tk.E), padx=5)
    entry_mpg = ttk.Entry(mainframe, width=7)
    entry_mpg.grid(row=sohairow2, column=1, padx=5)
    sohairow2 +=1
    
    # create a custom font
    custom_font_button = ('Roboto', 12, 'bold')
    
    # create a button with the custom font
    #calculate_button = ttk.Button(mainframe, text="Calculate", font=custom_font)
    #calculate_button.grid(row=5, column=0, columnspan=4, pady=10)
    
    calculate_button = ttk.Button(mainframe, text="Convert", command=calculate_efficiency)
    calculate_button.grid(row=sohairow2, column=0, columnspan=4, pady=10)
    sohairow2 +=1
    
    reset_button = ttk.Button(mainframe, text="Reset", command=reset)
    reset_button.grid(row=sohairow2, column=0, columnspan=4, pady=10)
    sohairow2 +=1


######################################################
#                      INITIATE DISPLAYS FOR OUTPUTS 
######################################################
for sohairow in range (9,10):
    result_mpg_var = tk.StringVar()
    result_mpg_label = ttk.Label(mainframe, textvariable=result_mpg_var,font=custom_fontimportant)
    result_mpg_label.grid(row=sohairow, column=0, columnspan=4)
    sohairow +=1
    result_liters_var = tk.StringVar()
    result_liters_label = ttk.Label(mainframe, textvariable=result_liters_var,font=custom_font2)
    result_liters_label.grid(row=sohairow, column=0, columnspan=4)
    sohairow +=1
    result_km_var = tk.StringVar()
    result_km_label = ttk.Label(mainframe, textvariable=result_km_var,font=custom_font2)
    result_km_label.grid(row=sohairow, column=0, columnspan=4)
    sohairow +=1
    result_fuel_price_var = tk.StringVar()
    result_fuel_price_label = ttk.Label(mainframe, textvariable=result_fuel_price_var,font=custom_font2)
    result_fuel_price_label.grid(row=sohairow, column=0, columnspan=4)
    sohairow +=1
    result_pump_price_var = tk.StringVar()
    result_pump_price_label = ttk.Label(mainframe, textvariable=result_pump_price_var,font=custom_font2)
    result_pump_price_label.grid(row=sohairow, column=0, columnspan=4)
    sohairow +=1
    result_l_100km_var = tk.StringVar()
    result_l_100km_label = ttk.Label(mainframe, textvariable=result_l_100km_var,font=custom_font2)
    result_l_100km_label.grid(row=sohairow, column=0, columnspan=4)
    sohairow +=1
    result_rm_km_var = tk.StringVar()
    result_rm_km_label = ttk.Label(mainframe, textvariable=result_rm_km_var,font=custom_fontimportant)
    result_rm_km_label.grid(row=sohairow, column=0, columnspan=4)
    sohairow +=1
    result_km_l_var = tk.StringVar()
    result_km_l_label = ttk.Label(mainframe, textvariable=result_km_l_var,font=custom_fontimportant)
    result_km_l_label.grid(row=sohairow, column=0, columnspan=4)
    

# Add an image to a Label or Button (optional)
#photo = tk.PhotoImage(file="https://www.pexels.com/photo/gas-pump-nozzle-273543/")
#label = ttk.Label(mainframe, image=photo, background="white")
#label.grid(row=12, column=0, columnspan=4)

root.mainloop()
