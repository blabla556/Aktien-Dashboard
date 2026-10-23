import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import requests
import json
import base64
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. SEITENKONFIGURATION ---
st.set_page_config(page_title="Depot & Aktien-Analyse Dashboard", layout="wide", page_icon="📈")

# --- 2. HINTERLEGTES BASIS-DEPOT (46 POSITIONEN) ---
DEFAULT_PORTFOLIO = {
    "--- Freie Suche über Eingabefeld nutzen ---": {"ticker": "", "shares": 0, "wkn": "", "cluster": ""},
    "AbbVie Inc.": {"ticker": "ABBV", "shares": 1, "wkn": "A1J84E", "cluster": "Gesundheit / Pharma"},
    "Airbus SE": {"ticker": "AIR.DE", "shares": 3, "wkn": "938914", "cluster": "Industrie & Luftfahrt"},
    "Allianz SE": {"ticker": "ALV.DE", "shares": 3, "wkn": "840400", "cluster": "Finanzen & Versicherungen"},
    "Alphabet Inc. Class A": {"ticker": "GOOGL", "shares": 8, "wkn": "A14Y6F", "cluster": "Technologie, Halbleiter & KI"},
    "Amazon.com Inc.": {"ticker": "AMZN", "shares": 14, "wkn": "906866", "cluster": "Konsum & E-Commerce"},
    "AMETEK Inc.": {"ticker": "AME", "shares": 1, "wkn": "908668", "cluster": "Industrie & Luftfahrt"},
    "Amphenol Corp.": {"ticker": "APH", "shares": 10, "wkn": "882749", "cluster": "Technologie, Halbleiter & KI"},
    "Broadcom Inc.": {"ticker": "AVGO", "shares": 2, "wkn": "A2JG9Z", "cluster": "Technologie, Halbleiter & KI"},
    "China Shenhua Energy": {"ticker": "1088.HK", "shares": 97, "wkn": "A0M4XP", "cluster": "Energie & Netzausbau"},
    "Coherent Corp.": {"ticker": "COHR", "shares": 12, "wkn": "877619", "cluster": "Technologie, Halbleiter & KI"},
    "Comfort Systems USA": {"ticker": "FIX", "shares": 1, "wkn": "908440", "cluster": "Industrie & Luftfahrt"},
    "Constellation Energy": {"ticker": "CEG", "shares": 3, "wkn": "A3DCXB", "cluster": "Energie & Netzausbau"},
    "D-Wave Quantum Inc.": {"ticker": "QBTS", "shares": 54, "wkn": "A3DSV9", "cluster": "Technologie, Halbleiter & KI"},
    "Daimler Truck Holding": {"ticker": "DTG.DE", "shares": 28, "wkn": "DTR0CK", "cluster": "Industrie & Luftfahrt"},
    "Deutsche Bank AG": {"ticker": "DBK.DE", "shares": 21, "wkn": "514000", "cluster": "Finanzen & Versicherungen"},
    "Deutsche Börse AG": {"ticker": "DB1.DE", "shares": 14, "wkn": "581005", "cluster": "Finanzen & Versicherungen"},
    "GE Vernova Inc.": {"ticker": "GEV", "shares": 5, "wkn": "A404PC", "cluster": "Energie & Netzausbau"},
    "GE Aerospace": {"ticker": "GE", "shares": 1, "wkn": "A3CSML", "cluster": "Industrie & Luftfahrt"},
    "General Mills Inc.": {"ticker": "GIS", "shares": 36, "wkn": "853862", "cluster": "Basiskonsum & REITs"},
    "Goldman Sachs Group": {"ticker": "GS", "shares": 1, "wkn": "920332", "cluster": "Finanzen & Versicherungen"},
    "IBM Corp.": {"ticker": "IBM", "shares": 11, "wkn": "851399", "cluster": "Technologie, Halbleiter & KI"},
    "ING Groep N.V.": {"ticker": "INGA.AS", "shares": 35, "wkn": "A2ANV3", "cluster": "Finanzen & Versicherungen"},
    "Jungheinrich AG Vz.": {"ticker": "JUN3.DE", "shares": 130, "wkn": "621993", "cluster": "Industrie & Luftfahrt"},
    "KLA Corporation": {"ticker": "KLAC", "shares": 10, "wkn": "865884", "cluster": "Technologie, Halbleiter & KI"},
    "Linde plc": {"ticker": "LIN", "shares": 4, "wkn": "A3D7VW", "cluster": "Industrie & Luftfahrt"},
    "Main Street Capital": {"ticker": "MAIN", "shares": 8, "wkn": "A0X8Y3", "cluster": "Finanzen & Versicherungen"},
    "Marvell Technology": {"ticker": "MRVL", "shares": 6, "wkn": "A3CNLD", "cluster": "Technologie, Halbleiter & KI"},
    "Merck & Co. Inc.": {"ticker": "MRK", "shares": 1, "wkn": "A0YD8Q", "cluster": "Gesundheit / Pharma"},
    "Microsoft Corp.": {"ticker": "MSFT", "shares": 28, "wkn": "870747", "cluster": "Technologie, Halbleiter & KI"},
    "MTU Aero Engines AG": {"ticker": "MTX.DE", "shares": 1, "wkn": "A0D9PT", "cluster": "Industrie & Luftfahrt"},
    "Münchener Rück": {"ticker": "MUV2.DE", "shares": 2, "wkn": "843002", "cluster": "Finanzen & Versicherungen"},
    "NVIDIA Corp.": {"ticker": "NVDA", "shares": 6, "wkn": "918422", "cluster": "Technologie, Halbleiter & KI"},
    "Oracle Corp.": {"ticker": "ORCL", "shares": 6, "wkn": "871460", "cluster": "Technologie, Halbleiter & KI"},
    "Palantir Technologies": {"ticker": "PLTR", "shares": 6, "wkn": "A2QA4J", "cluster": "Technologie, Halbleiter & KI"},
    "Palo Alto Networks": {"ticker": "PANW", "shares": 3, "wkn": "A1JZ0Q", "cluster": "Technologie, Halbleiter & KI"},
    "PFISTERER Holding SE": {"ticker": "PFS0.DE", "shares": 22, "wkn": "PFSE25", "cluster": "Energie & Netzausbau"},
    "Procter & Gamble Co.": {"ticker": "PG", "shares": 1, "wkn": "852062", "cluster": "Basiskonsum & REITs"},
    "Prysmian S.p.A.": {"ticker": "PRY.MI", "shares": 11, "wkn": "A0MP84", "cluster": "Energie & Netzausbau"},
    "Realty Income Corp.": {"ticker": "O", "shares": 12, "wkn": "899744", "cluster": "Basiskonsum & REITs"},
    "Rolls-Royce Holdings": {"ticker": "RR.L", "shares": 81, "wkn": "A1H81L", "cluster": "Industrie & Luftfahrt"},
    "SAP SE": {"ticker": "SAP.DE", "shares": 18, "wkn": "716460", "cluster": "Technologie, Halbleiter & KI"},
    "Siemens Energy AG": {"ticker": "ENR.DE", "shares": 39, "wkn": "ENER6Y", "cluster": "Energie & Netzausbau"},
    "UniCredit S.p.A.": {"ticker": "UCG.MI", "shares": 19, "wkn": "A2DJV6", "cluster": "Finanzen & Versicherungen"},
    "Waste Management Inc.": {"ticker": "WM", "shares": 1, "wkn": "893579", "cluster": "Industrie & Luftfahrt"},
    "Xiaomi Corp.": {"ticker": "1810.HK", "shares": 520, "wkn": "A2JNY1", "cluster": "Technologie, Halbleiter & KI"},
    "XPeng Inc.": {"ticker": "XPEV", "shares": 39, "wkn": "A2QBX7", "cluster": "Konsum & E-Commerce"}
}

DEFAULT_WATCHLIST = {
    "Quanta Services Inc.": {"ticker": "PWR", "wkn": "911688"},
    "ASML Holding N.V.": {"ticker": "ASML.AS", "wkn": "A1J4U4"}
}

DATA_FILE = "user_data.json"

# --- 3. PERSISTENZ-ENGINE (LOKAL & GITHUB API) + E-MAIL ALARME ---
def load_user_data():
    default_data = {
        "shares": {k: v["shares"] for k, v in DEFAULT_PORTFOLIO.items() if v["ticker"]},
        "watchlist": DEFAULT_WATCHLIST,
        "alerts": {}
    }
    try:
        if "GITHUB_TOKEN" in st.secrets and "GITHUB_REPO" in st.secrets:
            token = st.secrets["GITHUB_TOKEN"]
            repo = st.secrets["GITHUB_REPO"]
            url = f"https://api.github.com/repos/{repo}/contents/{DATA_FILE}"
            headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
            r = requests.get(url, headers=headers, timeout=5)
            if r.status_code == 200:
                content = base64.b64decode(r.json()["content"]).decode("utf-8")
                loaded = json.loads(content)
                for k in default_data["shares"]:
                    if k not in loaded.get("shares", {}):
                        loaded.setdefault("shares", {})[k] = default_data["shares"][k]
                return loaded
    except Exception:
        pass

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                for k in default_data["shares"]:
                    if k not in loaded.get("shares", {}):
                        loaded.setdefault("shares", {})[k] = default_data["shares"][k]
                return loaded
        except Exception:
            pass
    return default_data

def save_user_data(data_dict):
    json_str = json.dumps(data_dict, indent=2, ensure_ascii=False)
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            f.write(json_str)
    except Exception:
        pass

    try:
        if "GITHUB_TOKEN" in st.secrets and "GITHUB_REPO" in st.secrets:
            token = st.secrets["GITHUB_TOKEN"]
            repo = st.secrets["GITHUB_REPO"]
            url = f"https://api.github.com/repos/{repo}/contents/{DATA_FILE}"
            headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
            r = requests.get(url, headers=headers, timeout=5)
            sha = None
            if r.status_code == 200:
                sha = r.json().get("sha")

            payload = {
                "message": "Update user_data.json via Streamlit Dashboard",
                "content": base64.b64encode(json_str.encode("utf-8")).decode("utf-8")
            }
            if sha:
                payload["sha"] = sha
            put_r = requests.put(url, headers=headers, json=payload, timeout=8)
            if put_r.status_code in [200, 201]:
                return True, "✅ Dauerhaft in GitHub gespeichert!"
            else:
                return False, f"⚠️ Lokal gespeichert, aber GitHub-Fehler ({put_r.status_code})"
    except Exception as e:
        return False, f"⚠️ Lokal gespeichert (GitHub-Fehler: {e})"

    return True, "ℹ️ Für diese Sitzung gespeichert (Für dauerhaften Cloud-Sync bitte GitHub-Token in Secrets hinterlegen)."

def send_email_alert(subject: str, body_text: str):
    """Sendet eine E-Mail-Benachrichtigung aufs Smartphone, sofern SMTP-Daten in st.secrets hinterlegt sind."""
    try:
        if "SMTP_USER" in st.secrets and "SMTP_PASSWORD" in st.secrets:
            smtp_server = st.secrets.get("SMTP_SERVER", "smtp.gmail.com")
            smtp_port = int(st.secrets.get("SMTP_PORT", 587))
            smtp_user = st.secrets["SMTP_USER"]
            smtp_pass = st.secrets["SMTP_PASSWORD"]
            email_to = st.secrets.get("EMAIL_RECEIVER", smtp_user)

            msg = MIMEMultipart()
            msg["From"] = smtp_user
            msg["To"] = email_to
            msg["Subject"] = subject
            msg.attach(MIMEText(body_text, "plain", "utf-8"))

            server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
            server.quit()
            return True
    except Exception:
        pass
    return False

if "user_data" not in st.session_state:
    st.session_state["user_data"] = load_user_data()

PORTFOLIO = {}
for k, v in DEFAULT_PORTFOLIO.items():
    PORTFOLIO[k] = v.copy()
    if v["ticker"] and k in st.session_state["user_data"].get("shares", {}):
        PORTFOLIO[k]["shares"] = int(st.session_state["user_data"]["shares"][k])

# --- 4. HILFSFUNKTIONEN (WÄHRUNG, WKN-MAPPING & MATHEMATIK) ---
@st.cache_data(ttl=3600)
def get_fx_rates_to_eur():
    rates = {"EUR": 1.0, "USD": 0.92, "GBP": 1.19, "GBp": 0.0119, "GBX": 0.0119, "HKD": 0.118}
    try:
        eur_usd = yf.Ticker("EURUSD=X").fast_info.get("lastPrice", 1.085)
        eur_gbp = yf.Ticker("EURGBP=X").fast_info.get("lastPrice", 0.84)
        eur_hkd = yf.Ticker("EURHKD=X").fast_info.get("lastPrice", 8.45)
        if eur_usd and eur_usd > 0:
            rates["USD"] = 1.0 / eur_usd
        if eur_gbp and eur_gbp > 0:
            rates["GBP"] = 1.0 / eur_gbp
            rates["GBp"] = rates["GBP"] / 100.0
            rates["GBX"] = rates["GBP"] / 100.0
        if eur_hkd and eur_hkd > 0:
            rates["HKD"] = 1.0 / eur_hkd
    except Exception:
        pass
    return rates

@st.cache_data(ttl=3600)
def resolve_identifier_to_ticker(query: str):
    q_clean = query.strip().upper()
    if q_clean in ["PFSE25", "PFSE21", "DE000PFSE253", "DE000PFSE212", "PFISTERER", "PFS0.DE", "PFSE.DE"]:
        try:
            test_hist = yf.Ticker("PFS0.DE").history(period="1y")
            if len(test_hist) > 20:
                return "PFS0.DE", "PFISTERER Holding SE"
        except Exception:
            pass
        return "PFSE.DE", "PFISTERER Holding SE"

    url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        quotes = data.get("quotes", [])
        if quotes:
            return quotes[0]["symbol"], quotes[0].get("longname", quotes[0].get("shortname", query))
    except Exception:
        pass
    return q_clean, query

def calculate_dynamic_cagr(hist_df: pd.DataFrame, target_years: int):
    if hist_df.empty or len(hist_df) < 20:
        return None, 0.0
    end_date = hist_df.index[-1]
    start_date_target = end_date - pd.DateOffset(years=target_years)
    
    if hist_df.index[0] <= start_date_target + pd.Timedelta(days=30):
        sub_df = hist_df[hist_df.index >= start_date_target]
        actual_years = float(target_years)
    else:
        sub_df = hist_df
        actual_years = (end_date - sub_df.index[0]).days / 365.25
        
    if actual_years < 0.3:
        return None, 0.0
    start_price = sub_df["Close"].iloc[0]
    end_price = sub_df["Close"].iloc[-1]
    if start_price <= 0:
        return None, 0.0
    cagr = (end_price / start_price) ** (1 / actual_years) - 1
    return cagr * 100, round(actual_years, 1)

def calculate_dividend_cagr(div_series: pd.Series):
    if div_series is None or div_series.empty or len(div_series) < 2:
        return 0.0
    try:
        div_df = div_series.to_frame(name="div")
        div_df["year"] = div_df.index.year
        yearly_divs = div_df.groupby("year")["div"].sum()
        current_year = pd.Timestamp.now().year
        full_years = yearly_divs[yearly_divs.index < current_year]
        if len(full_years) >= 2:
            lookback = min(5, len(full_years) - 1)
            end_val = full_years.iloc[-1]
            start_val = full_years.iloc[-(lookback + 1)]
            if start_val > 0 and end_val > 0:
                cagr = (end_val / start_val) ** (1 / lookback) - 1
                return float(np.clip(cagr * 100, -15.0, 25.0))
    except Exception:
        pass
    return 3.5

def evaluate_stock_score(pe, p_cf, div_yield, div_cagr, rev_earn_growth, nd_ebitda, upside_1y, is_financial=False, roe=None):
    """
    Bewertet die 5 Kern-Kennzahlen mit jeweils 0, 1 oder 2 Punkten (Summe: 0 bis 10 Punkte).
    Zahlt eine Aktie keine Dividende, wird automatisch das Umsatz-/Gewinnwachstum herangezogen.
    """
    scores = {}
    
    # 1. KGV (P/E)
    if pe is not None and pe > 0:
        if pe <= 18:
            scores["KGV"] = 2
        elif pe <= 28:
            scores["KGV"] = 1
        else:
            scores["KGV"] = 0
    else:
        scores["KGV"] = 0

    # 2. Kurs-Cashflow (P/OCF)
    if p_cf is not None and p_cf > 0:
        if p_cf <= 14:
            scores["P/OCF"] = 2
        elif p_cf <= 22:
            scores["P/OCF"] = 1
        else:
            scores["P/OCF"] = 0
    elif is_financial and roe is not None:
        if roe >= 12:
            scores["P/OCF"] = 2
        elif roe >= 8:
            scores["P/OCF"] = 1
        else:
            scores["P/OCF"] = 0
    else:
        scores["P/OCF"] = 1

    # 3. Dividendenwachstum ODER Umsatz-/Gewinnwachstum (bei Wachstumswerten ohne Dividende)
    if div_yield is not None and div_yield > 0:
        if div_cagr is not None:
            if div_cagr >= 6.0:
                scores["Wachstum"] = 2
            elif div_cagr >= 1.0:
                scores["Wachstum"] = 1
            else:
                scores["Wachstum"] = 0
        else:
            scores["Wachstum"] = 0
    else:
        if rev_earn_growth is not None:
            if rev_earn_growth >= 12.0:
                scores["Wachstum"] = 2
            elif rev_earn_growth >= 4.0:
                scores["Wachstum"] = 1
            else:
                scores["Wachstum"] = 0
        else:
            scores["Wachstum"] = 0

    # 4. Verschuldung (Net Debt / EBITDA) bzw. ROE bei Finanzwerten
    if is_financial:
        if roe is not None:
            if roe >= 12:
                scores["Bilanz (ND/EBITDA)"] = 2
            elif roe >= 7:
                scores["Bilanz (ND/EBITDA)"] = 1
            else:
                scores["Bilanz (ND/EBITDA)"] = 0
        else:
            scores["Bilanz (ND/EBITDA)"] = 1
    else:
        if nd_ebitda is not None:
            if nd_ebitda <= 1.5:
                scores["Bilanz (ND/EBITDA)"] = 2
            elif nd_ebitda <= 3.0:
                scores["Bilanz (ND/EBITDA)"] = 1
            else:
                scores["Bilanz (ND/EBITDA)"] = 0
        else:
            scores["Bilanz (ND/EBITDA)"] = 0

    # 5. Analysten-Kurspotenzial (12M)
    if upside_1y is not None:
        if upside_1y >= 12.0:
            scores["Potenzial (12M)"] = 2
        elif upside_1y >= 2.0:
            scores["Potenzial (12M)"] = 1
        else:
            scores["Potenzial (12M)"] = 0
    else:
        scores["Potenzial (12M)"] = 1

    total_score = sum(scores.values())
    return total_score, scores

def style_mover_changes(val):
    if isinstance(val, (int, float)):
        if val > 0:
            return "color: #2ecc71; font-weight: bold;"
        elif val < 0:
            return "color: #e74c3c; font-weight: bold;"
    return ""

def style_score_matrix(val):
    if isinstance(val, (int, float)):
        if val >= 7:
            return "background-color: rgba(46, 204, 113, 0.35); font-weight: bold;"
        elif val >= 4:
            return "background-color: rgba(241, 196, 15, 0.35); font-weight: bold;"
        else:
            return "background-color: rgba(231, 76, 60, 0.35); font-weight: bold;"
    if isinstance(val, str):
        if "🟢" in val:
            return "background-color: rgba(46, 204, 113, 0.15);"
        elif "🟡" in val:
            return "background-color: rgba(241, 196, 15, 0.15);"
        elif "🔴" in val:
            return "background-color: rgba(231, 76, 60, 0.15);"
    return ""

# --- 5. SIDEBAR & HAUPTNAVIGATION ---
st.sidebar.header("🗂️ Mein Depot (46 Werte)")
portfolio_keys = list(PORTFOLIO.keys())
display_options = [f"{k} ({v['shares']} Stk. | {v['wkn']})" if v["ticker"] else k for k, v in PORTFOLIO.items()]
selected_name = st.sidebar.selectbox(
    "Aktie aus dem Depot wählen:",
    options=display_options,
    index=29
)

selected_key = portfolio_keys[display_options.index(selected_name)]
selected_meta = PORTFOLIO[selected_key]

st.sidebar.markdown("---")
st.sidebar.subheader("💾 Cloud-Speicher & E-Mail")
if "GITHUB_TOKEN" in st.secrets and "GITHUB_REPO" in st.secrets:
    st.sidebar.success("GitHub-Sync: Aktiv ✅")
else:
    st.sidebar.info("GitHub-Sync: Noch nicht in Secrets hinterlegt (Änderungen gelten aktuell pro Sitzung).")

if "SMTP_USER" in st.secrets and "SMTP_PASSWORD" in st.secrets:
    st.sidebar.success("E-Mail-Alarme: Aktiv 📧")
else:
    st.sidebar.caption("E-Mail-Alarme: Optional über SMTP-Daten in Secrets aktivierbar.")

if st.sidebar.button("💾 Alle Änderungen jetzt speichern", use_container_width=True):
    ok, msg = save_user_data(st.session_state["user_data"])
    if ok:
        st.sidebar.success(msg)
    else:
        st.sidebar.warning(msg)

st.title("📈 Fundamentales Aktien- & Depot-Dashboard")

tab_start, tab_single, tab_compare, tab_portfolio = st.tabs([
    "📰 Start: News, Watchlist & Alarme",
    "🔍 Einzelaktien-Analyse (1/3/5J-Szenarien)", 
    "⚖️ 3-Aktien-Vergleich & Ampel-Score (0-10)",
    "🗂️ Gesamtdepot-Übersicht & Bestand (+1/-1)"
])

fx_rates = get_fx_rates_to_eur()

# ==============================================================================
# TAB 1: STARTSEITE (NEWS, WATCHLIST & ALARME)
# ==============================================================================
with tab_start:
    st.markdown("### 📰 Cockpit: Kurzfrist-Bewegungen, Watchlist, Preis-Alarme & News")
    
    col_wl, col_al = st.columns([1.1, 1.3])
    
    with col_wl:
        with st.expander("🔭 Watchlist verwalten (Werte hinzufügen / entfernen)", expanded=False):
            wl_input = st.text_input("Neue Aktie zur Watchlist (WKN, ISIN oder Ticker):", placeholder="z.B. A1J4U4 oder ASML.AS")
            if st.button("➕ Zur Watchlist hinzufügen"):
                if wl_input.strip():
                    t_sym, r_name = resolve_identifier_to_ticker(wl_input.strip())
                    st.session_state["user_data"].setdefault("watchlist", {})[r_name] = {"ticker": t_sym, "wkn": wl_input.strip().upper()}
                    save_user_data(st.session_state["user_data"])
                    st.success(f"{r_name} ({t_sym}) hinzugefügt!")
                    st.rerun()
            
            current_wl = st.session_state["user_data"].get("watchlist", {})
            if current_wl:
                del_wl = st.selectbox("Aktie aus Watchlist entfernen:", options=["--- Bitte wählen ---"] + list(current_wl.keys()))
                if del_wl != "--- Bitte wählen ---" and st.button("🗑️ Aus Watchlist löschen"):
                    del st.session_state["user_data"]["watchlist"][del_wl]
                    save_user_data(st.session_state["user_data"])
                    st.rerun()

    with col_al:
        with st.expander("🔔 Preis-Grenzwerte (Alarme in €) festlegen", expanded=False):
            all_tracked = {k: v["ticker"] for k, v in PORTFOLIO.items() if v["ticker"]}
            for k, v in st.session_state["user_data"].get("watchlist", {}).items():
                all_tracked[f"[Watchlist] {k}"] = v["ticker"]
                
            sel_alert_name = st.selectbox("Aktie für Grenzwert auswählen:", options=list(all_tracked.keys()))
            sel_alert_ticker = all_tracked[sel_alert_name]
            existing_alert = st.session_state["user_data"].get("alerts", {}).get(sel_alert_ticker, {"min_eur": 0.0, "max_eur": 0.0})
            
            ca1, ca2 = st.columns(2)
            min_limit = ca1.number_input("Untergrenze / Kauflimit (€)", min_value=0.0, value=float(existing_alert.get("min_eur", 0.0)), step=1.0)
            max_limit = ca2.number_input("Obergrenze / Kursziel (€)", min_value=0.0, value=float(existing_alert.get("max_eur", 0.0)), step=1.0)
            
            if st.button("💾 Grenzwert speichern"):
                st.session_state["user_data"].setdefault("alerts", {})[sel_alert_ticker] = {
                    "name": sel_alert_name,
                    "min_eur": min_limit,
                    "max_eur": max_limit
                }
                ok, msg = save_user_data(st.session_state["user_data"])
                st.success(f"Grenzwert für {sel_alert_name} gespeichert! ({msg})")

    st.markdown("---")
    
    col_scan_btn, col_filter = st.columns([1, 2])
    scan_group = col_filter.radio("Auswahl für Kurzfrist-Check:", ["⭐ Watchlist & Top-15 Depotwerte (Schnell)", "🗂️ Alle 46 Depotwerte + Watchlist (Komplett)"], horizontal=True)
    
    if col_scan_btn.button("🚀 Kurzfrist-Check & Alarme jetzt prüfen", type="primary"):
        items_to_scan = []
        for k, v in st.session_state["user_data"].get("watchlist", {}).items():
            items_to_scan.append(("🔭 Watchlist", k, v["ticker"], v.get("wkn", "")))
            
        port_items = [(k, v) for k, v in PORTFOLIO.items() if v["ticker"]]
        if "Schnell" in scan_group:
            alert_tickers = set(st.session_state["user_data"].get("alerts", {}).keys())
            subset = [x for x in port_items[:15]]
            for k, v in port_items[15:]:
                if v["ticker"] in alert_tickers:
                    subset.append((k, v))
            port_items = subset
            
        for k, v in port_items:
            items_to_scan.append(("💼 Depot", k, v["ticker"], v["wkn"]))
            
        mover_rows = []
        triggered_alerts = []
        prog = st.progress(0, text="Prüfe Kurse der letzten Handelstage...")
        
        for idx, (kat, name, t_sym, wkn) in enumerate(items_to_scan):
            try:
                tk = yf.Ticker(t_sym)
                h5 = tk.history(period="7d")
                if not h5.empty:
                    curr = tk.fast_info.get("currency", "EUR")
                    p_fac = 0.01 if curr in ["GBp", "GBX"] else 1.0
                    disp_c = "GBP" if curr in ["GBp", "GBX"] else curr
                    fx = fx_rates.get(disp_c, 1.0)
                    
                    p_now = h5["Close"].iloc[-1] * p_fac
                    p_eur = p_now * fx
                    p_1d = h5["Close"].iloc[-2] * p_fac if len(h5) >= 2 else p_now
                    p_5d = h5["Close"].iloc[0] * p_fac
                    
                    chg_1d = ((p_now / p_1d) - 1) * 100 if p_1d > 0 else 0.0
                    chg_5d = ((p_now / p_5d) - 1) * 100 if p_5d > 0 else 0.0
                    
                    al_shared = st.session_state["user_data"].get("alerts", {}).get(t_sym, {})
                    min_e = al_shared.get("min_eur", 0.0)
                    max_e = al_shared.get("max_eur", 0.0)
                    status_str = "🟢 OK"
                    if min_e > 0 and p_eur <= min_e:
                        status_str = f"🔻 UNTERGRENZE ({min_e:.2f} €)"
                        triggered_alerts.append(f"⚠️ {name} ({t_sym}): Kurs ({p_eur:.2f} €) hat Untergrenze von {min_e:.2f} € erreicht/unterschritten!")
                    elif max_e > 0 and p_eur >= max_e:
                        status_str = f"🚀 OBERGRENZE ({max_e:.2f} €)"
                        triggered_alerts.append(f"🚀 {name} ({t_sym}): Kurs ({p_eur:.2f} €) hat Obergrenze von {max_e:.2f} € erreicht/überschritten!")
                        
                    mover_rows.append({
                        "Kategorie": kat,
                        "Unternehmen": name,
                        "WKN": wkn,
                        "Ticker": t_sym,
                        "Kurs (€)": round(p_eur, 2),
                        "Heute / 1T (%)": round(chg_1d, 2),
                        "Letzte 5T (%)": round(chg_5d, 2),
                        "Limit-Status": status_str
                    })
            except Exception:
                pass
            prog.progress((idx + 1) / len(items_to_scan))
        prog.empty()
        
        if triggered_alerts:
            st.error("### 🔔 Ausgelöste Preis-Alarme!")
            for al_msg in triggered_alerts:
                st.write(al_msg)
            email_body = "Folgende Preis-Grenzwerte in deinem Aktien-Dashboard wurden erreicht:\n\n" + "\n".join(triggered_alerts)
            mail_sent = send_email_alert("🔔 Kursalarm: Grenzwert im Aktien-Dashboard erreicht", email_body)
            if mail_sent:
                st.info("📧 E-Mail-Benachrichtigung wurde an dein Smartphone versendet!")
        else:
            st.success("✅ Keine Preis-Grenzwerte über- oder unterschritten.")
            
        if mover_rows:
            df_movers = pd.DataFrame(mover_rows).sort_values(by="Heute / 1T (%)", ascending=False)
            st.dataframe(
                df_movers.style.map(style_mover_changes, subset=["Heute / 1T (%)", "Letzte 5T (%)"]),
                use_container_width=True, hide_index=True
            )

    st.markdown("---")
    st.markdown("#### 🗞️ Aktuelle Unternehmens-News (Depot & Watchlist)")
    news_Pool = {k: v["ticker"] for k, v in st.session_state["user_data"].get("watchlist", {}).items()}
    for k, v in PORTFOLIO.items():
        if v["ticker"]:
            news_Pool[k] = v["ticker"]
            
    sel_news_stock = st.selectbox("Wähle eine Aktie für aktuelle Schlagzeilen:", options=list(news_Pool.keys()), index=0)
    if sel_news_stock:
        t_news = news_Pool[sel_news_stock]
        try:
            raw_news = yf.Ticker(t_news).news
            if raw_news:
                for n_item in raw_news[:6]:
                    content = n_item.get("content", n_item)
                    title = content.get("title", n_item.get("title", "Schlagzeile"))
                    publisher = content.get("provider", {}).get("displayName", n_item.get("publisher", "Finanz-News"))
                    link = content.get("canonicalUrl", {}).get("url", n_item.get("link", f"https://finance.yahoo.com/quote/{t_news}"))
                    st.markdown(f"- **[{title}]({link})** *(Quelle: {publisher})*")
            else:
                st.info("Aktuell keine englisch-/deutschsprachigen Meldungen über den Feed verfügbar.")
        except Exception:
            st.caption("News-Feed konnte momentan nicht geladen werden.")

# ==============================================================================
# TAB 2: EINZELAKTIEN-ANALYSE
# ==============================================================================
with tab_single:
    col_search, col_info, col_pos = st.columns([1.1, 1.6, 1.1])
    with col_search:
        default_q = selected_meta["ticker"] if selected_meta["ticker"] else "MSFT"
        search_input = st.text_input(
            "WKN, ISIN, Name oder Ticker prüfen:", 
            value=default_q,
            help="Wähle links im Menü eine deiner 46 Depot-Aktien oder tippe hier eine beliebige WKN ein."
        ).strip()

    if search_input:
        with st.spinner("Marktdaten, Bilanzen und Analystenschätzungen werden ausgewertet..."):
            ticker_symbol, resolved_name = resolve_identifier_to_ticker(search_input)
            stock = yf.Ticker(ticker_symbol)
            
            try:
                info = stock.info
                hist = stock.history(period="10y")
                divs = stock.dividends
                
                if hist.empty and "currentPrice" not in info:
                    st.error(f"Keine validen Daten für '{search_input}' (Ticker: {ticker_symbol}) gefunden.")
                    st.stop()
                    
                currency = info.get("currency", "EUR")
                raw_price = info.get("currentPrice") or info.get("regularMarketPrice") or hist["Close"].iloc[-1]
                
                is_gbp_pence = (currency in ["GBp", "GBX"])
                price_factor = 0.01 if is_gbp_pence else 1.0
                current_price = raw_price * price_factor
                display_currency = "GBP" if is_gbp_pence else currency
                fx_to_eur = fx_rates.get(display_currency, 1.0)
                
                company_name = info.get("longName", resolved_name)
                sector = info.get("sector", "Sektor N/A")
                industry = info.get("industry", "")
                
                with col_info:
                    st.subheader(f"{company_name} (`{ticker_symbol}`)")
                    st.caption(f"**Sektor:** {sector} ({industry}) | **Aktueller Kurs:** `{current_price:.2f} {display_currency}` (~ {current_price * fx_to_eur:.2f} €)")

                matched_shares = selected_meta["shares"] if selected_meta["ticker"] == ticker_symbol else 0
                if matched_shares == 0:
                    for k, v in PORTFOLIO.items():
                        if v["ticker"] == ticker_symbol:
                            matched_shares = v["shares"]
                            break

                div_rate = info.get("dividendRate", 0) or 0
                div_yield_info = info.get("dividendYield", 0)
                if div_rate > 0 and current_price > 0:
                    div_yield = (div_rate / current_price) * 100
                elif div_yield_info:
                    div_yield = div_yield_info * 100
                else:
                    div_yield = 0.0

                with col_pos:
                    if matched_shares > 0:
                        pos_val_eur = matched_shares * current_price * fx_to_eur
                        annual_div_eur = pos_val_eur * (div_yield / 100.0)
                        st.info(f"**Dein Depotbestand:** {matched_shares} Stück\n\n**Positionswert:** ~ {pos_val_eur:,.2f} €\n\n**Jährl. Dividende:** ~ {annual_div_eur:,.2f} €")
                    else:
                        st.caption("Kein Bestand im hinterlegten Depot (Beobachtungswert).")

                st.markdown("---")

                m1, m2, m3, m4 = st.columns(4)

                with m1:
                    st.markdown("#### 📊 A: Kurshistorie")
                    cagr_5, yrs_5 = calculate_dynamic_cagr(hist, 5)
                    cagr_10, yrs_10 = calculate_dynamic_cagr(hist, 10)
                    
                    if cagr_5 is not None:
                        lbl_5 = "Ø Wachstum (5 Jahre)" if yrs_5 == 5.0 else f"Ø Wachstum (seit {yrs_5} J.)"
                        st.metric(label=lbl_5, value=f"{cagr_5:+.2f} % p.a.")
                    else:
                        st.metric(label="Ø Wachstum (5 Jahre)", value="N/A")
                        
                    if cagr_10 is not None:
                        lbl_10 = "Ø Wachstum (10 Jahre)" if yrs_10 == 10.0 else f"Ø Max-Historie ({yrs_10} J.)"
                        st.metric(label=lbl_10, value=f"{cagr_10:+.2f} % p.a.")
                    else:
                        st.metric(label="Ø Wachstum (10 Jahre)", value="N/A")

                with m2:
                    st.markdown("#### 💰 B: Dividende & Cashflow")
                    fcf = info.get("freeCashflow")
                    ocf = info.get("operatingCashflow")
                    shares_out = info.get("sharesOutstanding")
                    
                    is_reit_or_bdc = (sector == "Real Estate") or ("Asset Management" in industry) or (ticker_symbol in ["O", "MAIN"])
                    cashflow_basis = ocf if (is_reit_or_bdc and ocf) else fcf
                    cf_label = "OCF/FFO" if is_reit_or_bdc else "FCF"
                    
                    fcf_payout = None
                    if cashflow_basis and shares_out and div_rate > 0:
                        total_div = div_rate * shares_out
                        if cashflow_basis > 0:
                            fcf_payout = (total_div / cashflow_basis) * 100
                        else:
                            fcf_payout = 999.0
                    
                    st.metric(label="Aktuelle Dividendenrendite", value=f"{div_yield:.2f} %")
                    
                    if div_yield == 0:
                        st.info("Schüttet aktuell keine Dividende aus.")
                        div_cagr_hist = 0.0
                    else:
                        div_cagr_hist = calculate_dividend_cagr(divs)
                        if fcf_payout is not None:
                            if fcf_payout > 80:
                                st.error(f"🔴 {cf_label}-Payout: {fcf_payout:.1f}% (Kritisch >80%)")
                            elif fcf_payout > 65:
                                st.warning(f"🟡 {cf_label}-Payout: {fcf_payout:.1f}% (Erhöht)")
                            else:
                                st.success(f"🟢 {cf_label}-Payout: {fcf_payout:.1f}% (Gesund)")
                        else:
                            payout_std = (info.get("payoutRatio", 0) or 0) * 100
                            st.caption(f"Payout Ratio (Gewinn): {payout_std:.1f}%")

                with m3:
                    st.markdown("#### ⚖️ C: Bewertung (Multiples)")
                    trailing_pe = info.get("trailingPE")
                    forward_pe = info.get("forwardPE")
                    
                    eps = info.get("trailingEps")
                    hist_5y = hist[hist.index >= (hist.index[-1] - pd.DateOffset(years=5))] if not hist.empty else hist
                    avg_price_5y = (hist_5y["Close"].mean() * price_factor) if not hist_5y.empty else current_price
                    pe_5y_avg = (avg_price_5y / eps) if (eps and eps > 0) else None
                    
                    pe_str = f"{trailing_pe:.1f}" if trailing_pe else "N/A"
                    pe_sub = f"Forward KGV: {forward_pe:.1f}" if forward_pe else (f"5J-Schnitt (Proxy): {pe_5y_avg:.1f}" if pe_5y_avg else "Kein positives EPS")
                    st.metric(label="Aktuelles KGV (P/E)", value=pe_str, delta=pe_sub, delta_color="off")
                    
                    mcap = info.get("marketCap")
                    p_cf = (mcap / ocf) if (ocf and ocf > 0 and mcap) else None
                    p_cf_5y = ((avg_price_5y / current_price) * p_cf) if (p_cf and current_price > 0) else None
                    
                    p_cf_str = f"{p_cf:.1f}" if p_cf else "N/A"
                    p_cf_sub = f"5J-Schnitt (Proxy): ~{p_cf_5y:.1f}" if p_cf_5y else "Cashflow N/A"
                    st.metric(label="Kurs-Cashflow (P/OCF)", value=p_cf_str, delta=p_cf_sub, delta_color="off")

                with m4:
                    st.markdown("#### 🛡️ D: Bilanz & Stabilität")
                    is_financial = (sector == "Financial Services") and (ticker_symbol not in ["MAIN", "DB1.DE"])
                    
                    if is_financial:
                        roe = (info.get("returnOnEquity", 0) or 0) * 100
                        pb = info.get("priceToBook")
                        st.metric(label="Kurs-Buchwert (KBV / P/B)", value=f"{pb:.2f}" if pb else "N/A")
                        if roe > 12:
                            st.success(f"🟢 Eigenkapitalrendite (ROE): {roe:.1f}% (Stark)")
                        elif roe > 7:
                            st.warning(f"🟡 Eigenkapitalrendite (ROE): {roe:.1f}% (Solide)")
                        else:
                            st.error(f"🔴 Eigenkapitalrendite (ROE): {roe:.1f}% (Schwach)")
                    else:
                        total_debt = info.get("totalDebt", 0) or 0
                        total_cash = info.get("totalCash", 0) or 0
                        ebitda = info.get("ebitda")
                        
                        net_debt = total_debt - total_cash
                        st.metric(label="Nettoverschuldung", value=f"{net_debt / 1e9:.2f} Mrd. {display_currency}")
                        
                        if net_debt <= 0:
                            st.success("🟢 Netto-Cash-Position (Schuldenfrei)")
                        elif ebitda and ebitda > 0:
                            nd_ebitda = net_debt / ebitda
                            if nd_ebitda > 3.5:
                                st.error(f"🔴 Net Debt / EBITDA: {nd_ebitda:.2f}x (Hoch)")
                            elif nd_ebitda > 2.0:
                                st.warning(f"🟡 Net Debt / EBITDA: {nd_ebitda:.2f}x (Moderat)")
                            else:
                                st.success(f"🟢 Net Debt / EBITDA: {nd_ebitda:.2f}x (Sehr solide)")
                        else:
                            st.warning("🟡 EBITDA negativ/N/A – Bilanz im Detail prüfen")

                st.markdown("---")
                st.markdown("### 🎯 Perspektivische Entwicklung: Kurs-Szenarien & Dividendenrendite (1, 3 und 5 Jahre)")
                
                target_high = (info.get("targetHighPrice") or 0) * price_factor
                target_mean = (info.get("targetMeanPrice") or 0) * price_factor
                target_low = (info.get("targetLowPrice") or 0) * price_factor
                num_analysts = info.get("numberOfAnalystOpinions", 0) or 0
                rec_key = info.get("recommendationKey", "none").upper()
                
                base_cagr_init = ((target_mean / current_price) - 1) * 100 if (target_mean > 0 and current_price > 0) else (cagr_5 if cagr_5 else 7.0)
                best_cagr_init = ((target_high / current_price) - 1) * 100 if (target_high > 0 and current_price > 0) else base_cagr_init + 6.0
                bear_cagr_init = ((target_low / current_price) - 1) * 100 if (target_low > 0 and current_price > 0) else base_cagr_init - 8.0

                base_cagr_init = float(np.clip(base_cagr_init, -15.0, 25.0))
                best_cagr_init = float(np.clip(best_cagr_init, base_cagr_init + 2.0, 35.0))
                bear_cagr_init = float(np.clip(bear_cagr_init, -25.0, base_cagr_init - 2.0))

                default_div_growth = div_cagr_hist if (fcf_payout is None or fcf_payout <= 80) else max(0.0, div_cagr_hist * 0.3)

                col_ctrl, col_charts = st.columns([1, 2.6])
                
                with col_ctrl:
                    st.markdown("##### 1. Analysten-Vorgabe (12M)")
                    st.write(f"**Votum:** `{rec_key}` ({num_analysts} Analysten)")
                    if target_mean > 0:
                        st.write(f"🚀 **High:** {target_high:.2f} {display_currency}")
                        st.write(f"🎯 **Mean (Base):** {target_mean:.2f} {display_currency}")
                        st.write(f"🔻 **Low:** {target_low:.2f} {display_currency}")
                    else:
                        st.caption("Keine direkten Analystenziele hinterlegt – nutze historische Wachstumsrate.")
                    
                    st.markdown("##### 2. Szenario-Parameter anpassen")
                    best_rate = st.slider("Best Case Kurswachstum (% p.a.)", -10.0, 40.0, round(best_cagr_init, 1), 0.5)
                    base_rate = st.slider("Base Case Kurswachstum (% p.a.)", -15.0, 30.0, round(base_cagr_init, 1), 0.5)
                    bear_rate = st.slider("Bear Case Kurswachstum (% p.a.)", -30.0, 15.0, round(bear_cagr_init, 1), 0.5)
                    
                    st.markdown("##### 3. Dividenden-Dynamik")
                    div_growth_rate = st.slider(
                        "Erw. Dividendenwachstum (% p.a.)", 
                        -10.0, 25.0, round(default_div_growth, 1), 0.5
                    )

                with col_charts:
                    tab_price, tab_div = st.tabs(["📈 Aktienkurs-Korridor (1, 3 & 5 Jahre)", "💵 Dividendenrendite-Projektion (3 & 5 Jahre)"])
                    
                    future_years = [0, 1, 2, 3, 4, 5]
                    last_date = hist.index[-1]
                    future_dates = [last_date + pd.DateOffset(years=y) for y in future_years]
                    
                    best_path = [current_price * ((1 + best_rate/100) ** y) for y in future_years]
                    base_path = [current_price * ((1 + base_rate/100) ** y) for y in future_years]
                    bear_path = [current_price * ((1 + bear_rate/100) ** y) for y in future_years]

                    with tab_price:
                        hist_recent = hist[hist.index >= (hist.index[-1] - pd.DateOffset(years=3))].copy()
                        hist_recent["Close_Adj"] = hist_recent["Close"] * price_factor
                        
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=hist_recent.index, y=hist_recent["Close_Adj"],
                            mode="lines", name="Historie (3J)", line=dict(color="#1f77b4", width=2)
                        ))
                        fig.add_trace(go.Scatter(
                            x=future_dates, y=best_path,
                            mode="lines+markers", name=f"Best Case ({best_rate:+.1f}% p.a.)",
                            line=dict(color="#2ca02c", width=2, dash="dash")
                        ))
                        fig.add_trace(go.Scatter(
                            x=future_dates, y=base_path,
                            mode="lines+markers", name=f"Base Case ({base_rate:+.1f}% p.a.)",
                            line=dict(color="#ff7f0e", width=3)
                        ))
                        fig.add_trace(go.Scatter(
                            x=future_dates, y=bear_path,
                            mode="lines+markers", name=f"Bear Case ({bear_rate:+.1f}% p.a.)",
                            line=dict(color="#d62728", width=2, dash="dot"),
                            fill="tonexty", fillcolor="rgba(255, 127, 14, 0.1)"
                        ))
                        fig.update_layout(
                            title=f"Kurs-Projektion für {company_name} (in {display_currency})",
                            xaxis_title="Jahr", yaxis_title=f"Kurs ({display_currency})",
                            hovermode="x unified", height=380, margin=dict(l=20, r=20, t=40, b=20)
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    with tab_div:
                        yoc_now = div_yield
                        yoc_1y = div_yield * ((1 + div_growth_rate / 100) ** 1)
                        yoc_3y = div_yield * ((1 + div_growth_rate / 100) ** 3)
                        yoc_5y = div_yield * ((1 + div_growth_rate / 100) ** 5)
                        
                        fig_div = go.Figure(data=[
                            go.Bar(
                                x=["Aktuell", "In 1 Jahr", "In 3 Jahren", "In 5 Jahren"],
                                y=[yoc_now, yoc_1y, yoc_3y, yoc_5y],
                                text=[f"{yoc_now:.2f} %", f"{yoc_1y:.2f} %", f"{yoc_3y:.2f} %", f"{yoc_5y:.2f} %"],
                                textposition="auto",
                                marker_color=["#6c757d", "#17a2b8", "#28a745", "#1e7e34"]
                            )
                        ])
                        fig_div.update_layout(
                            title=f"Erwartete Dividendenrendite (Yield on Cost) bei {div_growth_rate:+.1f}% Wachstum p.a.",
                            yaxis_title="Dividendenrendite (%)", height=380, margin=dict(l=20, r=20, t=40, b=20)
                        )
                        st.plotly_chart(fig_div, use_container_width=True)

            except Exception as e:
                st.error(f"Fehler bei der Verarbeitung der Daten für {ticker_symbol}: {e}")

# ==============================================================================
# TAB 3: 3-AKTIEN-VERGLEICH & AMPEL-BEWERTUNGSSYSTEM (0 BIS 10 PUNKTE)
# ==============================================================================
with tab_compare:
    st.markdown("### ⚖️ Marktweiter 3-Aktien-Vergleich inkl. Ampel-Bewertungssystem (0 bis 10 Punkte)")
    st.write("Vergleiche 3 beliebige Aktien (WKN, ISIN oder Ticker) direkt gegeneinander. Bei Aktien ohne Dividende fließt automatisch das Umsatz-/Gewinnwachstum in Kriterium 3 ein.")
    
    cc1, cc2, cc3, cc_time = st.columns([1, 1, 1, 1])
    comp_1 = cc1.text_input("Aktie 1 (WKN / Ticker):", value="MSFT")
    comp_2 = cc2.text_input("Aktie 2 (WKN / Ticker):", value="SAP.DE")
    comp_3 = cc3.text_input("Aktie 3 (WKN / Ticker):", value="NVDA")
    comp_period = cc_time.selectbox("Zeitraum für Kursvergleich:", options=["1y", "3y", "5y"], index=1, format_func=lambda x: {"1y": "1 Jahr", "3y": "3 Jahre", "5y": "5 Jahre"}[x])

    if st.button("🔍 3 Aktien jetzt vergleichen & bewerten", type="primary"):
        queries = [q.strip() for q in [comp_1, comp_2, comp_3] if q.strip()]
        comp_data = []
        fig_comp = go.Figure()
        
        with st.spinner("Lade Vergleichsdaten und berechne Ampel-Scores..."):
            for q in queries:
                t_sym, r_name = resolve_identifier_to_ticker(q)
                tk = yf.Ticker(t_sym)
                try:
                    inf = tk.info
                    h_c = tk.history(period=comp_period)
                    divs_c = tk.dividends
                    
                    curr = inf.get("currency", "EUR")
                    p_fac = 0.01 if curr in ["GBp", "GBX"] else 1.0
                    disp_c = "GBP" if curr in ["GBp", "GBX"] else curr
                    fx = fx_rates.get(disp_c, 1.0)
                    
                    raw_p = inf.get("currentPrice") or inf.get("regularMarketPrice") or (h_c["Close"].iloc[-1] if not h_c.empty else 0)
                    p_adj = raw_p * p_fac
                    p_eur = p_adj * fx
                    
                    if not h_c.empty and h_c["Close"].iloc[0] > 0:
                        norm_series = ((h_c["Close"] / h_c["Close"].iloc[0]) - 1.0) * 100
                        fig_comp.add_trace(go.Scatter(x=h_c.index, y=norm_series, mode="lines", name=f"{inf.get('shortName', r_name)} ({t_sym})"))
                        
                    pe = inf.get("trailingPE") or inf.get("forwardPE")
                    mcap = inf.get("marketCap")
                    ocf = inf.get("operatingCashflow")
                    p_cf = (mcap / ocf) if (mcap and ocf and ocf > 0) else None
                    
                    d_rate = inf.get("dividendRate", 0) or 0
                    d_yield = (d_rate / p_adj * 100) if (d_rate > 0 and p_adj > 0) else ((inf.get("dividendYield", 0) or 0) * 100)
                    div_cagr = calculate_dividend_cagr(divs_c) if d_yield > 0 else 0.0
                    
                    rev_g = (inf.get("revenueGrowth") or 0) * 100
                    earn_g = (inf.get("earningsGrowth") or 0) * 100
                    if rev_g != 0 and earn_g != 0:
                        rev_earn_growth = (rev_g + earn_g) / 2.0
                    elif rev_g != 0:
                        rev_earn_growth = rev_g
                    else:
                        rev_earn_growth = earn_g
                    
                    if d_yield > 0:
                        growth_str = f"Div: {div_cagr:+.1f} % p.a."
                    else:
                        growth_str = f"Ums/Gew: {rev_earn_growth:+.1f} %"
                    
                    sector = inf.get("sector", "")
                    is_fin = (sector == "Financial Services") and (t_sym not in ["MAIN", "DB1.DE"])
                    roe = (inf.get("returnOnEquity", 0) or 0) * 100 if is_fin else None
                    
                    t_debt = inf.get("totalDebt", 0) or 0
                    t_cash = inf.get("totalCash", 0) or 0
                    ebitda = inf.get("ebitda")
                    net_debt = t_debt - t_cash
                    nd_ebitda = (net_debt / ebitda) if (ebitda and ebitda > 0) else (0.0 if net_debt <= 0 else None)
                    
                    t_mean = (inf.get("targetMeanPrice") or 0) * p_fac
                    upside_1y = ((t_mean / p_adj) - 1.0) * 100 if (t_mean > 0 and p_adj > 0) else 0.0
                    
                    total_score, sub_scores = evaluate_stock_score(
                        pe, p_cf, d_yield, div_cagr, rev_earn_growth, nd_ebitda, upside_1y, is_fin, roe
                    )
                    
                    comp_data.append({
                        "Name": inf.get("shortName", r_name),
                        "Ticker": t_sym,
                        "Kurs (€)": f"{p_eur:.2f} €",
                        "Div.-Rendite": f"{d_yield:.2f} %",
                        "1. KGV (P/E)": f"{pe:.1f}" if pe else "N/A",
                        "2. Kurs-Cashflow (P/OCF)": f"{p_cf:.1f}" if p_cf else (f"ROE: {roe:.1f}%" if roe else "N/A"),
                        "3. Dynamik (Div. / Ums.-Gew.)": growth_ str,
                        "4. Net Debt / EBITDA": "Netto-Cash (<0x)" if (not is_fin and net_debt <= 0) else (f"{nd_ebitda:.2f}x" if nd_ebitda is not None else (f"ROE: {roe:.1f}%" if is_fin and roe else "N/A")),
                        "5. Analysten-Potenzial (12M)": f"{upside_1y:+.1f} %",
                        "🎯 GESAMT-SCORE (0-10)": total_score,
                        "_scores": sub_scores
                    })
                except Exception as e:
                    st.warning(f"Konnte {q} nicht vollständig laden: {e}")

        if comp_data:
            sc_cols = st.columns(len(comp_data))
            for idx, item in enumerate(comp_data):
                sc = item["🎯 GESAMT-SCORE (0-10)"]
                if sc >= 7:
                    badge = f"🟢 {sc} / 10 Punkte (Stark)"
                    bg_color = "rgba(46, 204, 113, 0.18)"
                elif sc >= 4:
                    badge = f"🟡 {sc} / 10 Punkte (Solide)"
                    bg_color = "rgba(241, 196, 15, 0.18)"
                else:
                    badge = f"🔴 {sc} / 10 Punkte (Schwach/Teuer)"
                    bg_color = "rgba(231, 76, 60, 0.18)"
                    
                with sc_cols[idx]:
                    st.markdown(
                        f"<div style='padding:15px; border-radius:10px; background-color:{bg_color}; text-align:center;'>"
                        f"<h4 style='margin:0;'>{item['Name']} ({item['Ticker']})</h4>"
                        f"<h2 style='margin:8px 0;'>{badge}</h2>"
                        f"<small>Aktueller Kurs: {item['Kurs (€)']} | Dividende: {item['Div.-Rendite']}</small>"
                        f"</div>", unsafe_allow_html=True
                    )
            
            st.markdown("#### 📈 Normierter Kursvergleich (in %)")
            fig_comp.update_layout(yaxis_title="Wertentwicklung (%)", xaxis_title="Datum", hovermode="x unified", height=380)
            st.plotly_chart(fig_comp, use_container_width=True)
            
            st.markdown("#### 🚦 Detaillierte Kennzahlen-Matrix mit Ampel-Bewertung")
            matrix_rows = []
            for item in comp_data:
                s_map = item["_scores"]
                emo = {2: "🟢 (2 Pkt.)", 1: "🟡 (1 Pkt.)", 0: "🔴 (0 Pkt.)"}
                matrix_rows.append({
                    "Unternehmen": f"{item['Name']} ({item['Ticker']})",
                    "🎯 Gesamt-Score (0-10)": item["🎯 GESAMT-SCORE (0-10)"],
                    "1. KGV (P/E)": f"{item['1. KGV (P/E)']}  |  {emo[s_map['KGV']]}",
                    "2. Kurs-Cashflow (P/OCF)": f"{item['2. Kurs-Cashflow (P/OCF)']}  |  {emo[s_map['P/OCF']]}",
                    "3. Wachstum (Div / Ums-Gew)": f"{item['3. Dynamik (Div. / Ums.-Gew.)']}  |  {emo[s_map['Wachstum']]}",
                    "4. Bilanz (ND/EBITDA)": f"{item['4. Net Debt / EBITDA']}  |  {emo[s_map['Bilanz (ND/EBITDA)']]}",
                    "5. Potenzial (12M)": f"{item['5. Analysten-Potenzial (12M)']}  |  {emo[s_map['Potenzial (12M)']]}"
                })
            df_comp_matrix = pd.DataFrame(matrix_rows)
            st.dataframe(df_comp_matrix.style.map(style_score_matrix), use_container_width=True, hide_index=True)

# ==============================================================================
# TAB 4: GESAMTDEPOT-ÜBERSICHT & INTERAKTIVE BESTANDSSTEUERUNG (+1 / -1)
# ==============================================================================
with tab_portfolio:
    st.markdown("### 🗂️ Gesamtdepot-Screening & Interaktive Bestandssteuerung (+1 / -1)")
    st.write("Klicke auf **Gesamtdepot live auswerten**, um alle 46 Positionen abzurufen. Anschließend kannst du in der Spalte **Stück** per Klick (`+` / `-`) deine Anzahl anpassen und dauerhaft speichern.")
    
    if st.button("🔄 Gesamtdepot jetzt live auswerten", type="primary"):
        rows = []
        progress_bar = st.progress(0, text="Rufe Livedaten für 46 Aktien ab...")
        valid_items = [(k, v) for k, v in PORTFOLIO.items() if v["ticker"]]
        
        for idx, (name, meta) in enumerate(valid_items):
            t_sym = meta["ticker"]
            shares = meta["shares"]
            wkn = meta["wkn"]
            cluster = meta["cluster"]
            
            if t_sym == "PFS0.DE":
                t_sym, _ = resolve_identifier_to_ticker("PFSE25")
                
            try:
                tk = yf.Ticker(t_sym)
                inf = tk.info
                curr = inf.get("currency", "EUR")
                raw_p = inf.get("currentPrice") or inf.get("regularMarketPrice") or 0.0
                
                p_fac = 0.01 if curr in ["GBp", "GBX"] else 1.0
                disp_curr = "GBP" if curr in ["GBp", "GBX"] else curr
                p_adj = raw_p * p_fac
                fx = fx_rates.get(disp_curr, 1.0)
                
                price_eur = p_adj * fx
                d_rate
