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

def fedfunds_rate_analysis(mom_pp: float, yoy_pp: float):
    signal = 0
    if mom_pp <= -0.25:
        txt = (f"Fed funds eased {mom_pp:+.2f} pp MoM "
               f"({yoy_pp:+.2f} pp YoY), loosening financial conditions.")
        signal += 2
    elif -0.25 < mom_pp < 0:
        txt = (f"Fed funds dipped {mom_pp:+.2f} pp MoM "
               f"({yoy_pp:+.2f} pp YoY). Slightly supportive.")
        signal += 1
    elif 0 < mom_pp < 0.25:
        txt = (f"Fed funds rose {mom_pp:+.2f} pp MoM "
               f"({yoy_pp:+.2f} pp YoY). Mild headwind for credit demand.")
        signal -= 1
    elif mom_pp >= 0.25:
        txt = (f"Fed funds jumped {mom_pp:+.2f} pp MoM "
               f"({yoy_pp:+.2f} pp YoY), tightening conditions.")
        signal -= 2
    else:
        txt = (f"Fed funds unchanged MoM ({mom_pp:+.2f} pp), "
               f"{yoy_pp:+.2f} pp YoY. No directional shift.")
        signal += 0
    return txt, signal

def yield_curve_analysis(mom_pp: float, yoy_pp: float, latest_pp: float):
    signal = 0
    if mom_pp >= 0.25:
        txt = (f"Yield curve steepened {mom_pp:+.2f} pp MoM "
               f"to {latest_pp:+.2f} pp ({yoy_pp:+.2f} pp YoY).")
        signal += 2
    elif 0 < mom_pp < 0.25:
        txt = (f"Yield curve modestly steepened {mom_pp:+.2f} pp MoM "
               f"to {latest_pp:+.2f} pp ({yoy_pp:+.2f} pp YoY).")
        signal += 1
    elif -0.25 < mom_pp < 0:
        txt = (f"Yield curve slightly flattened {mom_pp:+.2f} pp MoM "
               f"to {latest_pp:+.2f} pp ({yoy_pp:+.2f} pp YoY).")
        signal -= 1
    elif mom_pp <= -0.25:
        txt = (f"Yield curve flattened {mom_pp:+.2f} pp MoM "
               f"to {latest_pp:+.2f} pp ({yoy_pp:+.2f} pp YoY).")
        signal -= 2
    else:
        txt = (f"Yield curve was flat MoM ({mom_pp:+.2f} pp) "
               f"at {latest_pp:+.2f} pp ({yoy_pp:+.2f} pp YoY).")

    if latest_pp > 0.50:
        txt += " Slope is clearly positive."
        signal += 1
    elif latest_pp < -0.50:
        txt += " Curve remains deeply inverted."
        signal -= 1
    return txt, signal

def Fed_Funds():
    fred = Fred(api_key="ef418abc7729096c77970a459e9d62dd")
    series = fred.get_series("FEDFUNDS")
    df = series.to_frame(name="Rate")
    df.index.name = "Date"

    latest      = float(df.iloc[-1, 0])
    prev        = float(df.iloc[-2, 0])
    lysm        = float(df.iloc[-13, 0])

    mom_growth  = latest - prev
    yoy_growth  = latest - lysm
    mom_pct     = (mom_growth / prev) * 100
    yoy_pct     = (yoy_growth / lysm) * 100

    data = [[f"{latest:.2f}%",
             df.index[-1].strftime("%B, %Y"),
             f"{mom_growth:+.2f} pp",
             f"{mom_pct:+.2f}%",
             f"{yoy_growth:+.2f} pp",
             f"{yoy_pct:+.2f}%"]]

    analysis, sig = fedfunds_rate_analysis(mom_growth, yoy_growth)
    return data, analysis, sig

def Yield_Curve():
    fred = Fred(api_key="ef418abc7729096c77970a459e9d62dd")
    series = fred.get_series("T10Y2Y")
    yc_df = series.to_frame(name="Spread")

    latest      = float(yc_df.iloc[-1, 0])
    prev        = float(yc_df.iloc[-2, 0])
    lysm        = float(yc_df.iloc[-13, 0])

    mom_growth  = latest - prev
    yoy_growth  = latest - lysm
    mom_pct     = (mom_growth / prev) * 100
    yoy_pct     = (yoy_growth / lysm) * 100

    data = [[
        f"{latest:+.2f} pp", yc_df.index[-1].strftime("%B %d, %Y"),
        f"{mom_growth:+.2f} pp", f"{mom_pct:+.2f}%",
        f"{yoy_growth:+.2f} pp", f"{yoy_pct:+.2f}%"
        ]]

    analysis, sig = yield_curve_analysis(mom_growth, yoy_growth, latest)
    return data, analysis, sig

def Financials_Sector():
    macro_data_sign = 0
    output_data = []

    ff_data, ff_out, ff_sig = Fed_Funds()
    macro_data_sign += ff_sig

    yc_data, yc_out, yc_sig = Yield_Curve()
    macro_data_sign += yc_sig

    output_data += ff_data + yc_data
    idx = ["Fed Funds Rate", "10Y-2Y Spread"]

    df = pd.DataFrame(output_data, columns=GENERAL_Output_columns, index=idx)
    return ff_out, yc_out, df, macro_data_sign