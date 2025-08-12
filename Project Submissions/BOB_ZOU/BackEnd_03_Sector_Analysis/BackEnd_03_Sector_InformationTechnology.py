import os
import requests
import numpy as np
import pandas as pd
from fredapi import Fred
from datetime import datetime

GENERAL_Output_columns = pd.MultiIndex.from_tuples([
    ("Latest Data", "Data"),
    ("Latest Data", "Release Date"),

    ("MoM", "MoM Change"),
    ("MoM", "MoM Change Pct"),

    ("YoY", "YoY Change"),
    ("YoY", "YoY Change Pct")
])

FIXED_BTC_LINE = ("**Note:** BTC (Bitcoin) acts as a liquidity/risk-appetite proxy; during risk-on phases, flows into high-beta tech (and semis) rise alongside crypto, pushing positive short-run correlation.")


def BTC_USD():
    api_key = "9THYPTW9AE1DRHYJ"
    url = ("https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=USD&apikey=" + api_key)
    r = requests.get(url)
    js = r.json()
    key = "Time Series (Digital Currency Daily)"
    df = pd.DataFrame(js[key]).T
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    latest       = float(df.iloc[-1, 3])
    prev_month   = float(df.iloc[-30, 3])
    prev_day     = float(df.iloc[-2, 3])

    mom_growth  = latest - prev_month
    dod_growth  = latest - prev_day
    mom_pct     = (mom_growth / prev_month) * 100
    dod_pct     = (dod_growth / prev_day) * 100

    data = [[
        f"{latest:+.2f}", f"(Midnight (UTC)) {df.index[-1].strftime('%B %d, %Y')}",
        f"{mom_growth:+,.2f}", f"{mom_pct:+.2f}%",
        f"{dod_growth:+,.2f} (d/d)", f"{dod_pct:+.2f}% (d/d)"
    ]]

    signal = 0
    if   mom_pct >= 10: signal += 2
    elif mom_pct >= 3:  signal += 1
    elif mom_pct <= -10: signal -= 2
    elif mom_pct < 0:    signal -= 1

    if abs(dod_pct) >= 5: signal += 1 if dod_pct > 0 else -1  

    trend = "higher" if mom_pct > 0 else ("lower" if mom_pct < 0 else "flat")
    analysis = (f"Bitcoin last price {latest:,.0f} USD; {mom_pct:+.2f}% vs ~30d and {dod_pct:+.2f}% d/d ({trend} on a 30-day lookback). " + "\n" + "\n" + FIXED_BTC_LINE)

    return data, analysis, signal


def semis_ip_analysis(mom_pct: float, yoy_pct: float):
    signal = 0

    if mom_pct > 1.0:
        txt = (f"Semis IP (NAICS 3344) rose {mom_pct:.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY) — broad-based strength.")
        signal += 3
    elif mom_pct > 0:
        txt = (f"Semis IP edged up {mom_pct:.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY).")
        signal += 1
    elif mom_pct < -1.0:
        txt = (f"Semis IP fell {abs(mom_pct):.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY) — notable soft patch.")
        signal -= 3
    else:
        txt = (f"Semis IP slipped {abs(mom_pct):.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY).")
        signal -= 1

    if yoy_pct > 0:
        signal += 1
    elif yoy_pct < 0:
        signal -= 1

    return txt, signal

def Semis_IP():
    fred = Fred(api_key="ef418abc7729096c77970a459e9d62dd")
    series = fred.get_series("IPG3344S")
    s = series.dropna()
    s.index.name = "Date"

    latest      = float(s.iloc[-1])
    prev        = float(s.iloc[-2])
    lysm        = float(s.iloc[-13])

    mom_growth  = latest - prev
    yoy_growth  = latest - lysm
    mom_pct     = (mom_growth / prev) * 100
    yoy_pct     = (yoy_growth / lysm) * 100

    data = [[f"{latest:.2f}",
             s.index[-1].strftime("%b, %Y"),
             f"{mom_growth:+.2f}",
             f"{mom_pct:+.2f}%",
             f"{yoy_growth:+.2f}",
             f"{yoy_pct:+.2f}%"]]

    analysis, sig = semis_ip_analysis(mom_pct, yoy_pct)
    return data, analysis, sig


def Information_Technology_Sector():
    macro_data_sign = 0
    output_data = []

    ip_data, ip_out, ip_sig = Semis_IP()
    macro_data_sign += ip_sig

    btc_data, btc_out, btc_sig = BTC_USD()
    macro_data_sign += btc_sig

    output_data += ip_data + btc_data
    idx = ["Semis Industrial Production (NAICS 3344)", "Bitcoin (USD)"]

    df = pd.DataFrame(output_data, columns=GENERAL_Output_columns, index=idx)

    return ip_out, btc_out, df, macro_data_sign
