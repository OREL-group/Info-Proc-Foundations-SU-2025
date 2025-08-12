import pandas as pd
from fredapi import Fred
from datetime import datetime, timedelta

from BackEnd_02_Sector_Performance import get_sector

from BackEnd_03_Sector_Analysis.BackEnd_03_Sector_Industrials import Industrial_Sector_Company
from BackEnd_03_Sector_Analysis.BackEnd_03_Sector_ConsumerDiscretionary import Consumer_Discretionary_Sector
from BackEnd_03_Sector_Analysis.BackEnd_03_Sector_ConsumerStaples import Consumer_Staples_Sector
from BackEnd_03_Sector_Analysis.BackEnd_03_Sector_Financials import Financials_Sector
from BackEnd_03_Sector_Analysis.BackEnd_03_Sector_InformationTechnology import Information_Technology_Sector
from BackEnd_03_Sector_Analysis.BackEnd_03_Sector_Materials import Materials_Sector
from BackEnd_03_Sector_Analysis.BackEnd_03_Sector_RealEstate import Real_Estate_Sector
from BackEnd_03_Sector_Analysis.BackEnd_03_Sector_Utilities import Utilities_Sector
from BackEnd_03_Sector_Analysis.BackEnd_03_Sector_HealthCare import Health_Care_Sector
from BackEnd_03_Sector_Analysis.BackEnd_03_Sector_CommunicationServices import Communication_Services_Sector
from BackEnd_03_Sector_Analysis.BackEnd_03_Sector_Energy import Energy_Sector

# Part 3 of Project IS 430:

list_of_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


GENERAL_Output_columns = pd.MultiIndex.from_tuples([
    (f"Latest Data", "Data"),
    (f"Latest Data", "Release Date"),

    ("MoM", "MoM Change"),
    ("MoM", "MoM Change Pct"),

    ("YoY", "YoY Change"),
    ("YoY", "YoY Change Pct")
])

macro_data_sign = 0





# Function for Output

def macro_data_analysis(ticker):
    sector = get_sector(ticker)

    if sector == "Materials": #1
        Output_Line1, Output_Line2, df, signal = Materials_Sector()
        macro_data_analysis_output1 = Output_Line1
        macro_data_analysis_output2 = Output_Line2
        macro_data_analysis_output_df = df
    
    elif sector == "Communication Services": #2
        Output_Line1, Output_Line2, df, signal = Communication_Services_Sector()
        macro_data_analysis_output1 = Output_Line1
        macro_data_analysis_output2 = Output_Line2
        macro_data_analysis_output_df = df
    
    elif sector == "Consumer Discretionary": #3
        Output_Line1, Output_Line2, df, signal = Consumer_Discretionary_Sector()
        macro_data_analysis_output1 = Output_Line1
        macro_data_analysis_output2 = Output_Line2
        macro_data_analysis_output_df = df
    
    elif sector == "Consumer Staples": #4
        Output_Line1, Output_Line2, df, signal = Consumer_Staples_Sector()
        macro_data_analysis_output1 = Output_Line1
        macro_data_analysis_output2 = Output_Line2
        macro_data_analysis_output_df = df
    
    elif sector == "Energy": #5
        Output_Line1, Output_Line2, df, signal = Energy_Sector()
        macro_data_analysis_output1 = Output_Line1
        macro_data_analysis_output2 = Output_Line2
        macro_data_analysis_output_df = df
    
    elif sector == "Financials": #6
        Output_Line1, Output_Line2, df, signal = Financials_Sector()
        macro_data_analysis_output1 = Output_Line1
        macro_data_analysis_output2 = Output_Line2
        macro_data_analysis_output_df = df

    elif sector == "Health Care": #7
        Output_Line1, Output_Line2, df, signal = Health_Care_Sector()
        macro_data_analysis_output1 = Output_Line1
        macro_data_analysis_output2 = Output_Line2
        macro_data_analysis_output_df = df

    elif sector == "Industrials": #8
        Output_Line1, Output_Line2, df, signal = Industrial_Sector_Company()
        macro_data_analysis_output1 = Output_Line1
        macro_data_analysis_output2 = Output_Line2
        macro_data_analysis_output_df = df
    
    elif sector == "Real Estate": #9
        Output_Line1, Output_Line2, df, signal = Real_Estate_Sector()
        macro_data_analysis_output1 = Output_Line1
        macro_data_analysis_output2 = Output_Line2
        macro_data_analysis_output_df = df

    elif sector == "Information Technology": #10
        Output_Line1, Output_Line2, df, signal = Information_Technology_Sector()
        macro_data_analysis_output1 = Output_Line1
        macro_data_analysis_output2 = Output_Line2
        macro_data_analysis_output_df = df

    elif sector == "Utilities": #11
        Output_Line1, Output_Line2, df, signal = Utilities_Sector()
        macro_data_analysis_output1 = Output_Line1
        macro_data_analysis_output2 = Output_Line2
        macro_data_analysis_output_df = df


    Default = f"Market Expectation: "
    if signal == 10 or signal == 8:
        signal_output = (Default + f"Very Good. \n" + "\n" + f"Industrial macro indicators are firing on all cylinders. Robust order books and rising capacity utilisation point to continued revenue tailwinds and margin support across the sector.")
        score = 2
    elif signal in [6, 5, 4]:
        signal_output = (Default + f"Good. \n" + "\n" + f"Key macro metrics show healthy – though moderating – growth. The backdrop remains constructive, but monitor upcoming releases for signs of cooling demand.")
        score = 1
    elif signal in [3, 2, 1, 0, -1, -2, -3]:
        signal_output = (Default + f"Give It Some Time. \n" + "\n" + f"Signals are mixed. A stabilisation phase could be forming, but you’ll want confirmation from next month’s Durable-Goods and INDPRO prints.")
        score = 0
    elif signal in [-4, -5, -6]:
        signal_output = (Default + f"Bad. \n" + "\n" + f"Macro momentum has soured, with contracting orders and production flagging near-term headwinds. A more defensive stance is prudent.")
        score = -1
    elif signal == -8 or signal == -10:
        signal_output = (Default + f"Very Bad. \n" + "\n" + f"Leading indicators flash recessionary warnings. Expect broad demand weakness and potential earnings downgrades sector-wide.")
        score = 0
    else:
        signal_output = (f"Something Went Wrong for Sure")
        score = 0

    return macro_data_analysis_output1, macro_data_analysis_output2, macro_data_analysis_output_df, signal_output, score