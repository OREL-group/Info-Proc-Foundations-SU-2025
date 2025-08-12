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

def copper_price_analysis(mom_pct: float, yoy_pct: float):
    signal = 0

    if mom_pct > 5.0:
        txt = (f"Copper strengthened {mom_pct:.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY) — robust demand backdrop for Materials.")
        signal += 3
    elif mom_pct > 0:
        txt = (f"Copper edged up {mom_pct:.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY).")
        signal += 1
    elif mom_pct <= -5.0:
        txt = (f"Copper fell {abs(mom_pct):.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY) — notable soft patch.")
        signal -= 3
    else:
        txt = (f"Copper slipped {abs(mom_pct):.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY).")
        signal -= 1

    if   yoy_pct > 0: signal += 1
    elif yoy_pct < 0: signal -= 1

    return txt, signal

def Copper_Global():
    fred = Fred(api_key="ef418abc7729096c77970a459e9d62dd")
    copper = fred.get_series("PCOPPUSDM").dropna()
    copper.index.name = "Date"

    latest   = float(copper.iloc[-1])
    prev     = float(copper.iloc[-2])
    lysm     = float(copper.iloc[-13])

    mom_abs  = latest - prev
    yoy_abs  = latest - lysm
    mom_pct  = (mom_abs / prev) * 100 if prev  != 0 else 0.0
    yoy_pct  = (yoy_abs / lysm) * 100 if lysm != 0 else 0.0

    data = [[
        f"{latest:,.0f}", copper.index[-1].strftime("%B %d, %Y"),
        f"{mom_abs:+,.0f}", f"{mom_pct:+.2f}%",
        f"{yoy_abs:+,.0f}", f"{yoy_pct:+.2f}%"
    ]]

    analysis, sig = copper_price_analysis(mom_pct, yoy_pct)
    return data, analysis, sig

def primary_metals_ip_analysis(mom_pct: float, yoy_pct: float):
    signal = 0
    if mom_pct > 1.0:
        txt = (f"Primary Metals Industrial Production rose {mom_pct:.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY) — broad-based strength.")
        signal += 3
    elif mom_pct > 0:
        txt = (f"Primary Metals Industrial Production edged up {mom_pct:.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY).")
        signal += 1
    elif mom_pct <= -1.0:
        txt = (f"Primary Metals Industrial Production fell {abs(mom_pct):.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY) — notable soft patch.")
        signal -= 3
    else:
        txt = (f"Primary Metals Industrial Production slipped {abs(mom_pct):.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY).")
        signal -= 1

    if   yoy_pct > 0: signal += 1
    elif yoy_pct < 0: signal -= 1

    return txt, signal

def Primary_Metals_IP():
    fred = Fred(api_key="ef418abc7729096c77970a459e9d62dd")
    primary = fred.get_series("IPG331S").dropna()
    primary.index.name = "Date"

    latest   = float(primary.iloc[-1])
    prev     = float(primary.iloc[-2])
    lysm     = float(primary.iloc[-13])

    mom_abs  = latest - prev
    yoy_abs  = latest - lysm
    mom_pct  = (mom_abs / prev) * 100 if prev  != 0 else 0.0
    yoy_pct  = (yoy_abs / lysm) * 100 if lysm != 0 else 0.0

    data = [[
        f"{latest:.2f}", primary.index[-1].strftime("%B %d, %Y"),
        f"{mom_abs:+.2f}", f"{mom_pct:+.2f}%",
        f"{yoy_abs:+.2f}", f"{yoy_pct:+.2f}%"
    ]]

    analysis, sig = primary_metals_ip_analysis(mom_pct, yoy_pct)
    return data, analysis, sig

def Materials_Sector():
    macro_data_sign = 0
    output_data = []

    cu_data, cu_out, cu_sig = Copper_Global()
    macro_data_sign += cu_sig

    pm_data, pm_out, pm_sig = Primary_Metals_IP()
    macro_data_sign += pm_sig

    output_data += cu_data + pm_data
    idx = ["Copper Price (Global)", "Primary Metals Industrial Production"]

    df = pd.DataFrame(output_data, columns=GENERAL_Output_columns, index=idx)

    return cu_out, pm_out, df, macro_data_sign
