import csv
import requests
from datetime import datetime
import pandas as pd

api_key = "9THYPTW9AE1DRHYJ"

def standard_alpha_vantage(purpose, ticker, api_key = api_key):
    url = f"https://www.alphavantage.co/query?function={purpose}&symbol={ticker}&apikey={api_key}"
    r = requests.get(url)
    return r

def get_next_earnings_report_date(ticker, api_key = api_key):
    CSV_URL = f"https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=6month&apikey={api_key}"

    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    df = pd.DataFrame(cr)
    df = df.T.set_index(0).T.reset_index(drop=True).rename_axis(columns=None)
    df = df[df["symbol"] == ticker]["reportDate"]

    Next_Earnings_Report_date = datetime.strptime(df.iloc[0], "%Y-%m-%d").strftime("%B %d, %Y")
    return Next_Earnings_Report_date

def ER_table_1(ticker):
    YoY_QoQ = "INCOME_STATEMENT"
    ER_score = 0

    raw_YoY_QoQ = standard_alpha_vantage(YoY_QoQ, ticker)

    df = pd.DataFrame(raw_YoY_QoQ.json()["quarterlyReports"])

    for col in ["totalRevenue","grossProfit","netIncome"]:
        df[col] = df[col].astype(float)

    def compute_growth(s: pd.Series, periods: int):
        cur, prev = s.iloc[0], s.iloc[periods]
        cur = cur / (10 ** 6)
        prev = prev / (10 ** 6)
        abs_chg = cur - prev
        pct_chg = abs_chg / prev * 100
        return cur, abs_chg, pct_chg

    rev, rev_yoy, rev_yoy_pct = compute_growth(df["totalRevenue"], 4)
    gP, gP_yoy, gP_yoy_pct = compute_growth(df["grossProfit"], 4)
    netIncome, netIncome_yoy, netIncome_yoy_pct = compute_growth(df["netIncome"], 4)

    if rev_yoy_pct > 3:
        ER_score += 1
    elif rev_yoy_pct < -3:
        ER_score -= 2

    if (gP_yoy_pct > 3 and netIncome_yoy_pct > 0) or (gP_yoy_pct > 0 and netIncome_yoy_pct > 3):
        ER_score += 5
    elif gP_yoy_pct > 0 and netIncome_yoy_pct > 0:
        ER_score += 3
    elif gP_yoy_pct < 0:
        ER_score -= 5

    Table_1_data = [
        [rev,         rev_yoy,         rev_yoy_pct],
        [gP,          gP_yoy,          gP_yoy_pct],
        [netIncome,   netIncome_yoy,   netIncome_yoy_pct]
    ]

    Table_1_index       = ["Revenue", "Gross Profit", "Net Income"]
    Table_1_columns     = ["Current Data (in Million Dollars)", "YoY Δ (in Million Dollars)", "YoY %"]

    table_1 = pd.DataFrame(
        data=Table_1_data,
        index=Table_1_index,
        columns=Table_1_columns
    )

    table_1["Current Data (in Million Dollars)"] = table_1["Current Data (in Million Dollars)"].map(lambda x: f"{x:+,.0f}")
    table_1["YoY Δ (in Million Dollars)"] = table_1["YoY Δ (in Million Dollars)"].map(lambda x: f"{x:,.0f}")
    table_1["YoY %"] = table_1["YoY %"].map(lambda x: f"{x:+.2f}%")

    return table_1, ER_score

def EPS_table_2(ticker):
    EPS_score = 0
    url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey=9THYPTW9AE1DRHYJ'
    r = requests.get(url)
    data = r.json()

    df = pd.DataFrame(data["quarterlyEarnings"])
    df.iloc[0,:]

    last_report_date = datetime.strptime(df.iloc[0,1], "%Y-%m-%d").strftime("%B %d, %Y")
    reportedEPS = df.iloc[0,2]
    last_estimatedEPS = df.iloc[0,3]
    surprise = float(df.iloc[0,4])
    surprisePCT = float(df.iloc[0,5])

    if surprise > 0:
        EPS_output = f"EPS BEATS expectation by {surprise} ({surprisePCT:+.2f}%)."
        EPS_score += 1
    elif surprise == 0:
        EPS_output = f"EPS MEETS expectation."
    else:
        EPS_output = f"EPS MISSES expectation by {surprise} ({surprisePCT:+.2f}%)"
        EPS_score -= 1

    Table_2_data = [
            [reportedEPS, last_estimatedEPS, last_report_date, EPS_output]
        ]

    Table_2_columns = ["Last Reported EPS", "Estimated EPS", "Last Reported Date", "Expectations Result"]

    Table_2_index = [f"Non-GAAP"]

    table_2 = pd.DataFrame(data=Table_2_data, columns=Table_2_columns, index=Table_2_index)
    return table_2, EPS_score

def earnings_outlook(er_score: int, eps_score: int) -> tuple[str, str]:
    if er_score > 4 and eps_score > 0:
        output_line = f"Strong Earnings Across the Board, Momentum looks strong — this may be a good time to enter or add to your position."
        output_score = 2
    elif er_score > 4 and eps_score < 0:
        output_line = f"Strong Operational Growth. Though EPS MISSED, fundamentals are solid, but the market may wait for clearer earnings execution — proceed with moderate confidence."
        output_score = 1
    elif er_score > 4 and eps_score == 0:
        output_line = f"Strong Operational Growth. Fundamentals are solid, but the market may wait for clearer earnings execution — proceed with moderate confidence."
        output_score = 0
    elif er_score <= 4 and eps_score > 0:
        output_line = f"EPS Surprise Despite Tepid Top-Line Growth. Short-term optimism possible, but be cautious — underlying growth is not yet convincing."
        output_score = -1
    else:
        output_line = f"Weak Overall Earnings Performance. Earnings trends are soft — consider holding off, review your risk exposure before entering or even short."
        output_score = -2
    return output_line, output_score
