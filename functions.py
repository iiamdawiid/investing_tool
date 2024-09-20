import os
from colorama import Fore, Style
from dotenv import load_dotenv

load_dotenv()

api_url_bars = os.getenv("API_URL_BARS")
api_url_oc = os.getenv("API_URL_OC")


def get_ag_vars():
    # get api parameters from user: stocks_ticker, multiplier, timespan, from, to
    print("""
        ====================
            CANDLESTICKS
        ====================
    """)
    print(f"{Fore.YELLOW}Please enter the following data to receive candlesticks...{Style.RESET_ALL}")
    stocks_ticker = input("Stocks ticker: ")
    # the multiplier means that the API is aggregating data over X-day intervals. 
    # If X is 10, it groups 10 day's worth of price data into a single candlestick
    multiplier = int(input("Multiplier (Default=1): "))
    timespan = input("Candlestick timespan: ")
    date_from = input("From (YYYY-MM-DD): ")
    date_to = input("Till (YYYY-MM-DD): ")


def get_ag_data(): ...

def display_ag_data(): ...