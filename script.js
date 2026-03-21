// --- CONSTANTS (Proven Logic) ---
const MPG_TO_L100KM = 235.215;
const BUDI_RATE = 1.99;
const KM_TO_MILES = 1.60934;
const L_TO_GALLONS = 0.264172;
const FALLBACK = { ron95: "3.27", ron97: "4.55", diesel: "2.35" };
const API_URL = "https://api.data.gov.my/data-catalogue?id=fuelprice&limit=1&sort=-date";

let currentPrices = { ...FALLBACK };

async function fetchPrices() {
    try {
        const response = await fetch(API_URL);
        const data = await response.json();
        if (data && data.length > 0) {
            const latest = data[0];
            currentPrices.ron95 = latest.ron95?.toFixed(2) || FALLBACK.ron95;
            currentPrices.ron97 = latest.ron97?.toFixed(2) || FALLBACK.ron97;
            currentPrices.diesel = latest.diesel?.toFixed(2) || FALLBACK.diesel;
            document.getElementById('header').innerText = `Rates: 95:RM${currentPrices.ron95} | 97:RM${currentPrices.ron97} | D:RM${currentPrices.diesel}`;
            syncMarketRate();
        }
    } catch (e) {
        document.getElementById('header').innerText = "Using default fuel rates.";
    }
}

function syncMarketRate() {
    const fuel = document.querySelector('input[name="fuel"]:checked').value;
    document.getElementById('market_price').value = currentPrices[fuel];
}

function onFuelToggle() {
    const fuel = document.querySelector('input[name="fuel"]:checked').value;
    const subsidyCheck = document.getElementById('subsidized_var');
    const subsidyContainer = document.getElementById('subsidy_container');
    if (fuel === "ron95") {
        subsidyContainer.style.display = "block";
        subsidyCheck.disabled = false;
    } else {
        subsidyContainer.style.display = "none";
        subsidyCheck.checked = false;
    }
    syncMarketRate();
}

function calculate() {
    const market_rate = parseFloat(document.getElementById('market_price').value);
    const mpg_input = parseFloat(document.getElementById('mpg').value);
    const km_input = parseFloat(document.getElementById('km').value);
    const pump_rm = parseFloat(document.getElementById('pump_display_rm').value);
    const manual_liters = parseFloat(document.getElementById('liters').value);
    const isSubsidized = document.getElementById('subsidized_var').checked;
    const fuelType = document.querySelector('input[name="fuel"]:checked').value;

    let liters, km, isMpgMode = false;

    // --- LOGIC PRIORITY ---
    if (mpg_input > 0) {
        isMpgMode = true;
        const l_100km = MPG_TO_L100KM / mpg_input;
        liters = l_100km;
        km = 100.0;
    } else {
        km = km_input;
        if (!km || km <= 0) { alert("Distance (KM) is required."); return; }
        if (manual_liters > 0) {
            liters = manual_liters;
        } else if (pump_rm > 0) {
            liters = pump_rm / market_rate;
        } else {
            alert("Provide Liters, Pump RM, or MPG.");
            return;
        }
    }

    // --- CALCULATIONS ---
    const km_per_l = km / liters;
    const l_per_100km = (100 * liters) / km;
    const mpg_display = isMpgMode ? mpg_input : (km / KM_TO_MILES) / (liters * L_TO_GALLONS);

    // Update Technical UI
    document.getElementById('res_km_l').innerText = `${km_per_l.toFixed(2)} km/L`;
    document.getElementById('res_l100').innerText = `${l_per_100km.toFixed(2)} L/100km`;
    document.getElementById('res_mpg').innerText = `${mpg_display.toFixed(2)} MPG`;

    // Update Efficiency Gauge (Color logic: Green < 7L, Yellow 7-10L, Red > 10L)
    const gauge = document.getElementById('gauge');
    let percentage = (l_per_100km / 20) * 100; // Scaled to 20L max
    percentage = Math.min(percentage, 100);
    gauge.style.width = `${percentage}%`;
    gauge.style.backgroundColor = l_per_100km < 7 ? "#2e7d32" : (l_per_100km < 11 ? "#fbc02d" : "#d32f2f");

    // --- CONDITIONAL FINANCIAL UI ---
    const moneyBox = document.getElementById('money_results');
    if (isMpgMode) {
        moneyBox.style.display = "none";
    } else {
        moneyBox.style.display = "block";
        const pump_market_value = liters * market_rate;
        let actual_paid = (fuelType === "ron95" && isSubsidized) ? (liters * BUDI_RATE) : pump_market_value;
        let savings = pump_market_value - actual_paid;

        document.getElementById('res_liters').innerText = `${liters.toFixed(2)} L (${fuelType.toUpperCase()})`;
        document.getElementById('res_paid').innerText = `RM ${actual_paid.toFixed(2)}`;
        document.getElementById('res_market').innerText = `RM ${pump_market_value.toFixed(2)}`;
        document.getElementById('res_rm_km').innerText = `RM ${(actual_paid / km).toFixed(2)} / km`;
        
        const saveRow = document.getElementById('res_savings_row');
        if (savings > 0) {
            saveRow.style.display = "flex";
            document.getElementById('res_savings').innerText = `RM ${savings.toFixed(2)}`;
        } else {
            saveRow.style.display = "none";
        }
    }
    
    document.getElementById('results').style.display = "block";
}

function resetForm() {
    document.querySelectorAll('input').forEach(i => i.type === "number" ? i.value = "" : null);
    document.getElementById('results').style.display = "none";
    syncMarketRate();
}

fetchPrices();
