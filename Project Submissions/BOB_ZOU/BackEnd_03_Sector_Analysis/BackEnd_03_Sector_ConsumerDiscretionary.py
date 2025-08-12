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

def umich_sentiment_analysis(mom_pct: float, yoy_pct: float):
    signal = 0
    if mom_pct > 3:
        if yoy_pct > 0:
            txt = (f"Consumer sentiment is surging, up {mom_pct:.2f}% MoM and "
                   f"{yoy_pct:.2f}% YoY—pointing to solid discretionary spending ahead.")
            signal += 5
        else:
            txt = (f"Sentiment jumped {mom_pct:.2f}% MoM but remains "
                   f"{abs(yoy_pct):.2f}% below last year—early rebound signs.")
            signal += 3
    elif mom_pct > 0:
        txt = (f"Sentiment eked out a {mom_pct:.2f}% MoM gain "
               f"({yoy_pct:+.2f}% YoY), signalling steady but unspectacular demand.")
        signal += (1 if yoy_pct > 0 else 0)
    elif mom_pct < 0:
        txt = (f"Sentiment slipped {abs(mom_pct):.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY). Consumers look more cautious.")
        signal -= (1 if yoy_pct > 0 else 3)
    else:
        txt = (f"Sentiment was flat MoM ({mom_pct:.2f}%), "
               f"{yoy_pct:+.2f}% YoY. Direction still unclear.")
        signal -= 5
    return txt, signal

def retail_sales_analysis(mom_pct: float, yoy_pct: float):
    signal = 0
    if mom_pct > 2:
        txt = (f"Retail sales rose {mom_pct:.2f}% MoM "
               f"and {yoy_pct:+.2f}% YoY, underscoring healthy consumer outlays.")
        signal += (5 if yoy_pct > 0 else 3)
    elif mom_pct > 0:
        txt = (f"Retail sales inched up {mom_pct:.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY). Growth continues, albeit slower.")
        signal += (1 if yoy_pct > 0 else 0)
    elif mom_pct < 0:
        txt = (f"Retail sales fell {abs(mom_pct):.2f}% MoM "
               f"({yoy_pct:+.2f}% YoY). Momentum is fading.")
        signal -= (1 if yoy_pct > 0 else 3)
    else:
        txt = (f"Retail sales were unchanged MoM "
               f"({yoy_pct:+.2f}% YoY). Watch for next print.")
        signal -= 5
    return txt, signal

def UMich_Sentiment():
    url = "https://www.sca.isr.umich.edu/files/tbcics.csv"
    raw = pd.read_csv(url)
    raw = raw.dropna(how='all').iloc[1:].iloc[:, 0:5]
    raw.columns = ["DATE OF SURVEY", "YEAR", "?", "??", "INDEX OF CONSUMER SENTIMENT"]
    df = raw[["DATE OF SURVEY", "YEAR", "INDEX OF CONSUMER SENTIMENT"]].reset_index(drop=True)
    df["Survey_Date"] = pd.to_datetime(df["DATE OF SURVEY"] + " " + df["YEAR"].astype(int).astype(str), format="%B %Y")
    df["DATA RELEASE DATE"] = (df["Survey_Date"] + pd.offsets.MonthBegin(1)).dt.strftime("%B %d, %Y")
    df = df.drop(columns=["Survey_Date"])

    latest = float(df.iloc[-1, 2])
    prev = float(df.iloc[-2, 2])
    lysm = float(df.iloc[0, 2])
    
    mom_growth  = latest - prev
    yoy_growth  = latest - lysm
    mom_pct     = mom_growth / prev  * 100
    yoy_pct     = yoy_growth / lysm * 100

    data = [[f"{latest:.1f}",
             df.iloc[-1, 3],
             f"{mom_growth:+.1f}",
             f"{mom_pct:+.2f}%",
             f"{yoy_growth:+.1f}",
             f"{yoy_pct:+.2f}%"]]

    analysis, sig = umich_sentiment_analysis(mom_pct, yoy_pct)
    return data, analysis, sig

def Retail_Sales():
    fred = Fred(api_key="ef418abc7729096c77970a459e9d62dd")
    series = fred.get_series("RSAFS")
    rs_df  = series.to_frame(name="Sales")
    rs_df.index.name = "Date"

    latest      = rs_df.iloc[-1, 0]
    prev        = rs_df.iloc[-2, 0]
    lysm        = rs_df.iloc[-13, 0]

    mom_growth  = latest - prev
    yoy_growth  = latest - lysm
    mom_pct     = mom_growth / prev  * 100
    yoy_pct     = yoy_growth / lysm * 100

    data = [[f"{latest:,.0f}",
             rs_df.index[-1].strftime("%b, %Y"),
             f"{mom_growth:+,.0f}",
             f"{mom_pct:+.2f}%",
             f"{yoy_growth:+,.0f}",
             f"{yoy_pct:+.2f}%"]]

    analysis, sig = retail_sales_analysis(mom_pct, yoy_pct)
    return data, analysis, sig

def Consumer_Discretionary_Sector():
    macro_data_sign = 0
    output_data = []

    um_data, um_out, um_sig = UMich_Sentiment()
    macro_data_sign += um_sig

    rs_data, rs_out, rs_sig = Retail_Sales()
    macro_data_sign += rs_sig

    output_data += um_data + rs_data
    idx = ["UMich Sentiment", "Retail Sales"]

    df = pd.DataFrame(output_data, columns=GENERAL_Output_columns, index=idx)
    return um_out, rs_out, df, macro_data_sign