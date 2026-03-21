# ⛽ BUDI95 Trip & Efficiency Calculator (MY)

A precision web-based utility for Malaysian motorists to calculate fuel economy, trip costs, and subsidy savings.

**🚀 [Live Demo](https://kennychan-git.github.io/fuel-efficiency-calc/)**

---

## 🌟 Latest Features

* **🇲🇾 Regional Pricing:** Toggle between **West Malaysia** and **East Malaysia** to automatically adjust for regional diesel price variances.
* **📡 Live API Integration:** Fetches real-time prices for RON95, RON97, and Diesel directly from [data.gov.my](https://data.gov.my).
* **💰 Dynamic Subsidy Logic:** * Automatically updates the **BUDI95** rate from the API.
    * Calculates "Actual Paid" vs "Pump Value" to show your total savings.
* **🔄 Unit Conversion Mode:** Toggle to "MPG Mode" for instant conversion to Metric (L/100km & km/L) without financial calculations.
* **🚦 Efficiency Gauge:** Instant visual feedback (Green/Yellow/Red) based on your vehicle's L/100km performance.
* **🛡️ Reliability:** Built-in "Amber" fallback mode ensures the tool works even if the government API is temporarily offline.

## 🛠️ Technical Implementation

The app logic is strictly mirrored from a proven Python/Tkinter core:
- **Constants:** $MPG\_TO\_L100KM = 235.215$, $KM\_TO\_MILES = 1.60934$.
- **Prioritization:** The script prioritizes **MPG input** for unit conversion; otherwise, it calculates based on **Distance + (Liters or RM)**.
- **Tech Stack:** Vanilla JavaScript (ES6+), HTML5, CSS3. No heavy frameworks, ensuring fast loading on mobile data.

## 📂 Files

* `index.html`: Responsive UI with region and fuel toggles.
* `script.js`: Core engine handling API fetching, regional logic, and math.
* `fuel_efficiency_calc.py`: The original desktop version of the tool.

## ⚖️ License

MIT License - free to use and modify.

---
*Maintained by [kennychan-git](https://github.com/kennychan-git)*
