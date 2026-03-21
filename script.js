// --- CONSTANTS ---
const MPG_TO_L100KM = 235.215;
const BUDI_RATE = 1.99;
const KM_TO_MILES = 1.60934;
const L_TO_GALLONS = 0.264172;
const FALLBACK = { ron95: "3.27", ron97: "4.55", diesel: "2.35" };
const API_URL = "https://api.data.gov.my/data-catalogue?id=fuelprice&limit=1&sort=-date";

let currentPrices = { ...FALLBACK };

// --- FETCHING LOGIC ---
async function fetchPrices() {
    try {
        const response = await fetch(API_URL);
        const data = await response.json();
        if (data && data.length > 0) {
            const latest = data[0];
            currentPrices.ron95 = latest.ron95?.toFixed(2) || FALLBACK.ron95;
            currentPrices.ron97 = latest.ron97?.toFixed(2) || FALLBACK.ron97;
            currentPrices.diesel = latest.diesel?.toFixed(2) || FALLBACK.diesel;
            
            document.getElementById('header').innerText = 
                `RON95: RM${currentPrices.ron95} | RON97: RM${currentPrices.ron97} | Diesel: RM${currentPrices.diesel}`;
            document.getElementById('header').style.color = "#2e7d32";
            syncMarketRate();
        }
    } catch (e) {
        console.warn("API fetch failed, using fallbacks.", e);
        document.getElementById('header').innerText = "Using offline fuel rates.";
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
        subsidyContainer.style.opacity = "1";
        subsidyCheck.disabled = false;
    } else {
        subsidyContainer.style.opacity = "0.5";
        subsidyCheck.checked = false;
        subsidyCheck.disabled = true;
    }
    syncMarketRate();
}

// --- CALCULATION LOGIC (Direct Port from Python) ---
function calculate() {
    const market_rate = parseFloat(document.getElementById('market_price').value);
    const mpg_input = parseFloat(document.getElementById('mpg').value);
    const km_input = parseFloat(document.getElementById('km').value);
    const pump_rm = parseFloat(document.getElementById('pump_display_rm').value);
    const manual_liters = parseFloat(document.getElementById('liters').value);
    const isSubsidized = document.getElementById('subsidized_var').checked;
    const fuelType = document.querySelector('input[name="fuel"]:checked').value;

    if (!market_rate || market_rate <= 0) {
        alert("Market price is required.");
        return;
    }

    let liters, km;

    // Priority 1: MPG Input
    if (mpg_input > 0) {
        const l_100km = MPG_TO_L100KM / mpg_input;
        liters = l_100km;
        km = 100.0;
    } 
    // Priority 2: Distance + Liters/Pump
    else {
        km = km_input;
        if (!km || km <= 0) {
            alert("Distance (KM) is required when not using MPG.");
            return;
        }

        if (manual_liters > 0) {
            liters = manual_liters;
        } else if (pump_rm > 0) {
            liters = pump_rm / market_rate;
        } else {
            alert("Provide Liters, Pump Display, or MPG.");
            return;
        }
    }

    if (liters <= 0) return;

    const pump_market_value = liters * market_rate;
    let actual_paid, savings;

    if (fuelType === "ron95" && isSubsidized) {
        actual_paid = liters * BUDI_RATE;
        savings = pump_market_value - actual_paid;
    } else {
        actual_paid = pump_market_value;
        savings = 0.0;
    }

    // Derived Metrics
    const cost_per_km = actual_paid / km;
    const km_per_l = km / liters;
    const l_per_100km = (100 * liters) / km;
    const mpg_display = mpg_input ? mpg_input : (km / KM_TO_MILES) / (liters * L_TO_GALLONS);

    // Display Results
    const fuelLabel = fuelType.toUpperCase();
    document.getElementById('res_liters').innerText = `Liters: ${liters.toFixed(3)} L (${fuelLabel})`;
    document.getElementById('res_paid').innerText = `Actual Paid: RM ${actual_paid.toFixed(2)}`;
    document.getElementById('res_market').innerText = `Pump Value: RM ${pump_market_value.toFixed(2)}`;
    document.getElementById('res_savings').innerText = savings > 0 ? `Total Savings: RM ${savings.toFixed(2)}` : "";
    document.getElementById('res_rm_km').innerText = `Cost: RM ${cost_per_km.toFixed(2)} / km`;
    document.getElementById('res_km_l').innerText = `Efficiency: ${km_per_l.toFixed(2)} km/L`;
    document.getElementById('res_l100').innerText = `L/100 km: ${l_per_100km.toFixed(2)}`;
    document.getElementById('res_mpg').innerText = `MPG: ${mpg_display.toFixed(2)}`;
    
    document.getElementById('results').style.display = "block";
}

function resetForm() {
    document.querySelectorAll('input[type="number"]').forEach(i => i.value = "");
    document.getElementById('subsidized_var').checked = false;
    document.getElementById('results').style.display = "none";
    syncMarketRate();
}

// Init
fetchPrices();
