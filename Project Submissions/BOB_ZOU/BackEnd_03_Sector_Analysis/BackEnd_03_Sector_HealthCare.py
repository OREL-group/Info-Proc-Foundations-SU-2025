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

def medical_care_cpi_analysis(mom_pct: float, yoy_pct: float):
    signal = 0
    if mom_pct <= -0.5:
        txt = (f"CPI: Medical Care fell {abs(mom_pct):.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY) — cost pressure easing.")
        signal += 2
    elif -0.5 < mom_pct < 0:
        txt = (f"CPI: Medical Care dipped {abs(mom_pct):.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY).")
        signal += 1
    elif 0 < mom_pct < 0.5:
        txt = (f"CPI: Medical Care rose {mom_pct:.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY).")
        signal -= 1
    else:  # ≥ +0.5
        txt = (f"CPI: Medical Care jumped {mom_pct:.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY) — potential margin headwind.")
        signal -= 2

    if yoy_pct < 0:
        signal += 1
    elif yoy_pct > 0:
        signal -= 1

    return txt, signal

def Medical_Care_CPI():
    fred = Fred(api_key="ef418abc7729096c77970a459e9d62dd")
    hc_cpi = fred.get_series("CPIMEDSL").dropna()

    latest   = float(hc_cpi.iloc[-1])
    prev     = float(hc_cpi.iloc[-2])
    lysm     = float(hc_cpi.iloc[-13])

    mom_abs  = latest - prev
    yoy_abs  = latest - lysm
    mom_pct  = (mom_abs / prev) * 100 if prev  != 0 else 0.0
    yoy_pct  = (yoy_abs / lysm) * 100 if lysm != 0 else 0.0

    data = [[
        f"{latest:.2f}", hc_cpi.index[-1].strftime("%b, %Y"),
        f"{mom_abs:+.2f}", f"{mom_pct:+.2f}%",
        f"{yoy_abs:+.2f}", f"{yoy_pct:+.2f}%"
    ]]

    analysis, sig = medical_care_cpi_analysis(mom_pct, yoy_pct)
    return data, analysis, sig

def hc_employment_analysis(mom_pct: float, yoy_pct: float):
    signal = 0
    if mom_pct > 0.30:
        txt = (f"Health Care & Social Assistance employment rose {mom_pct:.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY) — strong utilization.")
        signal += 3
    elif mom_pct > 0:
        txt = (f"Health Care & Social Assistance employment edged up {mom_pct:.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY).")
        signal += 1
    elif mom_pct <= -0.30:
        txt = (f"Health Care & Social Assistance employment fell {abs(mom_pct):.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY) — softer backdrop.")
        signal -= 3
    else:
        txt = (f"Health Care & Social Assistance employment slipped {abs(mom_pct):.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY).")
        signal -= 1

    if yoy_pct > 0:
        signal += 1
    elif yoy_pct < 0:
        signal -= 1

    return txt, signal

def HealthCare_Employment():
    fred = Fred(api_key="ef418abc7729096c77970a459e9d62dd")
    HC_E = fred.get_series("CES6562000001").dropna()

    latest   = float(HC_E.iloc[-1])
    prev     = float(HC_E.iloc[-2])
    lysm     = float(HC_E.iloc[-13])

    mom_abs  = latest - prev
    yoy_abs  = latest - lysm
    mom_pct  = (mom_abs / prev) * 100 if prev  != 0 else 0.0
    yoy_pct  = (yoy_abs / lysm) * 100 if lysm != 0 else 0.0

    data = [[
        f"{latest:,.0f}", HC_E.index[-1].strftime("%b, %Y"),
        f"{mom_abs:+,.0f}", f"{mom_pct:+.2f}%",
        f"{yoy_abs:+,.0f}", f"{yoy_pct:+.2f}%"
    ]]

    analysis, sig = hc_employment_analysis(mom_pct, yoy_pct)
    return data, analysis, sig


def Health_Care_Sector():
    macro_data_sign = 0
    output_data = []

    cpi_data, cpi_out, cpi_sig = Medical_Care_CPI()
    macro_data_sign += cpi_sig

    emp_data, emp_out, emp_sig = HealthCare_Employment()
    macro_data_sign += emp_sig

    output_data += cpi_data + emp_data
    idx = ["CPI: Medical Care", "HC Employment (Thousands)"]

    df = pd.DataFrame(output_data, columns=GENERAL_Output_columns, index=idx)

    healthcare_note = "**POLICY RISK WATCH:** Track executive/legislative actions (e.g., revisions to the ACA) and related litigation; incorporate scenario and sensitivity analyses accordingly."
    emp_out += + "\n" + "\n" + healthcare_note

    return cpi_out, emp_out, df, macro_data_sign
