# ⛽ BUDI95 Trip & MPG Calculator

A precision fuel efficiency and subsidy calculator designed for Malaysian motorists. This tool helps you calculate trip costs, fuel economy (km/L, L/100km, MPG), and potential savings under the **BUDI95** subsidy program.

**🚀 [Live Demo](https://kennychan-git.github.io/fuel-efficiency-calc/)**

---

## 🌟 Key Features

* **Live Fuel Rates:** Automatically fetches the latest RON95, RON97, and Diesel prices from the [data.gov.my](https://data.gov.my) API.
* **BUDI95 Subsidy Logic:** Calculate actual out-of-pocket costs and total savings when using the RM1.99 targeted subsidy rate.
* **Dual-Mode Calculation:**
    * **Trip Mode:** Input distance and fuel amount (RM or Liters) to see trip costs and efficiency.
    * **Conversion Mode:** Input MPG to instantly get metric equivalents (L/100km, km/L) without financial fluff.
* **Efficiency Gauge:** Visual color-coded feedback based on your vehicle's consumption.
* **Mobile Responsive:** Designed to be used on-the-go at the petrol station.

## 📊 Logic & Constants

The calculator uses the following proven conversion logic:
* **MPG to L/100km:** $235.215 / MPG$
* **Distance:** $KM / 1.60934$ to Miles
* **Volume:** $Liters * 0.264172$ to Gallons
* **Subsidized Rate:** Hardcoded to **RM 1.99/L** per BUDI95 guidelines.

## 🛠️ Tech Stack

* **Frontend:** HTML5, CSS3, Vanilla JavaScript (ES6+).
* **API:** [Data.gov.my Fuel Price API](https://developer.data.gov.my/).
* **Deployment:** GitHub Pages.
* *Original logic ported from a Python/Tkinter desktop application.*

## 📂 Project Structure

* `index.html`: The UI structure and responsive styling.
* `script.js`: Core logic, API handling, and DOM manipulation.
* `fuel_efficiency_calc.py`: The original Python/Tkinter version (Legacy).

## 🚀 How to Use Locally

If you wish to run the web version locally:
1. Clone the repository.
2. Open `index.html` in any modern web browser.
3. (Optional) Run the Python version: `python fuel_efficiency_calc.py` (requires `ttkthemes`).

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Maintained by [kennychan-git](https://github.com/kennychan-git)*
