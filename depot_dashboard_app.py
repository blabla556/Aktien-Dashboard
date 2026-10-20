import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import requests

# --- 1. SEITENKONFIGURATION ---
st.set_page_config(page_title="Depot & Aktien-Analyse Dashboard", layout="wide", page_icon="📈")

# --- 2. HINTERLEGTES DEPOT MIT STÜCKZAHLEN (46 POSITIONEN - FINAL BESTÄTIGT) ---
PORTFOLIO = {
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

# --- 3. HILFSFUNKTIONEN (WÄHRUNG, WKN-MAPPING & MATHEMATIK) ---
@st.cache_data(ttl=3600)
def get_fx_rates_to_eur():
    """Holt aktuelle Wechselkurse zur Umrechnung von USD, GBP und HKD in EUR."""
    rates = {"EUR": 1.0, "USD": 0.92, "GBP": 1.19, "GBp": 0.0119, "GBX": 0.0119, "HKD": 0.118}
    try:
        eur_usd = yf.Ticker("EURUSD=X").fast_info.get("lastPrice", 1.085)
        eur_gbp = yf.Ticker("EURGBP=X").fast_info.get("lastPrice", 0.84)
        eur_hkd = yf.Ticker("EURHKD=X").fast_info.get("lastPrice", 8.45)
        if eur_usd > 0: rates["USD"] = 1.0 / eur_usd
        if eur_gbp > 0:
            rates["GBP"] = 1.0 / eur_gbp
            rates["GBp"] = rates["GBP"] / 100.0
            rates["GBX"] = rates["GBP"] / 100.0
        if eur_hkd > 0: rates["HKD"] = 1.0 / eur_hkd
    except Exception:
        pass
    return rates

@st.cache_data(ttl=3600)
def resolve_identifier_to_ticker(query: str):
    """Übersetzt WKN, ISIN oder Unternehmensnamen via Yahoo Finance Search API in einen Ticker."""
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
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        quotes = data.get('quotes', [])
        if quotes:
            return quotes[0]['symbol'], quotes[0].get('longname', quotes[0].get('shortname', query))
    except Exception:
        pass
    return q_clean, query

def calculate_dynamic_cagr(hist_df: pd.DataFrame, target_years: int):
    """Berechnet die jährliche Kurs-Wachstumsrate (CAGR) mit Fallback auf kürzere Historie."""
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
    start_price = sub_df['Close'].iloc[0]
    end_price = sub_df['Close'].iloc[-1]
    if start_price <= 0:
        return None, 0.0
    cagr = (end_price / start_price) ** (1 / actual_years) - 1
    return cagr * 100, round(actual_years, 1)

def calculate_dividend_cagr(div_series: pd.Series):
    """Berechnet das historische Dividendenwachstum (CAGR) der letzten bis zu 5 Jahre."""
    if div_series is None or div_series.empty or len(div_series) < 2:
        return 0.0
    try:
        div_df = div_series.to_frame(name='div')
        div_df['year'] = div_df.index.year
        yearly_divs = div_df.groupby('year')['div'].sum()
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

# --- 4. SIDEBAR & HAUPTNAVIGATION ---
st.sidebar.header("🗂️ Mein Depot (46 Werte)")
portfolio_keys = list(PORTFOLIO.keys())
display_options = [f"{k} ({v['shares']} Stk. | {v['wkn']})" if v['ticker'] else k for k, v in PORTFOLIO.items()]
selected_name = st.sidebar.selectbox(
    "Aktie aus dem Depot wählen:",
    options=display_options,
    index=29  # Startwert: Microsoft Corp.
)

selected_key = portfolio_keys[display_options.index(selected_name)]
selected_meta = PORTFOLIO[selected_key]

st.title("📈 Fundamentales Aktien- & Depot-Dashboard")

main_tab_single, main_tab_portfolio = st.tabs([
    "🔍 Einzelaktien-Analyse (Historie, Cashflow & 1/3/5J-Szenarien)", 
    "🗂️ Gesamtdepot-Übersicht (Alle 46 Positionen & Gewichtung)"
])

fx_rates = get_fx_rates_to_eur()

# ==============================================================================
# TAB 1: EINZELAKTIEN-ANALYSE
# ==============================================================================
with main_tab_single:
    col_search, col_info, col_pos = st.columns([1.1, 1.6, 1.1])
    with col_search:
        default_q = selected_meta["ticker"] if selected_meta["ticker"] else "MSFT"
        search_input = st.text_input(
            "WKN, ISIN, Name oder Ticker prüfen:", 
            value=default_q,
            help="Wähle links im Menü eine deiner 46 Depot-Aktien oder tippe hier eine beliebige WKN ein."
        ).strip()

    if search_input:
        with st.spinner('Marktdaten, Bilanzen und Analystenschätzungen werden ausgewertet...'):
            ticker_symbol, resolved_name = resolve_identifier_to_ticker(search_input)
            stock = yf.Ticker(ticker_symbol)
            
            try:
                info = stock.info
                hist = stock.history(period="10y")
                divs = stock.dividends
                
                if hist.empty and 'currentPrice' not in info:
                    st.error(f"Keine validen Daten für '{search_input}' (Ticker: {ticker_symbol}) gefunden.")
                    st.stop()
                    
                currency = info.get('currency', 'EUR')
                raw_price = info.get('currentPrice') or info.get('regularMarketPrice') or hist['Close'].iloc[-1]
                
                is_gbp_pence = (currency in ['GBp', 'GBX'])
                price_factor = 0.01 if is_gbp_pence else 1.0
                current_price = raw_price * price_factor
                display_currency = "GBP" if is_gbp_pence else currency
                fx_to_eur = fx_rates.get(display_currency, 1.0)
                
                company_name = info.get('longName', resolved_name)
                sector = info.get('sector', 'Sektor N/A')
                industry = info.get('industry', '')
                
                with col_info:
                    st.subheader(f"{company_name} (`{ticker_symbol}`)")
                    st.caption(f"**Sektor:** {sector} ({industry}) | **Aktueller Kurs:** `{current_price:.2f} {display_currency}` (~ {current_price * fx_to_eur:.2f} €)")

                # Depot-Bestandsanzeige oben rechts, falls Aktie im Depot
                matched_shares = selected_meta["shares"] if selected_meta["ticker"] == ticker_symbol else 0
                if matched_shares == 0:
                    for k, v in PORTFOLIO.items():
                        if v["ticker"] == ticker_symbol:
                            matched_shares = v["shares"]
                            break

                div_rate = info.get('dividendRate', 0) or 0
                div_yield_info = info.get('dividendYield', 0)
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

                # --- 5. DIE 4 FUNDAMENTAL-MODULE ---
                m1, m2, m3, m4 = st.columns(4)

                # MODUL A: Historische Kursentwicklung (CAGR 5J & 10J)
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

                # MODUL B: Dividende, FCF-Ausschüttungsquote & 3/5-Jahres-Erwartung
                with m2:
                    st.markdown("#### 💰 B: Dividende & Cashflow")
                    fcf = info.get('freeCashflow')
                    ocf = info.get('operatingCashflow')
                    shares_out = info.get('sharesOutstanding')
                    
                    is_reit_or_bdc = (sector == 'Real Estate') or ('Asset Management' in industry) or (ticker_symbol in ['O', 'MAIN'])
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
                            payout_std = (info.get('payoutRatio', 0) or 0) * 100
                            st.caption(f"Payout Ratio (Gewinn): {payout_std:.1f}%")

                # MODUL C: Fundamental-Bewertung (KGV & KCV vs. 5J-Mittel)
                with m3:
                    st.markdown("#### ⚖️ C: Bewertung (Multiples)")
                    trailing_pe = info.get('trailingPE')
                    forward_pe = info.get('forwardPE')
                    
                    eps = info.get('trailingEps')
                    hist_5y = hist[hist.index >= (hist.index[-1] - pd.DateOffset(years=5))] if not hist.empty else hist
                    avg_price_5y = (hist_5y['Close'].mean() * price_factor) if not hist_5y.empty else current_price
                    pe_5y_avg = (avg_price_5y / eps) if (eps and eps > 0) else None
                    
                    pe_str = f"{trailing_pe:.1f}" if trailing_pe else "N/A"
                    pe_sub = f"Forward KGV: {forward_pe:.1f}" if forward_pe else (f"5J-Schnitt (Proxy): {pe_5y_avg:.1f}" if pe_5y_avg else "Kein positives EPS")
                    st.metric(label="Aktuelles KGV (P/E)", value=pe_str, delta=pe_sub, delta_color="off")
                    
                    mcap = info.get('marketCap')
                    p_cf = (mcap / ocf) if (ocf and ocf > 0 and mcap) else None
                    p_cf_5y = ((avg_price_5y / current_price) * p_cf) if (p_cf and current_price > 0) else None
                    
                    p_cf_str = f"{p_cf:.1f}" if p_cf else "N/A"
                    p_cf_sub = f"5J-Schnitt (Proxy): ~{p_cf_5y:.1f}" if p_cf_5y else "Cashflow N/A"
                    st.metric(label="Kurs-Cashflow (P/OCF)", value=p_cf_str, delta=p_cf_sub, delta_color="off")

                # MODUL D: Bilanz & Verschuldung
                with m4:
                    st.markdown("#### 🛡️ D: Bilanz & Stabilität")
                    is_financial = (sector == 'Financial Services') and (ticker_symbol not in ['MAIN', 'DB1.DE'])
                    
                    if is_financial:
                        roe = (info.get('returnOnEquity', 0) or 0) * 100
                        pb = info.get('priceToBook')
                        st.metric(label="Kurs-Buchwert (KBV / P/B)", value=f"{pb:.2f}" if pb else "N/A")
                        if roe > 12:
                            st.success(f"🟢 Eigenkapitalrendite (ROE): {roe:.1f}% (Stark)")
                        elif roe > 7:
                            st.warning(f"🟡 Eigenkapitalrendite (ROE): {roe:.1f}% (Solide)")
                        else:
                            st.error(f"🔴 Eigenkapitalrendite (ROE): {roe:.1f}% (Schwach)")
                    else:
                        total_debt = info.get('totalDebt', 0) or 0
                        total_cash = info.get('totalCash', 0) or 0
                        ebitda = info.get('ebitda')
                        
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

                # --- 6. SZENARIO-KORRIDOR (KURS) & DIVIDENDEN-PROJEKTION (3 & 5 JAHRE) ---
                st.markdown("### 🎯 Perspektivische Entwicklung: Kurs-Szenarien & Dividendenrendite (1, 3 und 5 Jahre)")
                
                target_high = (info.get('targetHighPrice') or 0) * price_factor
                target_mean = (info.get('targetMeanPrice') or 0) * price_factor
                target_low = (info.get('targetLowPrice') or 0) * price_factor
                num_analysts = info.get('numberOfAnalystOpinions', 0) or 0
                rec_key = info.get('recommendationKey', 'none').upper()
                
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
                        -10.0, 25.0, round(default_div_growth, 1), 0.5,
                        help="Vorbelegt mit dem historischen 5-Jahres-Dividendenwachstum (automatisch reduziert bei FCF-Payout > 80%)."
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
                        hist_recent['Close_Adj'] = hist_recent['Close'] * price_factor
                        
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=hist_recent.index, y=hist_recent['Close_Adj'],
                            mode='lines', name='Historie (3J)', line=dict(color='#1f77b4', width=2)
                        ))
                        fig.add_trace(go.Scatter(
                            x=future_dates, y=best_path,
                            mode='lines+markers', name=f'Best Case ({best_rate:+.1f}% p.a.)',
                            line=dict(color='#2ca02c', width=2, dash='dash')
                        ))
                        fig.add_trace(go.Scatter(
                            x=future_dates, y=base_path,
                            mode='lines+markers', name=f'Base Case ({base_rate:+.1f}% p.a.)',
                            line=dict(color='#ff7f0e', width=3)
                        ))
                        fig.add_trace(go.Scatter(
                            x=future_dates, y=bear_path,
                            mode='lines+markers', name=f'Bear Case ({bear_rate:+.1f}% p.a.)',
                            line=dict(color='#d62728', width=2, dash='dot'),
                            fill='tonexty', fillcolor='rgba(255, 127, 14, 0.1)'
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
                                textposition='auto',
                                marker_color=['#6c757d', '#17a2b8', '#28a745', '#1e7e34']
                            )
                        ])
                        fig_div.update_layout(
                            title=f"Erwartete Dividendenrendite (Yield on Cost) bei {div_growth_rate:+.1f}% Wachstum p.a.",
                            yaxis_title="Dividendenrendite (%)", height=380, margin=dict(l=20, r=20, t=40, b=20)
                        )
                        st.plotly_chart(fig_div, use_container_width=True)

                    yoc_1y_val = div_yield * ((1 + div_growth_rate / 100) ** 1)
                    yoc_3y_val = div_yield * ((1 + div_growth_rate / 100) ** 3)
                    yoc_5y_val = div_yield * ((1 + div_growth_rate / 100) ** 5)
                    
                    summary_df = pd.DataFrame({
                        "Kennzahl / Szenario": [
                            "🚀 Best Case Aktienkurs", 
                            "🎯 Base Case Aktienkurs (Mittelwert)", 
                            "🔻 Bear Case Aktienkurs (Untergrenze)",
                            "💰 Erwartete Dividendenrendite (auf aktuellen Kurs)"
                        ],
                        "Dynamik p.a.": [
                            f"{best_rate:+.1f} %", 
                            f"{base_rate:+.1f} %", 
                            f"{bear_rate:+.1f} %",
                            f"{div_growth_rate:+.1f} %"
                        ],
                        "Aktuell": [
                            f"{current_price:.2f} {display_currency}",
                            f"{current_price:.2f} {display_currency}",
                            f"{current_price:.2f} {display_currency}",
                            f"{div_yield:.2f} %"
                        ],
                        "Sicht: 1 Jahr": [
                            f"{best_path[1]:.2f} {display_currency}", 
                            f"{base_path[1]:.2f} {display_currency}", 
                            f"{bear_path[1]:.2f} {display_currency}",
                            f"{yoc_1y_val:.2f} %"
                        ],
                        "Sicht: 3 Jahre": [
                            f"{best_path[3]:.2f} {display_currency}", 
                            f"{base_path[3]:.2f} {display_currency}", 
                            f"{bear_path[3]:.2f} {display_currency}",
                            f"{yoc_3y_val:.2f} %"
                        ],
                        "Sicht: 5 Jahre": [
                            f"{best_path[5]:.2f} {display_currency}", 
                            f"{base_path[5]:.2f} {display_currency}", 
                            f"{bear_path[5]:.2f} {display_currency}",
                            f"{yoc_5y_val:.2f} %"
                        ]
                    })
                    st.dataframe(summary_df, use_container_width=True, hide_index=True)

            except Exception as e:
                st.error(f"Fehler bei der Verarbeitung der Daten für {ticker_symbol}: {e}")

# ==============================================================================
# TAB 2: GESAMTDEPOT-ÜBERSICHT (ALLE 46 POSITIONEN)
# ==============================================================================
with main_tab_portfolio:
    st.markdown("### 🗂️ Gesamtdepot-Screening & Sektor-Allokation (46 Positionen)")
    st.write("Klicke auf den Button, um alle 46 Depotpositionen live abzurufen, in Euro umzurechnen und nach Kurspotenzial sowie Dividendenrendite auszuwerten.")
    
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
                pos_val_eur = price_eur * shares
                
                d_rate = inf.get("dividendRate", 0) or 0
                d_yield = (d_rate / p_adj * 100) if (d_rate > 0 and p_adj > 0) else ((inf.get("dividendYield", 0) or 0) * 100)
                annual_div_eur = pos_val_eur * (d_yield / 100.0)
                
                t_mean = (inf.get("targetMeanPrice") or 0) * p_fac
                upside_1y = ((t_mean / p_adj) - 1.0) * 100 if (t_mean > 0 and p_adj > 0) else 0.0
                pe = inf.get("trailingPE")
                
                rows.append({
                    "Unternehmen": name,
                    "WKN": wkn,
                    "Ticker": t_sym,
                    "Cluster": cluster,
                    "Stück": shares,
                    "Kurs (€)": round(price_eur, 2),
                    "Positionswert (€)": round(pos_val_eur, 2),
                    "Div.-Rendite (%)": round(d_yield, 2),
                    "Jährl. Dividende (€)": round(annual_div_eur, 2),
                    "KGV": round(pe, 1) if pe else None,
                    "Analysten-Potenzial 1J (%)": round(upside_1y, 1)
                })
            except Exception:
                pass
            progress_bar.progress((idx + 1) / len(valid_items), text=f"Verarbeite {name} ({idx+1}/{len(valid_items)})...")
            
        progress_bar.empty()
        
        if rows:
            df_port = pd.DataFrame(rows)
            total_val = df_port["Positionswert (€)"].sum()
            total_div = df_port["Jährl. Dividende (€)"].sum()
            weighted_yield = (total_div / total_val * 100) if total_val > 0 else 0.0
            weighted_upside = ((df_port["Positionswert (€)"] * df_port["Analysten-Potenzial 1J (%)"]).sum() / total_val) if total_val > 0 else 0.0
            
            df_port["Gewichtung (%)"] = (df_port["Positionswert (€)"] / total_val * 100).round(2)
            df_port = df_port.sort_values(by="Positionswert (€)", ascending=False)
            
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Gesamtwert Depot", f"{total_val:,.2f} €")
            k2.metric("Jährliche Brutto-Dividende", f"{total_div:,.2f} €")
            k3.metric("Gewichtete Dividendenrendite", f"{weighted_yield:.2f} %")
            k4.metric("Ø Analysten-Potenzial (12M)", f"{weighted_upside:+.1f} %")
            
            c_chart1, c_chart2 = st.columns(2)
            with c_chart1:
                fig_pie = px.pie(df_port, values="Positionswert (€)", names="Cluster", hole=0.4, title="Depot-Allokation nach Sektor-Clustern")
                st.plotly_chart(fig_pie, use_container_width=True)
            with c_chart2:
                fig_bar = px.bar(df_port.head(15), x="Positionswert (€)", y="Unternehmen", color="Cluster", orientation="h", title="Top-15 Positionen nach Wert (€)")
                fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig_bar, use_container_width=True)
                
            st.markdown("#### 📋 Vollständige Bestands- und Potenzialtabelle (sortierbar)")
            st.dataframe(df_port, use_container_width=True, hide_index=True)
