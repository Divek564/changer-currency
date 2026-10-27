
import streamlit as st
import requests

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Live Currency Converter",
    page_icon="💱",
    layout="wide"
)

# ---------- SESSION STATE ----------
if "from_currency" not in st.session_state:
    st.session_state.from_currency = "USD"

if "to_currency" not in st.session_state:
    st.session_state.to_currency = "EUR"

if "refresh_key" not in st.session_state:
    st.session_state.refresh_key = 0


# ---------- CSS ----------
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(ellipse at 100% 30%,
        rgba(105,25,115,0.48), transparent 38%),
        radial-gradient(ellipse at 0% 75%,
        rgba(90,20,100,0.45), transparent 38%),
        #08080d;
    color: white;
}

.block-container {
    max-width: 900px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

header[data-testid="stHeader"] {
    background: transparent;
}

/* Header */
.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 24px;
}

.brand {
    font-size: 27px;
    font-weight: 700;
    color: white;
    letter-spacing: -0.6px;
}

.header-tag {
    background: #1c1c2b;
    border: 1px solid #302f40;
    border-radius: 15px;
    padding: 13px 20px;
    color: #c9c9df;
    font-size: 14px;
    white-space: nowrap;
}

/* Exchange Banner */
.exchange-banner {
    width: 100%;
    padding: 19px 24px;
    margin: 0 0 8px 0;
    border-radius: 24px;
    background: linear-gradient(110deg,#1e1e2d,#17131f);
    border: 1px solid #353343;
    box-sizing: border-box;
}

.banner-title {
    font-size: 20px;
    font-weight: 650;
    color: white;
}

.banner-subtitle {
    font-size: 13px;
    color: #a5a6b5;
    margin-top: 6px;
}

/* Dropdown */
div[data-baseweb="select"] > div {
    background: #1c1c29;
    border: 1px solid #353544;
    border-radius: 12px;
    min-height: 48px;
}

/* Amount Input */
div[data-testid="stNumberInput"] input {
    background: #22222e;
    color: white;
    border-radius: 10px;
}

div[data-testid="stNumberInput"] button {
    background: #22222e;
    color: white;
}

/* Buttons */
.stButton > button {
    min-height: 48px;
    border-radius: 12px;
    border: 1px solid #373746;
    background: #1c1c29;
    color: white;
    transition: 0.2s;
}

.stButton > button:hover {
    border-color: #a78bfa;
    color: #d8caff;
    background: #262337;
}

/* Result Card */
.result-card {
    background: rgba(10,10,16,0.85);
    border: 1px solid #302c3b;
    border-radius: 25px;
    padding: 38px 20px 26px;
    text-align: center;
    margin-top: 34px;
}

.result-amount {
    font-size: clamp(34px,5vw,52px);
    font-weight: 750;
    color: white;
    letter-spacing: -1.5px;
    overflow-wrap: anywhere;
}

.result-caption {
    color: #b5b5c9;
    font-size: 14px;
    margin-top: 17px;
}

.rate-divider {
    border-top: 1px solid #302c3b;
    margin-top: 24px;
    padding-top: 20px;
    color: #dddde9;
    font-size: 14px;
}

.rate-date {
    color: #9c9ca9;
    font-size: 12px;
    margin-top: 8px;
}

/* Responsive */
@media(max-width:600px) {
    .brand {
        font-size: 20px;
    }

    .header-tag {
        font-size: 12px;
        padding: 10px 12px;
    }

    .exchange-banner {
        padding: 17px;
    }

    .result-card {
        padding: 28px 12px;
    }
}
</style>
""", unsafe_allow_html=True)


# ---------- HEADER ----------
st.markdown("""
<div class="header">
<div class="brand">💱 &nbsp; Live Currency Converter</div>
<div class="header-tag">Currencies</div>
</div>
""", unsafe_allow_html=True)


# ---------- EXCHANGE BANNER ----------
st.markdown("""
<div class="exchange-banner">
<div class="banner-title">⇄ &nbsp; Global Currency Exchange</div>
<div class="banner-subtitle">Convert currencies instantly with live exchange rates.</div>
</div>
""", unsafe_allow_html=True)


# ---------- CURRENCY DATA ----------
currencies = {
    "USD": "🇺🇸 US Dollar",
    "EUR": "🇪🇺 Euro",
    "INR": "🇮🇳 Indian Rupee",
    "GBP": "🇬🇧 British Pound",
    "JPY": "🇯🇵 Japanese Yen",
    "AUD": "🇦🇺 Australian Dollar",
    "CAD": "🇨🇦 Canadian Dollar",
    "CHF": "🇨🇭 Swiss Franc",
    "CNY": "🇨🇳 Chinese Yuan",
    "AED": "🇦🇪 UAE Dirham",
    "SGD": "🇸🇬 Singapore Dollar",
    "NZD": "🇳🇿 New Zealand Dollar",
    "SAR": "🇸🇦 Saudi Riyal",
    "BDT": "🇧🇩 Bangladeshi Taka",
    "PKR": "🇵🇰 Pakistani Rupee",
    "NPR": "🇳🇵 Nepalese Rupee",
    "ZAR": "🇿🇦 South African Rand",
    "THB": "🇹🇭 Thai Baht",
    "KRW": "🇰🇷 South Korean Won",
    "HKD": "🇭🇰 Hong Kong Dollar"
}

currency_codes = list(currencies.keys())


# ---------- SWAP ----------
def swap_currency():
    old_from = st.session_state.from_currency
    old_to = st.session_state.to_currency

    st.session_state.from_currency = old_to
    st.session_state.to_currency = old_from


# ---------- AMOUNT ----------
# Amount is placed directly below the banner
amount = st.number_input(
    "Amount",
    min_value=0.0,
    value=100.0,
    step=10.0,
    key="amount",
    format="%.2f"
)


# ---------- CURRENCY SELECTORS ----------
col1, col2, col3 = st.columns([5, 0.8, 5])

with col1:
    st.selectbox(
        "From",
        currency_codes,
        format_func=lambda x: currencies[x],
        key="from_currency"
    )

with col2:
    st.markdown(
        "<div style='height:26px'></div>",
        unsafe_allow_html=True
    )

    st.button(
        "⇄",
        key="swap",
        use_container_width=True,
        on_click=swap_currency
    )

with col3:
    st.selectbox(
        "To",
        currency_codes,
        format_func=lambda x: currencies[x],
        key="to_currency"
    )


# ---------- REFRESH ----------
def refresh_rates():
    st.session_state.refresh_key += 1


st.button(
    "↻ Refresh Live Rates",
    use_container_width=True,
    on_click=refresh_rates
)


# ---------- CURRENCY SYMBOLS ----------
symbols = {
    "USD": "$",
    "EUR": "€",
    "INR": "₹",
    "GBP": "£",
    "JPY": "¥",
    "AUD": "A$",
    "CAD": "C$",
    "CHF": "CHF ",
    "CNY": "¥",
    "AED": "د.إ ",
    "SGD": "S$",
    "NZD": "NZ$",
    "SAR": "﷼ ",
    "BDT": "৳",
    "PKR": "Rs ",
    "NPR": "रू ",
    "ZAR": "R ",
    "THB": "฿",
    "KRW": "₩",
    "HKD": "HK$"
}


# ---------- FETCH EXCHANGE RATES ----------
@st.cache_data(ttl=300)
def get_exchange_rates(base):
    url = f"https://open.er-api.com/v6/latest/{base}"

    response = requests.get(url, timeout=15)
    response.raise_for_status()

    data = response.json()

    if data.get("result") != "success":
        raise ValueError("Exchange rates unavailable.")

    return data


# ---------- FORCE REFRESH ----------
if st.session_state.refresh_key > 0:
    get_exchange_rates.clear()
    st.session_state.refresh_key = 0


# ---------- CONVERSION ----------
base = st.session_state.from_currency
target = st.session_state.to_currency

try:
    data = get_exchange_rates(base)

    rate = data["rates"][target]
    converted_amount = amount * rate

    from_symbol = symbols.get(base, base + " ")
    to_symbol = symbols.get(target, target + " ")

    rate_date = data.get(
        "time_last_update_utc",
        "Latest available rate"
    )

    # ---------- RESULT CARD ----------
    result_html = f"""
<div class="result-card">
<div class="result-amount">{to_symbol}{converted_amount:,.2f}</div>
<div class="result-caption">{from_symbol}{amount:,.2f} {base} &nbsp; → &nbsp; {target}</div>
<div class="rate-divider">1 {base} = <b>{rate:.4f} {target}</b></div>
</div>
<div class="rate-date">Rate updated: {rate_date}</div>
"""

    st.markdown(result_html, unsafe_allow_html=True)

except Exception:
    st.error(
        "Unable to fetch exchange rates. "
        "Please check your internet connection and try again."
    )
