import pandas as pd
from datetime import datetime, timedelta
import requests
import time

# Part 2 of Project IS 430:

FMP_TO_GICS = {
    "Basic Materials":       "Materials",
    "Communication Services":"Communication Services",
    "Consumer Cyclical":     "Consumer Discretionary",
    "Consumer Defensive":    "Consumer Staples",
    "Energy":                "Energy",
    "Financial Services":    "Financials",
    "Healthcare":            "Health Care",
    "Industrials":           "Industrials",
    "Real Estate":           "Real Estate",
    "Technology":            "Information Technology",
    "Utilities":             "Utilities"
}

SECTOR_LEADERS = {
    "Communication Services": ["META", "GOOGL", "TMUS", "VZ"],
    "Consumer Discretionary": ["AMZN", "TSLA", "F", "HD"],
    "Consumer Staples": ["COST", "PG", "WMT", "KO"],
    "Energy": ["XOM", "CVX", "COP", "SLB"],
    "Financials": ["JPM", "BAC", "GS", "MS"],
    "Health Care": ["JNJ", "PFE", "UNH", "ABBV"],
    "Industrials": ["GE", "HON", "UPS", "CAT"],
    "Information Technology": ["AAPL", "MSFT", "NVDA", "PLTR"], 
    "Materials": ["NEM", "LIN", "APD", "FCX"],
    "Real Estate": ["PLD", "SPG", "CCI", "O"],
    "Utilities": ["NEE", "DUK", "SO", "EXC"] 
}

def get_sector(ticker):
    alpha_url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey=9THYPTW9AE1DRHYJ"
    alpha_CIK = requests.get(alpha_url).json()["CIK"]
    CIK_to_FMP_url = f"https://financialmodelingprep.com/stable/profile-cik?cik={alpha_CIK}&apikey=ctaFTNC4FkIV3kxvxBWMVimtV786oI0A"
    FMP = pd.DataFrame(requests.get(CIK_to_FMP_url).json())["sector"].values.item()
    GICS_sector_key = FMP_TO_GICS.get(FMP, None)
    return GICS_sector_key

def Companies_in_Same_Sector_for_comparison(ticker):
    GICS_sector_key = get_sector(ticker)

    if GICS_sector_key in SECTOR_LEADERS:
        companies_in_same_sector = SECTOR_LEADERS[GICS_sector_key]
        if ticker in companies_in_same_sector:
            companies_to_compare =  [t for t in companies_in_same_sector if t != ticker]
        else:
            companies_to_compare = companies_in_same_sector[:3]
        return companies_to_compare
    else:
        return f"SOMETHING WENT WRONG"

def sector_1d_comparison(ticker):
    same_sector = Companies_in_Same_Sector_for_comparison(ticker)
    tickers     = [ticker] + same_sector
    raw = {}
    for TI in tickers:
        INTRADAY_url = (
            f"https://www.alphavantage.co/query"
            f"?function=TIME_SERIES_INTRADAY"
            f"&symbol={TI}"
            f"&interval=5min"
            f"&entitlement=delayed"
            f"&apikey=9THYPTW9AE1DRHYJ"
        )
        resp = requests.get(INTRADAY_url)
        data = resp.json()
        ts_key = "Time Series (5min)"
        ts     = data.get(ts_key, {})
        df = pd.DataFrame.from_dict(ts, orient="index")
        df.index = pd.to_datetime(df.index)
        df.columns = [col.split(". ")[1].lower().capitalize() for col in df.columns]
        raw[TI] = df.sort_index().astype(float)

        time.sleep(0.3)

    rows = []
    rows_compare = []
    for sym in tickers:
        df = raw[sym]

        open_p = df["Open"].iloc[0]
        last_p = df["Close"].iloc[-1]
        pct = (last_p - open_p) / open_p * 100

        group = "Target" if sym == ticker else "Same Sector"
        rows.append((group, sym, open_p, last_p, f"{pct:+.3f}"))
        rows_compare.append((group, sym, pct))
    
    result = pd.DataFrame(rows, columns=["Group", "Ticker", "Open", "Last", "1D % Change"])
    result = result.sort_values(["Group","1D % Change"], ascending=[True, False]).reset_index(drop=True)

    for_analysis = pd.DataFrame(rows_compare, columns=["Group", "Ticker", "1D % Change"])

    target_pct = for_analysis.loc[for_analysis["Ticker"] == ticker, "1D % Change"].iat[0]
    comparison_pct = for_analysis[for_analysis["Group"] == "Same Sector"]

    q75 = comparison_pct["1D % Change"].quantile(0.75)
    q25 = comparison_pct["1D % Change"].quantile(0.25)

    if target_pct >= q75:
        status = "Leading"
        same_sector_performance = +3
        text = (
            f"{ticker} is outperforming its same‐sector peers with a 1D return of "
            f"{target_pct:.2f}%, placing it in the top quartile of sector performance."
        )
    elif target_pct <= q25:
        status = "Underperforming"
        same_sector_performance = -3
        text = (
            f"{ticker} is underperforming its same‐sector peers with a 1D return of "
            f"{target_pct:.2f}%, ranking in the bottom quartile."
        )
    else:
        status = "In-Line"
        same_sector_performance = 0
        text = (
            f"{ticker} is moving in‐line with its same‐sector peers, with a 1D return "
            f"of {target_pct:.2f}% (between the 25th and 75th percentile)."
        )

    return result, status, same_sector_performance, text
