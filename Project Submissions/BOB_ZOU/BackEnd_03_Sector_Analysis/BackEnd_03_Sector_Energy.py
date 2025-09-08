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


def brent_crude_analysis(mom_pct: float, dod_pct: float):
    signal = 0
    if mom_pct >= 10:
        txt_core = "Brent crude jumped over ~30 days"
        signal += 2
    elif 0 < mom_pct < 10:
        txt_core = "Brent crude rose over ~30 days"
        signal += 1
    elif -10 < mom_pct < 0:
        txt_core = "Brent crude dipped over ~30 days"
        signal -= 1
    else:  # ≤ -10
        txt_core = "Brent crude fell sharply over ~30 days"
        signal -= 2

    if abs(dod_pct) >= 5:
        signal += (1 if dod_pct > 0 else -1)

    txt = f"{txt_core} ({mom_pct:+.2f}% 30d; {dod_pct:+.2f}% d/d)."
    return txt, signal

def Brent_Crude():
    fred = Fred(api_key="ef418abc7729096c77970a459e9d62dd")
    brent = fred.get_series("DCOILBRENTEU").dropna()

    if len(brent) < 32:
        raise RuntimeError("Insufficient history for 30d and 1d comparisons")

    latest = float(brent.iloc[-1])
    prev_day = float(brent.iloc[-2])
    prev_month = float(brent.iloc[-32])  # ~30 calendar days

    mom_growth = latest - prev_month
    dod_growth = latest - prev_day
    mom_pct = (mom_growth / prev_month) * 100 if prev_month != 0 else 0.0
    dod_pct = (dod_growth / prev_day) * 100 if prev_day != 0 else 0.0

    data = [[
        f"{latest:,.2f} USD/bbl",
        f"(Daily) {brent.index[-1].strftime('%B %d, %Y')}",
        f"{mom_growth:+,.2f}",
        f"{mom_pct:+.2f}%",
        f"{dod_growth:+,.2f} (d/d)",
        f"{dod_pct:+.2f}% (d/d)"
    ]]

    analysis, sig = brent_crude_analysis(mom_pct, dod_pct)
    return data, analysis, sig


def natgas_price_analysis_energy(mom_pct: float, yoy_pct: float):
    signal = 0
    if mom_pct >= 10.0:
        txt = (f"Henry Hub natural gas jumped {mom_pct:.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY) — supportive for upstream realizations.")
        signal += 3
    elif 0 < mom_pct < 10.0:
        txt = (f"Henry Hub natural gas rose {mom_pct:.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY).")
        signal += 1
    elif -10.0 < mom_pct < 0:
        txt = (f"Henry Hub natural gas dipped {abs(mom_pct):.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY).")
        signal -= 1
    else:  # ≤ -10%
        txt = (f"Henry Hub natural gas fell {abs(mom_pct):.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY) — upstream headwind.")
        signal -= 3

    if yoy_pct > 0:
        signal += 1
    elif yoy_pct < 0:
        signal -= 1

    return txt, signal

def Natural_Gas_HenryHub():
    fred = Fred(api_key="ef418abc7729096c77970a459e9d62dd")
    Nat_Gas = fred.get_series("DHHNGSP").dropna()

    latest   = float(Nat_Gas.iloc[-1])
    prev     = float(Nat_Gas.iloc[-2])
    lysm     = float(Nat_Gas.iloc[-13])

    mom_abs  = latest - prev
    yoy_abs  = latest - lysm
    mom_pct  = (mom_abs / prev) * 100 if prev  != 0 else 0.0
    yoy_pct  = (yoy_abs / lysm) * 100 if lysm != 0 else 0.0

    data = [[
        f"{latest:.2f}", Nat_Gas.index[-1].strftime("%b, %Y"),
        f"{mom_abs:+.2f}", f"{mom_pct:+.2f}%",
        f"{yoy_abs:+.2f}", f"{yoy_pct:+.2f}%"
    ]]

    analysis, sig = natgas_price_analysis_energy(mom_pct, yoy_pct)
    return data, analysis, sig


def Energy_Sector():
    macro_data_sign = 0
    output_data = []

    br_data, br_out, br_sig = Brent_Crude()
    macro_data_sign += br_sig

    ng_data, ng_out, ng_sig = Natural_Gas_HenryHub()
    macro_data_sign += ng_sig

    output_data += br_data + ng_data
    idx = ["Brent Crude (Daily)", "Nat Gas (Henry Hub)"]

    df = pd.DataFrame(output_data, columns=GENERAL_Output_columns, index=idx)

    return br_out, ng_out, df, macro_data_sign
