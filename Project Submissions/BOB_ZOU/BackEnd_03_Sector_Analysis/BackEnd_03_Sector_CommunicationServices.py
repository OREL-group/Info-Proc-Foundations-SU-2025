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

def internet_ppi_analysis(mom_pct: float, yoy_pct: float):
    signal = 0
    if mom_pct > 0.50:
        txt = (f"PPI (Internet Publishing & Web Search) rose {mom_pct:.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY) — firm pricing power.")
        signal += 3
    elif mom_pct > 0:
        txt = (f"PPI (Internet Publishing & Web Search) edged up {mom_pct:.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY).")
        signal += 1
    elif mom_pct <= -0.50:
        txt = (f"PPI (Internet Publishing & Web Search) fell {abs(mom_pct):.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY) — softer pricing.")
        signal -= 3
    else:
        txt = (f"PPI (Internet Publishing & Web Search) slipped {abs(mom_pct):.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY).")
        signal -= 1

    if   yoy_pct > 0: signal += 1
    elif yoy_pct < 0: signal -= 1

    return txt, signal


def Internet_PPI():
    fred = Fred(api_key="ef418abc7729096c77970a459e9d62dd")
    internet = fred.get_series("PCU519130519130").dropna()

    latest   = float(internet.iloc[-1])
    prev     = float(internet.iloc[-2])
    lysm     = float(internet.iloc[-13])

    mom_abs  = latest - prev
    yoy_abs  = latest - lysm
    mom_pct  = (mom_abs / prev) * 100 if prev  != 0 else 0.0
    yoy_pct  = (yoy_abs / lysm) * 100 if lysm != 0 else 0.0

    data = [[
        f"{latest:.2f}", internet.index[-1].strftime("%b, %Y"),
        f"{mom_abs:+.2f}", f"{mom_pct:+.2f}%",
        f"{yoy_abs:+.2f}", f"{yoy_pct:+.2f}%"
    ]]

    analysis, sig = internet_ppi_analysis(mom_pct, yoy_pct)
    return data, analysis, sig


def info_broadcast_telecom_ip_analysis(mom_pct: float, yoy_pct: float):
    signal = 0
    if mom_pct > 1.0:
        txt = (f"IP (Broadcasting/Telecom proxy) rose {mom_pct:.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY) — constructive activity.")
        signal += 3
    elif mom_pct > 0:
        txt = (f"IP (Broadcasting/Telecom proxy) edged up {mom_pct:.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY).")
        signal += 1
    elif mom_pct <= -1.0:
        txt = (f"IP (Broadcasting/Telecom proxy) fell {abs(mom_pct):.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY) — softer backdrop.")
        signal -= 3
    else:
        txt = (f"IP (Broadcasting/Telecom proxy) slipped {abs(mom_pct):.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY).")
        signal -= 1

    if   yoy_pct > 0: signal += 1
    elif yoy_pct < 0: signal -= 1

    return txt, signal


def Info_Broadcasting_Telecom_IP():
    fred = Fred(api_key="ef418abc7729096c77970a459e9d62dd")

    try:
        df = fred.get_series("IPG517S").dropna()
        label = "IP: Telecommunications (NAICS 517)"
    except Exception:
        df = fred.get_series("IPG515S").dropna()
        label = "IP: Broadcasting (NAICS 515)"

    latest   = float(df.iloc[-1])
    prev     = float(df.iloc[-2])
    lysm     = float(df.iloc[-13])

    mom_abs  = latest - prev
    yoy_abs  = latest - lysm
    mom_pct  = (mom_abs / prev) * 100 if prev  != 0 else 0.0
    yoy_pct  = (yoy_abs / lysm) * 100 if lysm != 0 else 0.0

    data = [[
        f"{latest:.2f}", df.index[-1].strftime("%b, %Y"),
        f"{mom_abs:+.2f}", f"{mom_pct:+.2f}%",
        f"{yoy_abs:+.2f}", f"{yoy_pct:+.2f}%"
    ]]

    analysis, sig = info_broadcast_telecom_ip_analysis(mom_pct, yoy_pct)
    return label, data, analysis, sig


def Communication_Services_Sector():
    macro_data_sign = 0
    output_data = []

    ppi_data, ppi_out, ppi_sig = Internet_PPI()
    macro_data_sign += ppi_sig

    ip_label, ip_data, ip_out, ip_sig = Info_Broadcasting_Telecom_IP()
    macro_data_sign += ip_sig

    output_data += ppi_data + ip_data
    idx = ["PPI: Internet Publishing & Web Search", ip_label]

    df = pd.DataFrame(output_data, columns=GENERAL_Output_columns, index=idx)

    return ppi_out, ip_out, df, macro_data_sign
