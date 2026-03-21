// --- CONSTANTS ---
const MPG_TO_L100KM = 235.215;
const KM_TO_MILES = 1.60934;
const L_TO_GALLONS = 0.264172;
const FALLBACK = { ron95: "3.27", ron97: "4.55", diesel: "4.72", diesel_em: "2.15", budi95: "1.99" };
const API_URL = "https://api.data.gov.my/data-catalogue?id=fuelprice&limit=1&sort=-date";

let currentPrices = { ...FALLBACK };
let budiRate = parseFloat(FALLBACK.budi95);  // Updated from API on fetch

// --- PRICE FETCHING ---
async function fetchPrices() {
    const header = document.getElementById('header');
    header.style.color = "#888";
    header.innerText = "Fetching live fuel rates...";

    try {
        const response = await fetch(API_URL);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        if (!data || data.length === 0) {
            throw new Error("Empty response");
        }

        const latest = data[0];
        currentPrices.ron95 = latest.ron95?.toFixed(2) || FALLBACK.ron95;
        currentPrices.ron97 = latest.ron97?.toFixed(2) || FALLBACK.ron97;
        currentPrices.diesel = latest.diesel?.toFixed(2) || FALLBACK.diesel;
        currentPrices.diesel_em = latest.diesel_eastmsia?.toFixed(2) || FALLBACK.diesel_em;
        budiRate = latest.ron95_budi95 ?? parseFloat(FALLBACK.budi95);

        // Format effective date e.g. "2026-03-19" → "19 Mar 2026"
        const effectiveDate = formatDate(latest.date);
        const dateSuffix = effectiveDate ? ` · Effective ${effectiveDate}` : "";

        header.style.color = "#2e7d32";  // Green = live data
        header.innerHTML =
            `✓ Live  &nbsp;|&nbsp; ` +
            `RON95: <strong>RM${currentPrices.ron95}</strong> &nbsp;|&nbsp; ` +
            `RON97: <strong>RM${currentPrices.ron97}</strong> &nbsp;|&nbsp; ` +
            `Diesel: <strong>RM${currentPrices.diesel}</strong>` +
            `<br><span style="font-weight:normal; font-size:0.75rem;">${dateSuffix}</span>`;

        syncMarketRate();

    } catch (e) {
        // Clearly signal fallback mode with the hardcoded values shown
        header.style.color = "#e65100";  // Amber = fallback
        header.innerHTML =
            `⚠ Could not reach data.gov.my — using last known prices &nbsp;|&nbsp; ` +
            `RON95: <strong>RM${FALLBACK.ron95}</strong> &nbsp;|&nbsp; ` +
            `RON97: <strong>RM${FALLBACK.ron97}</strong> &nbsp;|&nbsp; ` +
            `Diesel: <strong>RM${FALLBACK.diesel}</strong>` +
            `<br><span style="font-weight:normal; font-size:0.75rem;">Prices may not reflect the current week. Verify before use.</span>`;

        syncMarketRate();
        console.warn("[WARN] Fuel price fetch failed:", e.message);
    }
}

function formatDate(dateStr) {
    if (!dateStr) return null;
    const d = new Date(dateStr);
    if (isNaN(d)) return dateStr;  // Return raw string if unparseable
    return d.toLocaleDateString("en-MY", { day: "numeric", month: "short", year: "numeric" });
}

// --- REGION + FUEL TOGGLE ---
function isEastMalaysia() {
    const checked = document.querySelector('input[name="region"]:checked');
    return checked ? checked.value === "em" : false;
}

function syncMarketRate() {
    const fuel = document.querySelector('input[name="fuel"]:checked').value;
    const em = isEastMalaysia();
    // East Malaysia diesel uses its own subsidised rate from the API
    const priceKey = (fuel === "diesel" && em) ? "diesel_em" : fuel;
    const price = currentPrices[priceKey];
    console.log(`[syncMarketRate] fuel=${fuel} em=${em} priceKey=${priceKey} price=${price}`);
    document.getElementById('market_price').value = price || "";
}

function onFuelToggle() {
    const fuel = document.querySelector('input[name="fuel"]:checked').value;
    const subsidyCheck = document.getElementById('subsidized_var');
    const subsidyContainer = document.getElementById('subsidy_container');
    // BUDI95 applies to RON95 regardless of region
    if (fuel === "ron95") {
        subsidyContainer.classList.remove("hidden");
        subsidyCheck.disabled = false;
    } else {
        subsidyContainer.classList.add("hidden");
        subsidyCheck.checked = false;
    }
    syncMarketRate();
}

function onRegionToggle() {
    // Re-run fuel toggle logic to update subsidy visibility + market rate
    onFuelToggle();
}

// --- CALCULATE ---
function calculate() {
    const market_rate = parseFloat(document.getElementById('market_price').value);

    if (!market_rate || market_rate <= 0) {
        alert("Market rate is required and must be a positive number.");
        document.getElementById('market_price').focus();
        return;
    }

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
        liters = MPG_TO_L100KM / mpg_input;
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

    if (liters <= 0) { alert("Liters must be greater than zero."); return; }

    // --- CALCULATIONS ---
    const km_per_l = km / liters;
    const l_per_100km = (100 * liters) / km;
    const mpg_display = isMpgMode ? mpg_input : (km / KM_TO_MILES) / (liters * L_TO_GALLONS);

    document.getElementById('res_km_l').innerText = `${km_per_l.toFixed(2)} km/L`;
    document.getElementById('res_l100').innerText = `${l_per_100km.toFixed(2)} L/100km`;
    document.getElementById('res_mpg').innerText = `${mpg_display.toFixed(2)} MPG`;

    // Efficiency gauge (green < 7L, yellow 7–11L, red > 11L)
    const gauge = document.getElementById('gauge');
    const percentage = Math.min((l_per_100km / 20) * 100, 100);
    gauge.style.width = `${percentage}%`;
    gauge.style.backgroundColor = l_per_100km < 7 ? "#2e7d32" : (l_per_100km < 11 ? "#fbc02d" : "#d32f2f");

    // --- FINANCIAL RESULTS ---
    const moneyBox = document.getElementById('money_results');
    if (isMpgMode) {
        moneyBox.style.display = "none";
    } else {
        moneyBox.style.display = "block";
        const pump_market_value = liters * market_rate;
        const actual_paid = (fuelType === "ron95" && isSubsidized) ? (liters * budiRate) : pump_market_value;
        const savings = pump_market_value - actual_paid;

        document.getElementById('res_liters').innerText = `${liters.toFixed(3)} L (${fuelType.toUpperCase()})`;
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

// --- RESET ---
function resetForm() {
    document.querySelectorAll('input[type="number"]').forEach(i => i.value = "");
    document.getElementById('results').style.display = "none";
    // Reset region to West Malaysia and fuel to RON95
    document.querySelector('input[name="region"][value="wm"]').checked = true;
    document.querySelector('input[name="fuel"][value="ron95"]').checked = true;
    onFuelToggle();  // Restores subsidy visibility + syncs market rate
}

// --- INIT ---
fetchPrices();
