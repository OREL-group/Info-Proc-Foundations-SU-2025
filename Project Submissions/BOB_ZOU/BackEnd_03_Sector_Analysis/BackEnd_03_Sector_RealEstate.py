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

def mortgage_rate_analysis(mom_pp: float, yoy_pp: float):
    signal = 0

    if mom_pp <= -0.25:
        txt = (f"30Y mortgage rate fell {mom_pp:+.2f} pp MoM "
               f"({yoy_pp:+.2f} pp YoY), easing financing costs.")
        signal += 2
    elif -0.25 < mom_pp < 0:
        txt = (f"30Y mortgage rate dipped {mom_pp:+.2f} pp MoM "
               f"({yoy_pp:+.2f} pp YoY). Slightly supportive.")
        signal += 1
    elif 0 < mom_pp < 0.25:
        txt = (f"30Y mortgage rate rose {mom_pp:+.2f} pp MoM "
               f"({yoy_pp:+.2f} pp YoY). Mild headwind.")
        signal -= 1
    elif mom_pp >= 0.25:
        txt = (f"30Y mortgage rate jumped {mom_pp:+.2f} pp MoM "
               f"({yoy_pp:+.2f} pp YoY), tightening affordability.")
        signal -= 2
    else:
        txt = (f"30Y mortgage rate unchanged MoM ({mom_pp:+.2f} pp), "
               f"{yoy_pp:+.2f} pp YoY.")
        
    if yoy_pp < 0:
        signal += 1
    elif yoy_pp > 0:
        signal -= 1
    return txt, signal

def Mortgage_30Y():
    fred = Fred(api_key="ef418abc7729096c77970a459e9d62dd")
    M30 = fred.get_series("MORTGAGE30US").dropna()

    latest = float(M30.iloc[-1])
    latest_date = M30.index[-1]

    prev_m   = float(M30.iloc[-2])
    lysm_m   = float(M30.iloc[-13])

    mom_pp = latest - prev_m
    yoy_pp = latest - lysm_m
    mom_pct = (mom_pp / prev_m) * 100 if prev_m != 0 else 0.0
    yoy_pct = (yoy_pp / lysm_m) * 100 if lysm_m != 0 else 0.0

    data = [[
        f"{latest:.2f}%", latest_date.strftime("%B %d, %Y"),
        f"{mom_pp:+.2f} pp", f"{mom_pct:+.2f}%",
        f"{yoy_pp:+.2f} pp", f"{yoy_pct:+.2f}%"
    ]]

    analysis, sig = mortgage_rate_analysis(mom_pp, yoy_pp)
    return data, analysis, sig

def building_permits_analysis(mom_pct: float, yoy_pct: float):
    signal = 0

    if mom_pct > 3.0:
        txt = (f"Building permits rose {mom_pct:.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY) — strong forward signal.")
        signal += 3
    elif mom_pct > 0:
        txt = (f"Building permits edged up {mom_pct:.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY).")
        signal += 1
    elif mom_pct <= -3.0:
        txt = (f"Building permits fell {abs(mom_pct):.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY) — softer pipeline.")
        signal -= 3
    else:
        txt = (f"Building permits slipped {abs(mom_pct):.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY).")
        signal -= 1

    if yoy_pct > 0:
        signal += 1
    elif yoy_pct < 0:
        signal -= 1
    return txt, signal

def Building_Permits():
    fred = Fred(api_key="ef418abc7729096c77970a459e9d62dd")
    bp = fred.get_series("PERMIT").dropna()

    latest  = float(bp.iloc[-1])
    prev    = float(bp.iloc[-2])
    lysm    = float(bp.iloc[-13])

    mom_abs = latest - prev
    yoy_abs = latest - lysm
    mom_pct = (mom_abs / prev) * 100 if prev != 0 else 0.0
    yoy_pct = (yoy_abs / lysm) * 100 if lysm != 0 else 0.0

    data = [[
        f"{latest:,.0f}", bp.index[-1].strftime("%B %d, %Y"),
        f"{mom_abs:+,.0f}", f"{mom_pct:+.2f}%",
        f"{yoy_abs:+,.0f}", f"{yoy_pct:+.2f}%"
    ]]

    analysis, sig = building_permits_analysis(mom_pct, yoy_pct)
    return data, analysis, sig


def Real_Estate_Sector():
    macro_data_sign = 0
    output_data = []

    mort_data, mort_out, mort_sig = Mortgage_30Y()
    macro_data_sign += mort_sig

    perm_data, perm_out, perm_sig = Building_Permits()
    macro_data_sign += perm_sig

    output_data += mort_data + perm_data
    idx = ["30Y Mortgage Rate", "Building Permits"]

    df = pd.DataFrame(output_data, columns=GENERAL_Output_columns, index=idx)
    return mort_out, perm_out, df, macro_data_sign