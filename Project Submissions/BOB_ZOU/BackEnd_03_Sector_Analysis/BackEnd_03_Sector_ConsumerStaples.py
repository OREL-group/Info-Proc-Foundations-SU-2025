import pandas as pd
from fredapi import Fred
from datetime import datetime

GENERAL_Output_columns = pd.MultiIndex.from_tuples([
    (f"Latest Data", "Data"),
    (f"Latest Data", "Release Date"),

    ("MoM", "MoM Change"),
    ("MoM", "MoM Change Pct"),

    ("YoY", "YoY Change"),
    ("YoY", "YoY Change Pct")
])

def sticky_cpi_analysis(mom_pct: float, yoy_pct: float):
    sig = 0
    if mom_pct > 0.3:
        if yoy_pct > 0:
            txt = (f"Sticky CPI accelerated {mom_pct:.2f}% MoM "
                   f"and {yoy_pct:+.2f}% YoY, signalling persistent price pressure "
                   "in core consumer staples.")
            sig += 5
        else:
            txt = (f"Sticky CPI jumped {mom_pct:.2f}% MoM, but remains "
                   f"{abs(yoy_pct):.2f}% below last year—early sign of re-inflation.")
            sig += 3
    elif mom_pct > 0:
        txt = (f"Sticky CPI edged up {mom_pct:.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY). Inflation remains sticky but contained.")
        sig += (1 if yoy_pct > 0 else 0)
    elif mom_pct < 0:
        txt = (f"Sticky CPI slipped {abs(mom_pct):.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY). Price momentum is easing.")
        sig -= (1 if yoy_pct > 0 else 3)
    else:
        txt = (f"Sticky CPI was flat MoM "
               f"({yoy_pct:+.2f}% YoY). Inflation trend unclear.")
        sig -= 5
    return txt, sig

def ppi_analysis(mom_pct: float, yoy_pct: float):
    sig = 0
    if mom_pct > 1:
        txt = (f"PPI jumped {mom_pct:.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY), pointing to upstream cost pressure.")
        sig += (5 if yoy_pct > 0 else 3)
    elif mom_pct > 0:
        txt = (f"PPI rose {mom_pct:.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY). Costs drifting higher.")
        sig += (1 if yoy_pct > 0 else 0)
    elif mom_pct < 0:
        txt = (f"PPI fell {abs(mom_pct):.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY). Input prices easing.")
        sig -= (1 if yoy_pct > 0 else 3)
    else:
        txt = (f"PPI unchanged MoM "
               f"({yoy_pct:+.2f}% YoY).")
        sig -= 5
    return txt, sig

def Core_CPI():
    url = "https://www.atlantafed.org/-/media/documents/datafiles/research/inflationproject/stickprice/stickyprice.xlsx"
    xls = pd.read_excel(url).iloc[-13:][["Date", "Core Flexible CPI (monthly)", "1-mo annualized percent change.1", "12mo.1"]]
    xls["Date"] = pd.to_datetime(xls["Date"])
    latest = float(xls.iloc[-1, 1])
    prev = float(xls.iloc[-2, 1])
    lysm = float(xls.iloc[0, 1])

    mom_g  = latest - prev
    yoy_g  = latest - lysm
    mom_p     = float(xls.iloc[-1, 2])
    yoy_p     = float(xls.iloc[-1, 3])

    rel_date = (xls.iloc[-1, 0] + pd.offsets.MonthBegin(1)).strftime('%B, %Y')

    row = [[f"{latest:.5f}",
            rel_date,
            f"{mom_g:+.5f}", f"{mom_p:+.2f}%",
            f"{yoy_g:+.5f}", f"{yoy_p:+.2f}%"]]

    narrative, sig = sticky_cpi_analysis(mom_p, yoy_p)
    return row, narrative, sig

def PPI_All_Commodities():
    fred   = Fred(api_key="ef418abc7729096c77970a459e9d62dd")
    series = fred.get_series("PPIACO")
    ppi_df = series.to_frame(name="PPI")
    ppi_df.index.name = "Date"

    latest = ppi_df.iloc[-1, 0]
    prev   = ppi_df.iloc[-2, 0]
    lysm   = ppi_df.iloc[-13, 0]

    mom_g  = latest - prev
    yoy_g  = latest - lysm
    mom_p  = mom_g / prev * 100
    yoy_p  = yoy_g / lysm * 100

    # BLS usually publishes PPI on ~11-15th of next month
    rel_date = (ppi_df.index[-1] + pd.offsets.MonthBegin(1) + 
                pd.Timedelta(days=14)).strftime("%B %d, %Y")

    row = [[f"{latest:.1f}",
            rel_date,
            f"{mom_g:+.1f}", f"{mom_p:+.2f}%",
            f"{yoy_g:+.1f}", f"{yoy_p:+.2f}%"]]

    narrative, sig = ppi_analysis(mom_p, yoy_p)
    return row, narrative, sig

def Consumer_Staples_Sector():
    macro_data_sign = 0
    data_rows = []

    sc_row, sc_out, sc_sig = Core_CPI()
    macro_data_sign += sc_sig

    ppi_row, ppi_out, ppi_sig = PPI_All_Commodities()
    macro_data_sign += ppi_sig

    data_rows += sc_row + ppi_row
    idx = ["Core CPI", "PPI (All Commodities)"]

    df = pd.DataFrame(data_rows, columns=GENERAL_Output_columns, index=idx)
    return sc_out, ppi_out, df, macro_data_sign