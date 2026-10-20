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

def calculate_dynamic_c