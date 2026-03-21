# ⛽ BUDI95 Trip & Efficiency Calculator (MY)

A localized web utility for Malaysian motorists to analyze fuel consumption, trip costs, and subsidy savings using real-time market data.

**🚀 [Live Demo](https://kennychan-git.github.io/fuel-efficiency-calc/)**

---

## 🌟 Key Features

* **🇲🇾 Localized Calculation:** Designed for the Malaysian standard ($km/L$ and $L/100km$). Input your trip distance and either your pump receipt (RM) or total liters to get instant efficiency metrics.
* **📡 Live API Integration:** Fetches real-time prices for RON95, RON97, and Diesel (West & East Malaysia) directly from [data.gov.my](https://data.gov.my).
* **💰 BUDI95 Subsidy Engine:** Automatically calculates "Actual Paid" using the targeted subsidy rate vs. the current market pump value, showing your exact savings.
* **🗺️ Regional Support:** Dedicated toggle for **West vs. East Malaysia** to handle the different diesel pricing structures.
* **🔄 MPG Conversion Utility:** Includes support for converting MPG (miles per gallon) into local metric equivalents for easy vehicle comparison.
* **🚦 Efficiency Gauge:** Visual color-coded feedback (Green/Yellow/Red) based on your vehicle's $L/100km$ performance.

## 🛠️ Logic Prioritization

To ensure the most accurate results, the script follows this calculation hierarchy:

1. **Primary (Local Trip):** Calculates efficiency based on **Distance (KM)** combined with either **Manual Liters** or **Pump Display (RM)**. If Pump RM is used, it cross-references the live Market Rate to determine exact liters.
2. **Secondary (Conversion):** If an **MPG** value is provided, the script pivots to a conversion-only mode, providing the metric equivalent ($L/100km$ and $km/L$) while hiding financial data that doesn't apply to a simple unit conversion.

## 📂 Project Structure

* `index.html`: Responsive UI with region and fuel toggles.
* `script.js`: The "engine" handling API fetching, regional pricing, and math logic.
* `fuel_efficiency_calc.py`: The original desktop version of the tool (Legacy).

## ⚖️ License

MIT License - free to use and modify.

---
*Maintained by [kennychan-git](https://github.com/kennychan-git)*
