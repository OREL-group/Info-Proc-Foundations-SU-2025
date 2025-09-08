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


def wti_crude_analysis(mom_pct: float, dod_pct: float):
    signal = 0

    if mom_pct <= -10:
        txt_core = "WTI crude fell sharply over ~30 days"
        signal += 2
    elif -10 < mom_pct < 0:
        txt_core = "WTI crude dipped over ~30 days"
        signal += 1
    elif 0 < mom_pct < 10:
        txt_core = "WTI crude rose over ~30 days"
        signal -= 1
    else:  # ≥ +10
        txt_core = "WTI crude jumped over ~30 days"
        signal -= 2

    if abs(dod_pct) >= 5:
        signal += (1 if dod_pct < 0 else -1)

    txt = f"{txt_core} ({mom_pct:+.2f}% 30d; {dod_pct:+.2f}% d/d)."
    return txt, signal

def WTI_Crude():
    fred = Fred(api_key="ef418abc7729096c77970a459e9d62dd")
    WTI = fred.get_series("DCOILWTICO").dropna()

    if len(WTI) < 32:
        raise RuntimeError("Insufficient history for 30d and 1d comparisons")

    latest = float(WTI.iloc[-1])
    prev_day = float(WTI.iloc[-2])
    prev_month = float(WTI.iloc[-32])  # ~30 calendar days of daily prints

    mom_growth = latest - prev_month
    dod_growth = latest - prev_day
    mom_pct = (mom_growth / prev_month) * 100 if prev_month != 0 else 0.0
    dod_pct = (dod_growth / prev_day) * 100 if prev_day != 0 else 0.0

    data = [[
        f"{latest:,.2f} USD/bbl", f"(Daily) {WTI.index[-1].strftime('%B %d, %Y')}",
        f"{mom_growth:+,.2f}", f"{mom_pct:+.2f}%",
        f"{dod_growth:+,.2f} (Day to Day)", f"{dod_pct:+.2f}% (Day to Day)"
    ]]

    analysis, sig = wti_crude_analysis(mom_pct, dod_pct)
    return data, analysis, sig

def cpi_electricity_analysis(mom_pct: float, yoy_pct: float):
    signal = 0
    if mom_pct <= -1.0:
        txt = (f"CPI: Electricity fell {abs(mom_pct):.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY) — affordability tailwind.")
        signal += 2
    elif -1.0 < mom_pct < 0:
        txt = (f"CPI: Electricity dipped {abs(mom_pct):.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY).")
        signal += 1
    elif 0 < mom_pct < 1.0:
        txt = (f"CPI: Electricity rose {mom_pct:.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY).")
        signal -= 1
    else:  # ≥ +1.0
        txt = (f"CPI: Electricity jumped {mom_pct:.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY) — potential demand/optics headwind.")
        signal -= 2

    if yoy_pct < 0:
        signal += 1
    elif yoy_pct > 0:
        signal -= 1
    return txt, signal

def CPI_Electricity():
    fred = Fred(api_key="ef418abc7729096c77970a459e9d62dd")
    electric = fred.get_series("CUSR0000SEHF01").dropna()

    latest   = float(electric.iloc[-1])
    prev     = float(electric.iloc[-2])
    lysm     = float(electric.iloc[-13])

    mom_abs  = latest - prev
    yoy_abs  = latest - lysm
    mom_pct  = (mom_abs / prev) * 100 if prev != 0 else 0.0
    yoy_pct  = (yoy_abs / lysm) * 100 if lysm != 0 else 0.0

    data = [[
        f"{latest:.2f}", electric.index[-1].strftime("%B %d, %Y"),
        f"{mom_abs:+.2f}", f"{mom_pct:+.2f}%",
        f"{yoy_abs:+.2f}", f"{yoy_pct:+.2f}%"
    ]]

    analysis, sig = cpi_electricity_analysis(mom_pct, yoy_pct)
    return data, analysis, sig

def Utilities_Sector():
    macro_data_sign = 0
    output_data = []

    wti_data, wti_out, wti_sig = WTI_Crude()
    macro_data_sign += wti_sig

    cpi_data, cpi_out, cpi_sig = CPI_Electricity()
    macro_data_sign += cpi_sig

    output_data += wti_data + cpi_data
    idx = ["WTI Crude Oil Future (Daily)", "CPI: Electricity"]

    df = pd.DataFrame(output_data, columns=GENERAL_Output_columns, index=idx)

    return wti_out, cpi_out, df, macro_data_sign
