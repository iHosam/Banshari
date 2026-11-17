/**
 * Banshari Global Automotive Spare Parts Metasearch Engine
 * Client-Side Controller & Real-Time Aggregator Renderer
 */

const STATE = {
    query: "",
    destinationCountry: "SA",
    currency: "SAR",
    searchMode: "auto",
    vehicle: {
        year: null,
        make: null,
        model: null,
        vin: null
    },
    filters: {
        listing_types: [],
        conditions: [],
        authenticity_tiers: [],
        sources: [],
        only_direct_shipping: false,
        exclude_hazmat: false
    },
    timerIntervals: []
};

// --- DOM Elements ---
const searchForm = document.getElementById("searchForm");
const searchInput = document.getElementById("searchInput");
const countrySelect = document.getElementById("countrySelect");
const currencySelect = document.getElementById("currencySelect");
const listingsContainer = document.getElementById("listingsContainer");
const emptyState = document.getElementById("emptyState");
const resultsTitle = document.getElementById("resultsTitle");
const resultsCountBadge = document.getElementById("resultsCountBadge");
const resultsSubtitle = document.getElementById("resultsSubtitle");
const interchangeBanner = document.getElementById("interchangeBanner");
const queryStatusPill = document.getElementById("queryStatusPill");
const queryStatusMode = document.getElementById("queryStatusMode");

// Garage elements
const garageYear = document.getElementById("garageYear");
const garageMake = document.getElementById("garageMake");
const garageModel = document.getElementById("garageModel");
const applyVehicleBtn = document.getElementById("applyVehicleBtn");
const clearVehicleBtn = document.getElementById("clearVehicleBtn");
const activeVehicleBadge = document.getElementById("activeVehicleBadge");
const activeVehicleLabel = document.getElementById("activeVehicleLabel");

// VIN modal elements
const openVinModalBtn = document.getElementById("openVinModalBtn");
const closeVinModalBtn = document.getElementById("closeVinModalBtn");
const vinModal = document.getElementById("vinModal");
const vinInput = document.getElementById("vinInput");
const decodeVinBtn = document.getElementById("decodeVinBtn");
const vinResultCard = document.getElementById("vinResultCard");
const vinMakeVal = document.getElementById("vinMakeVal");
const vinYearVal = document.getElementById("vinYearVal");
const vinCountryVal = document.getElementById("vinCountryVal");
const vinWmiVal = document.getElementById("vinWmiVal");

// Reset filter button
const resetFiltersBtn = document.getElementById("resetFiltersBtn");

// --- Initialization ---
document.addEventListener("DOMContentLoaded", () => {
    initEventListeners();
    performSearch();
});

function initEventListeners() {
    searchForm.addEventListener("submit", (e) => {
        e.preventDefault();
        STATE.query = searchInput.value.trim();
        performSearch();
    });

    countrySelect.addEventListener("change", (e) => {
        STATE.destinationCountry = e.target.value;
        // Auto select country currency
        const map = { SA: "SAR", AE: "AED", US: "USD", GB: "GBP", DE: "EUR", JP: "JPY", CA: "CAD", KW: "KWD", QA: "QAR" };
        if (map[STATE.destinationCountry]) {
            STATE.currency = map[STATE.destinationCountry];
            currencySelect.value = STATE.currency;
        }
        performSearch();
    });

    currencySelect.addEventListener("change", (e) => {
        STATE.currency = e.target.value;
        performSearch();
    });

    // Search Mode radio buttons (Auto, Part Number Exact, Keyword & Synonyms)
    document.querySelectorAll("input[name=searchMode]").forEach(radio => {
        radio.addEventListener("change", (e) => {
            STATE.searchMode = e.target.value;
            performSearch();
        });
    });

    // Checkboxes in sidebar
    document.querySelectorAll("input[type=checkbox]").forEach(box => {
        box.addEventListener("change", handleFilterChange);
    });

    // Quick chips
    document.querySelectorAll(".quick-chip").forEach(chip => {
        chip.addEventListener("click", () => {
            const q = chip.getAttribute("data-query");
            searchInput.value = q;
            STATE.query = q;
            performSearch();
        });
    });

    // Vehicle Garage Locking
    applyVehicleBtn.addEventListener("click", () => {
        STATE.vehicle.year = garageYear.value ? parseInt(garageYear.value) : null;
        STATE.vehicle.make = garageMake.value || null;
        STATE.vehicle.model = garageModel.value || null;
        updateGarageUI();
        performSearch();
    });

    clearVehicleBtn.addEventListener("click", () => {
        STATE.vehicle = { year: null, make: null, model: null, vin: null };
        garageYear.value = "";
        garageMake.value = "";
        garageModel.value = "";
        updateGarageUI();
        performSearch();
    });

    // VIN Modal events
    openVinModalBtn.addEventListener("click", () => {
        vinModal.classList.remove("hidden");
        vinInput.focus();
    });

    closeVinModalBtn.addEventListener("click", () => {
        vinModal.classList.add("hidden");
    });

    decodeVinBtn.addEventListener("click", async () => {
        const vin = vinInput.value.trim();
        if (vin.length !== 17) {
            alert("Please enter a valid 17-character VIN");
            return;
        }
        try {
            const res = await fetch(`/api/vin/${vin}`);
            const data = await res.json();
            if (data.is_valid_format) {
                vinResultCard.classList.remove("hidden");
                vinMakeVal.textContent = data.make;
                vinYearVal.textContent = data.model_year;
                vinCountryVal.textContent = data.country_of_manufacture;
                vinWmiVal.textContent = data.wmi;

                // Update state and garage
                STATE.vehicle.make = data.make;
                STATE.vehicle.year = data.model_year;
                STATE.vehicle.vin = data.vin;
                if (garageMake.querySelector(`option[value="${data.make}"]`)) {
                    garageMake.value = data.make;
                }
                garageYear.value = data.model_year;
                updateGarageUI();
                setTimeout(() => {
                    vinModal.classList.add("hidden");
                    performSearch();
                }, 1000);
            } else {
                alert("Could not decode VIN format");
            }
        } catch (err) {
            console.error(err);
        }
    });

    resetFiltersBtn.addEventListener("click", () => {
        document.querySelectorAll("input[type=checkbox]").forEach(box => box.checked = false);
        STATE.filters = {
            listing_types: [],
            conditions: [],
            authenticity_tiers: [],
            sources: [],
            only_direct_shipping: false,
            exclude_hazmat: false
        };
        performSearch();
    });
}

function handleFilterChange() {
    STATE.filters.listing_types = Array.from(document.querySelectorAll("input[name=listing_type]:checked")).map(b => b.value);
    STATE.filters.conditions = Array.from(document.querySelectorAll("input[name=condition]:checked")).map(b => b.value);
    STATE.filters.authenticity_tiers = Array.from(document.querySelectorAll("input[name=tier]:checked")).map(b => b.value);
    STATE.filters.sources = Array.from(document.querySelectorAll("input[name=source]:checked")).map(b => b.value);
    STATE.filters.only_direct_shipping = document.getElementById("onlyDirectShipping").checked;
    STATE.filters.exclude_hazmat = document.getElementById("excludeHazmat").checked;

    performSearch();
}

function updateGarageUI() {
    if (STATE.vehicle.make || STATE.vehicle.model || STATE.vehicle.year) {
        const text = `${STATE.vehicle.year || ""} ${STATE.vehicle.make || ""} ${STATE.vehicle.model || ""}`.trim();
        activeVehicleLabel.textContent = `Locked: ${text}`;
        activeVehicleBadge.classList.remove("bg-slate-800", "text-slate-200");
        activeVehicleBadge.classList.add("bg-emerald-950/60", "text-emerald-300", "border-emerald-700");
        clearVehicleBtn.classList.remove("hidden");
    } else {
        activeVehicleLabel.textContent = "Select a vehicle to verify fitment";
        activeVehicleBadge.classList.remove("bg-emerald-950/60", "text-emerald-300", "border-emerald-700");
        activeVehicleBadge.classList.add("bg-slate-800", "text-slate-200");
        clearVehicleBtn.classList.add("hidden");
    }
}

// --- Search Dispatcher ---
async function performSearch() {
    clearActiveTimers();
    listingsContainer.innerHTML = `<div class="p-12 text-center text-slate-400"><div class="inline-block w-8 h-8 border-4 border-orange-500 border-t-transparent rounded-full animate-spin mb-3"></div><p class="text-sm">Querying global platforms and calculating landed costs...</p></div>`;

    const payload = {
        query: STATE.query,
        country: STATE.destinationCountry,
        currency: STATE.currency,
        filters: STATE.filters,
        garage: STATE.vehicle
    };

    // Construct query URL
    const params = new URLSearchParams();
    if (STATE.query) params.append("q", STATE.query);
    params.append("country", STATE.destinationCountry);
    if (STATE.currency) params.append("currency", STATE.currency);
    const selectedMode = document.querySelector("input[name=searchMode]:checked")?.value || STATE.searchMode || "auto";
    params.append("mode", selectedMode);
    STATE.filters.listing_types.forEach(lt => params.append("listing_type", lt));
    STATE.filters.conditions.forEach(c => params.append("condition", c));
    STATE.filters.authenticity_tiers.forEach(t => params.append("tier", t));
    STATE.filters.sources.forEach(s => params.append("source", s));
    if (STATE.filters.exclude_hazmat) params.append("exclude_hazmat", "true");
    if (STATE.vehicle.year) params.append("year", STATE.vehicle.year);
    if (STATE.vehicle.make) params.append("make", STATE.vehicle.make);
    if (STATE.vehicle.model) params.append("model", STATE.vehicle.model);

    try {
        const response = await fetch(`/api/search?${params.toString()}`);
        const data = await response.json();
        renderResults(data);
    } catch (err) {
        console.error("Search failed:", err);
        listingsContainer.innerHTML = `<div class="p-8 text-center text-red-400 bg-red-950/20 rounded-xl border border-red-900"><p>Failed to retrieve data from Banshari engine.</p></div>`;
    }
}

// --- Results Rendering ---
function renderResults(data) {
    const { results, query_meta, total_matches, facets, selected_currency, destination_country } = data;

    // Update query pill
    queryStatusPill.classList.remove("hidden");
    queryStatusMode.textContent = query_meta.detected_mode.toUpperCase();

    // Show / Hide interchange alert
    if (query_meta.detected_mode === "part_number" && query_meta.cleaned_part_number) {
        interchangeBanner.classList.remove("hidden");
    } else {
        interchangeBanner.classList.add("hidden");
    }

    // Update counts
    resultsCountBadge.textContent = `${results.length} of ${total_matches} matches`;
    resultsTitle.textContent = query_meta.raw_query ? `Results for "${query_meta.raw_query}"` : "Global Automotive Spare Parts Catalog";

    // Update Facet counts in sidebar
    updateFacetCounts(facets);

    if (results.length === 0) {
        listingsContainer.innerHTML = "";
        emptyState.classList.remove("hidden");
        return;
    }

    emptyState.classList.add("hidden");
    listingsContainer.innerHTML = "";

    results.forEach((item, index) => {
        const card = createPartCard(item, selected_currency, destination_country, index);
        listingsContainer.appendChild(card);
    });

    if (window.lucide) {
        lucide.createIcons();
    }
}

function updateFacetCounts(facets) {
    const mapping = {
        buy_now: "count-buy_now",
        auction: "count-auction",
        new_factory_sealed: "count-new_factory_sealed",
        used_grade_a: "count-used_grade_a",
        used_grade_b: "count-used_grade_b",
        oem_genuine: "count-oem_genuine",
        oes_tier1: "count-oes_tier1",
        aftermarket_performance: "count-aftermarket_performance",
        "eBay Motors": "count-ebay_motors",
        "RockAuto": "count-rockauto",
        "Partsouq": "count-partsouq",
        "AutoDoc": "count-autodoc",
        "Yahoo! Auctions Japan": "count-yahoo_japan",
        "Car-Part.com": "count-car_part",
        "FCP Euro": "count-fcpeuro",
        "ECS Tuning": "count-ecstuning",
        "Summit Racing": "count-summit",
        "Allegro": "count-allegro",
        "B-Parts": "count-bparts",
        "Amayama": "count-amayama",
        "Up Garage": "count-upgarage",
        "Croooober": "count-upgarage",
        "Megazip": "count-megazip"
    };

    // Reset all to 0
    Object.values(mapping).forEach(id => {
        const el = document.getElementById(id);
        if (el) el.textContent = "0";
    });

    // Fill counts from response
    [...facets.listing_types, ...facets.conditions, ...facets.authenticity_tiers, ...facets.sources].forEach(f => {
        const targetId = mapping[f.key];
        if (targetId) {
            const el = document.getElementById(targetId);
            if (el) el.textContent = f.count;
        }
    });
}

function createPartCard(itemEnriched, currency, userCountry, index) {
    const { listing, landed_cost, fitment_verified, fitment_notes } = itemEnriched;
    const isAuction = listing.listing_type === "auction";

    const card = document.createElement("div");
    card.className = "part-card bg-slate-900 border border-slate-800 rounded-2xl p-5 overflow-hidden relative shadow-lg";

    // Badges logic
    const isOEM = listing.authenticity_tier === "oem_genuine";
    const tierBadge = isOEM 
        ? `<span class="bg-amber-500/20 text-amber-300 border border-amber-500/30 text-[11px] font-bold px-2 py-0.5 rounded flex items-center gap-1"><i data-lucide="shield-check" class="w-3 h-3"></i> OEM Genuine</span>`
        : `<span class="bg-blue-500/20 text-blue-300 border border-blue-500/30 text-[11px] font-medium px-2 py-0.5 rounded flex items-center gap-1"><i data-lucide="wrench" class="w-3 h-3"></i> ${formatLabel(listing.authenticity_tier)}</span>`;

    const isNew = listing.condition.includes("new");
    const conditionBadge = isNew
        ? `<span class="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[11px] font-medium px-2 py-0.5 rounded">New Condition</span>`
        : `<span class="bg-slate-700 text-slate-300 text-[11px] font-medium px-2 py-0.5 rounded">Used / Salvage</span>`;

    const formatBadge = isAuction
        ? `<span class="bg-red-500/20 text-red-300 border border-red-500/30 text-[11px] font-bold px-2 py-0.5 rounded flex items-center gap-1"><i data-lucide="gavel" class="w-3 h-3"></i> Live Auction</span>`
        : `<span class="bg-slate-800 text-slate-300 text-[11px] font-medium px-2 py-0.5 rounded flex items-center gap-1"><i data-lucide="tag" class="w-3 h-3"></i> Buy It Now</span>`;

    const fitmentBadge = fitment_verified
        ? `<div class="bg-emerald-950/80 border border-emerald-700/80 text-emerald-300 text-[11px] px-2.5 py-1 rounded-md flex items-center gap-1.5 mt-2 font-medium">
             <i data-lucide="check" class="w-3.5 h-3.5 text-emerald-400"></i>
             <span>${fitment_notes || "Verified fit for your locked vehicle"}</span>
           </div>`
        : "";

    // Hazmat warning badge
    const hazmatBadge = landed_cost.hazmat_warning
        ? `<div class="bg-rose-950/70 border border-rose-800/80 text-rose-300 text-[11px] px-2.5 py-1.5 rounded-md flex items-start gap-1.5 mt-2">
             <i data-lucide="alert-triangle" class="w-3.5 h-3.5 text-rose-400 shrink-0 mt-0.5"></i>
             <div><span class="font-bold">Dangerous Goods Alert:</span> ${landed_cost.hazmat_warning}</div>
           </div>`
        : "";

    // Timer markup for auctions
    const timerId = `auction-timer-${index}`;
    const timerMarkup = isAuction
        ? `<div class="text-xs bg-slate-800/90 border border-slate-700 px-2.5 py-1.5 rounded-lg flex items-center gap-2 text-amber-400 font-mono mt-2">
             <i data-lucide="clock" class="w-3.5 h-3.5 text-amber-400"></i>
             <span class="text-slate-400">Ends in:</span>
             <span id="${timerId}" class="font-bold">Calculating...</span>
             <span class="text-slate-500 font-sans text-[11px]">(${listing.bid_count || 1} bids)</span>
           </div>`
        : "";

    // Start timer interval if auction
    if (isAuction && listing.auction_end_time) {
        startCountdown(timerId, listing.auction_end_time);
    }

    // Interchange pill badges
    const interchangesHtml = listing.interchange_part_numbers.length > 0
        ? `<div class="mt-2 text-[11px] text-slate-400 flex flex-wrap items-center gap-1">
             <span class="text-slate-500">Cross-Ref Interchange:</span>
             ${listing.interchange_part_numbers.slice(0, 4).map(ic => `<span class="bg-slate-800 px-1.5 py-0.5 rounded border border-slate-700 text-slate-300 font-mono">${ic}</span>`).join("")}
           </div>`
        : "";

    // ACES details summary
    const fitmentSummary = listing.aces_fitments.length > 0 
        ? `${listing.aces_fitments[0].year_start}-${listing.aces_fitments[0].year_end} ${listing.aces_fitments[0].make_name} ${listing.aces_fitments[0].model_name} (${listing.aces_fitments[0].pcdb_position})`
        : "Universal / Multi-Fit";

    // Accordion ID for landed cost
    const drawerId = `landed-drawer-${index}`;

    card.innerHTML = `
        <div class="flex flex-col md:flex-row gap-5">
            <!-- Left: Thumbnail Image & Source Tag -->
            <div class="w-full md:w-52 h-48 md:h-auto shrink-0 relative rounded-xl overflow-hidden bg-slate-950 border border-slate-800 group">
                <a href="${listing.source_url}" target="_blank" rel="noopener noreferrer" class="block w-full h-full cursor-pointer">
                    <img src="${listing.primary_image_url}" alt="${listing.title}" class="w-full h-full object-cover group-hover:scale-105 transition duration-300">
                </a>
                <div class="absolute top-2 left-2 bg-slate-900/90 backdrop-blur-sm border border-slate-700 px-2 py-0.5 rounded text-[10px] font-bold text-slate-200">
                    ${listing.source_platform}
                </div>
                <div class="absolute bottom-2 left-2 right-2 bg-slate-950/80 backdrop-blur-sm px-2 py-1 rounded text-[10px] text-slate-300 flex justify-between">
                    <span>Seller: ${listing.seller_name}</span>
                    <span class="text-amber-400">★ ${listing.seller_rating}</span>
                </div>
            </div>

            <!-- Middle: Title, Part Number, Classification & Compliance -->
            <div class="flex-1 min-w-0">
                <div class="flex flex-wrap items-center gap-1.5 mb-1.5">
                    ${formatBadge}
                    ${tierBadge}
                    ${conditionBadge}
                </div>

                <h2 class="text-base font-bold text-white hover:text-orange-400 transition leading-snug">
                    <a href="${listing.source_url}" target="_blank" rel="noopener noreferrer">${listing.title}</a>
                </h2>

                <div class="mt-1 flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-slate-400 font-mono">
                    <div>Brand: <span class="text-slate-200 font-semibold font-sans">${listing.brand}</span></div>
                    <div>MPN: <span class="text-orange-400 font-bold">${listing.manufacturer_part_number}</span></div>
                    <div>HS Code: <span class="text-slate-300">${listing.shipping.hs_code}</span></div>
                    <div>Weight: <span class="text-slate-300">${listing.pies_attributes.weight_kg} kg</span></div>
                </div>

                <div class="mt-2 text-xs text-slate-400">
                    <span class="text-slate-500 font-semibold">ACES 5.0 Fitment:</span>
                    <span class="text-slate-300">${fitmentSummary}</span>
                </div>

                ${interchangesHtml}
                ${fitmentBadge}
                ${hazmatBadge}
                ${timerMarkup}
            </div>

            <!-- Right: Pricing & Landed Cost Breakdown -->
            <div class="w-full md:w-64 shrink-0 flex flex-col justify-between border-t md:border-t-0 md:border-l border-slate-800 pt-4 md:pt-0 md:pl-5">
                <div>
                    <div class="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">
                        ${isAuction ? "Current Bid" : "Item Price"}
                    </div>
                    <div class="flex items-baseline gap-2">
                        <span class="text-2xl font-black text-white font-mono">
                            $${isAuction ? listing.current_bid.toFixed(2) : listing.buy_now_price.toFixed(2)}
                        </span>
                        <span class="text-xs text-slate-500 font-mono">USD</span>
                    </div>

                    <!-- Landed Cost Summary to User Country -->
                    <div class="mt-3 bg-slate-800/70 border border-slate-700/80 rounded-xl p-3">
                        <div class="flex items-center justify-between text-xs">
                            <span class="text-slate-400">Est. Total Landed Cost:</span>
                            <span class="font-black text-orange-400 font-mono text-sm">
                                ${landed_cost.local_currency_code} ${landed_cost.total_landed_cost_local.toLocaleString()}
                            </span>
                        </div>
                        <div class="text-[10px] text-slate-500 mt-0.5">
                            Delivered to <strong>${userCountry}</strong> (Item + Duty + VAT + Freight)
                        </div>

                        <!-- Toggle breakdown drawer -->
                        <button onclick="toggleLandedDrawer('${drawerId}')" class="mt-2 text-[11px] text-orange-400 hover:text-orange-300 flex items-center gap-1 font-medium focus:outline-none">
                            <span>Duty & Freight Breakdown</span>
                            <i data-lucide="chevron-down" class="w-3.5 h-3.5"></i>
                        </button>

                        <div id="${drawerId}" class="hidden mt-2 pt-2 border-t border-slate-700 space-y-1 text-[11px] text-slate-300 font-mono">
                            <div class="flex justify-between">
                                <span class="text-slate-400">Intl Shipping:</span>
                                <span>$${landed_cost.shipping_usd.toFixed(2)}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-slate-400">Customs Duty (${landed_cost.duty_rate_percent}%):</span>
                                <span>$${landed_cost.customs_duty_usd.toFixed(2)}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-slate-400">Import VAT/Tax (${landed_cost.tax_vat_percent}%):</span>
                                <span>$${landed_cost.tax_vat_usd.toFixed(2)}</span>
                            </div>
                            <div class="flex justify-between pt-1 border-t border-slate-700 font-bold text-white">
                                <span>Total (USD):</span>
                                <span>$${landed_cost.total_landed_cost_usd.toFixed(2)}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- CTA Action Button -->
                <div class="mt-4">
                    <a
                        href="${listing.source_url}"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl font-bold text-xs uppercase tracking-wider text-white transition shadow-lg ${
                            isAuction 
                                ? "bg-amber-600 hover:bg-amber-500 shadow-amber-600/30" 
                                : "bg-orange-600 hover:bg-orange-500 shadow-orange-600/30"
                        }"
                    >
                        <span>${isAuction ? "Place Bid on " + listing.source_platform : "Buy Now on " + listing.source_platform}</span>
                        <i data-lucide="external-link" class="w-3.5 h-3.5"></i>
                    </a>
                </div>
            </div>
        </div>
    `;

    return card;
}

// --- Live Countdown Timer Helper ---
function startCountdown(elementId, targetIso) {
    const targetDate = new Date(targetIso).getTime();

    function update() {
        const el = document.getElementById(elementId);
        if (!el) return;

        const now = new Date().getTime();
        const diff = targetDate - now;

        if (diff <= 0) {
            el.textContent = "Auction Ended";
            el.classList.add("text-rose-500");
            return;
        }

        const hours = Math.floor(diff / (1000 * 60 * 60));
        const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const secs = Math.floor((diff % (1000 * 60)) / 1000);

        el.textContent = `${hours}h ${mins}m ${secs}s`;
    }

    update();
    const interval = setInterval(update, 1000);
    STATE.timerIntervals.push(interval);
}

function clearActiveTimers() {
    STATE.timerIntervals.forEach(clearInterval);
    STATE.timerIntervals = [];
}

// --- Drawer Toggle ---
window.toggleLandedDrawer = function(id) {
    const el = document.getElementById(id);
    if (el) {
        el.classList.toggle("hidden");
    }
};

function formatLabel(val) {
    if (!val) return "";
    return val.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase());
}
