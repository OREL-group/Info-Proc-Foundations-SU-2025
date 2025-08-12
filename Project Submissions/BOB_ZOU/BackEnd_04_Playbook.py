from BackEnd_01_Earnings import ER_table_1, EPS_table_2, earnings_outlook
from BackEnd_02_Sector_Performance import sector_1d_comparison
from BackEnd_03_Macro_Data import macro_data_analysis

ticker = "GOOGL"

def get_signal_scores(ticker):
    _, er_score = ER_table_1(ticker)
    _, eps_score = EPS_table_2(ticker)
    _, s_earn = earnings_outlook(er_score, eps_score)

    _, _, signal, _ = sector_1d_comparison(ticker)
    if signal == 3:
        s_sect = 2
    elif signal == -3:
        s_sect = -2
    else:
        s_sect = 0

    _, _, _, _, s_macro = macro_data_analysis(ticker)

    return s_earn, s_sect, s_macro

def get_trade_plan(ticker, shares = 100):
    s_earn, s_sect, s_macro = get_signal_scores(ticker)

    final_score = s_earn + s_sect + s_macro

    if final_score >= 3:
        scenario = "Bullish"
    elif final_score <= -3:
        scenario = "Bearish"
    else:
        scenario = "Neutral"

    if scenario == "Bullish":
        if shares >= 100:
            plan = (
                "Sell 2-week OTM puts to enhance returns. (No Protection, Risky, but Maximize Gain)"
                + "\n" 
                + "\n" 
                + "\n" 
                + "__OR__ Sell 1-month OTM call to enhance returns while capping upside"
            )
        else:
            plan = (
                "Purchase call options for leveraged exposure, or accumulate shares up to 100 then sell covered calls."
            )
    elif scenario == "Bearish":
        if shares >= 100:
            plan = (
                "Buy protective puts or establish a zero-cost collar on your 100-share lot to limit downside."
            )
        else:
            plan = (
                "Buy put options to hedge or speculate on declines; defer new long entries until signals improve."
            )
    else:
        plan = (
            "Hold and generate income through selling OTM calls or balanced option spreads (iron condors, etc.)."
        )

    return scenario, plan