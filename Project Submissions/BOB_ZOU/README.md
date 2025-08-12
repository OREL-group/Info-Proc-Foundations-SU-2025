# Bob Zou's IS 430 Final Project (SU25) – Stock Market Analytics

A Streamlit app that unifies **Earnings**, **Sector Performance**, and **Macro Data** into a single playbook for any U.S. equity. 
It fetches (maximum) 15-minute delayed data from **Alpha Vantage** and **FRED**, builds sector‑aware macro tables, and produces an **actionable trade plan**.

> Default position size in the UI is **100 shares** (editable). Intraday price uses Alpha Vantage’s 1‑minute data (15‑minute delay per your key tier).

---

## Quick Start

```bash
# 1) Python 3.10+ recommended
python -V

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run the app
streamlit run FrontEnd.py
```

**Environment variables**
- `ALPHAVANTAGE_API_KEY` (required): used for earnings, fundamentals, intraday prices, and BTC pricing.
- `FRED_API_KEY` (optional but recommended): used for macro indicators across sectors.

---

## Project Structure (top level)

```
FrontEnd.py                      # Streamlit UI (4 sections: Earnings → Sector Perf → Macro → Playbook)
BackEnd_01_Earnings.py           # Earnings tables (YoY/QoQ) + EPS surprise + next ER date + outlook
BackEnd_02_Sector_Performance.py # Sector lookup + 1D same‑sector comparison vs leaders
BackEnd_03_Macro_Data.py         # Dispatcher: routes to the proper sector module and returns (line1, line2, df, signal_text, score)
BackEnd_04_Playbook.py           # Aggregates scores and produces a simple trade plan
BackEnd_03_Sector_*.py           # One file per GICS sector (see mapping below)
README.md
requirements.txt
```

---

## Data Sources

- **Alpha Vantage**: Earnings time series, company overview, intraday prices, and **BTC daily** (Digital Currency Daily).  
- **FRED**: Rate policy, production, PPI/CPI, IP and other macro series for sector‑specific context.
  - Note: Some FRED daily series are **end‑of‑day** and can lag ~1 business day; weekly/monthly series post on release cadence.

**Rate limits**
- Alpha Vantage free tier is rate‑limited. The app keeps calls minimal but during a rapid demo, **avoid spamming multiple tickers** back‑to‑back.

---

## Sector Modules & Indicators

Each sector module returns `(line1, line2, df, signal_int)`; the dispatcher maps `signal_int` to **signal_text** and a coarse **score**.  
All data tables share the same columns:
`("Latest Data","Data")`, `("Latest Data","Release Date")`, `("MoM","MoM Change")`, `("MoM","MoM Change Pct")`, `("YoY","YoY Change")`, `("YoY","YoY Change Pct")`.

| Sector | Module | Row 1 | Row 2 |
|---|---|---|---|
| **Consumer Discretionary** | `BackEnd_03_Sector_ConsumerDiscretionary.py` | **UMich Sentiment** | **Retail Sales (RSAFS)** |
| **Consumer Staples** | `BackEnd_03_Sector_ConsumerStaples.py` | **Core/Sticky CPI** | **PPI** |
| **Industrials** | `BackEnd_03_Sector_Industrials.py` | **Durable Goods** | **Industrial Production (INDPRO)** |
| **Financials** | `BackEnd_03_Sector_Financials.py` | **Fed Funds (FEDFUNDS)** | **Yield Curve 10y–2y** |
| **Information Technology** | `BackEnd_03_Sector_InformationTechnology.py` | **Bitcoin (AV, 30d & d/d)** | **Semis IP – NAICS 3344** |
| **Materials** | `BackEnd_03_Sector_Materials.py` | **Copper** | **Primary Metals IP** |
| **Real Estate** | `BackEnd_03_Sector_RealEstate.py` | **30Y Mortgage Rate** | **Building Permits** |
| **Utilities** | `BackEnd_03_Sector_Utilities.py` | **WTI** | **CPI: Electricity** |
| **Health Care** | `BackEnd_03_Sector_HealthCare.py` | **CPI: Medical Care** | **All Employees: HC & Social Assistance** |
| **Communication Services** | `BackEnd_03_Sector_CommunicationServices.py` | **PPI: Internet Publishing & Web Search** | **IP: Telecommunications (IPG517S)** |
| **Energy** | `BackEnd_03_Sector_Energy.py` | **Brent Crude** | **Henry Hub Nat Gas** |

**Notes**
- IT module appends a fixed line to explain BTC’s role:  
  *“BTC (Bitcoin) acts as a liquidity/risk‑appetite proxy; during risk‑on phases, flows into high‑beta tech (and semis) rise alongside crypto, pushing positive short‑run correlation.”*
- “30d & d/d” rows place **30‑day change** in the MoM columns and **day‑over‑day change** in the YoY columns (labeled “Day to Day”).

---

## Scoring & Narratives

- Each indicator contributes an integer **signal** (supportive vs headwind) based on MoM/YoY thresholds tailored to the series.
- The dispatcher converts that into a human‑readable **signal_text** + **score** for the **Playbook**.

---

## Running the Demo

1. Enter a ticker (e.g., `AAPL`, `JPM`, `XOM`).  
2. The app:
   - Builds **Earnings** tables (YoY/QoQ and EPS surprise).
   - Compares **Sector Performance** vs leaders (e.g., IT includes PLTR; Comm Services: META, GOOGL, TMUS, VZ).
   - Loads **Macro Data** for the detected GICS sector using the module above.
   - Aggregates to an **Actionable Playbook** with a short recommendation.

If a data source times out or a series is unavailable, the table shows **“—”** with a neutral signal and a brief note.

---

## License / Attribution

- Data provided by **Alpha Vantage** and **FRED**. Please respect their terms of use.
- For course/demo purposes.

---

## Disclaimer

**Nothing here is financial, investment, legal, or tax advice.**
