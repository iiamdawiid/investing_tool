import os
import re
import sys
import json
import mplfinance as mf
import pandas as pd
import textwrap
from datetime import datetime, timezone
import requests
from colorama import Fore, Style
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")


def display_quit_message():
    sys.exit(f"\n{Fore.RED}PROGRAM QUIT{Style.RESET_ALL}")


def validate_date(date):
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    return re.match(pattern, date)

# ==================== CANDLESTICKS ====================
def get_ag_vars():
    print(
        textwrap.dedent(
        """
          ====================
              CANDLESTICKS
          ====================
        """
        ), end="")
    print(
        f"{Fore.YELLOW}Please enter the following data to receive candlesticks...{Style.RESET_ALL}"
    )
    timespan_options = {"second", "minute", "hour", "day", "week", "month", "quarter", "year"}
    try:
        stocks_ticker = input("Stocks ticker: ")
        while True:
            try:
                multiplier = int(input("Multiplier (default=1): "))
                break
            except ValueError:
                print(f"\n{Fore.RED}ERROR: Multiplier must be an integer{Style.RESET_ALL}\n")
        
        timespan = input("Candlestick timespan: ").lower()
        while timespan not in timespan_options:
            print(f"\n{Fore.RED}ERROR: Enter a valid timespan: ({', '.join(timespan_options)}){Style.RESET_ALL}\n")
            timespan = input("Candlestick timespan: ").lower()

        while True:
            date_from = input("From (YYYY-MM-DD): ")
            while not validate_date(date_from):
                print(f"\n{Fore.RED}ERROR: Date must be in format: {Fore.YELLOW}YYYY-MM-DD{Style.RESET_ALL}\n")
                date_from = input("From (YYYY-MM-DD): ")

            date_to = input("Till (YYYY-MM-DD): ")
            while not validate_date(date_to):
                print(f"\n{Fore.RED}ERROR: Date must be in format: {Fore.YELLOW}YYYY-MM-DD{Style.RESET_ALL}\n")
                date_to = input("To (YYYY-MM-DD): ")

            date1 = datetime.strptime(date_from, "%Y-%m-%d")
            date2 = datetime.strptime(date_to, "%Y-%m-%d")
            if date1 > date2:
                print(f"\n{Fore.RED}ERROR: First date can not exceed second date{Style.RESET_ALL}\n")
            else:
                break

        get_ag_data(stocks_ticker, timespan, date_from, date_to, multiplier)

    except Exception as e:
        print(f"\n{Fore.RED}ERROR: {e}{Style.RESET_ALL}\n")


def get_ag_data(stocks_ticker, timespan, date_from, date_to, multiplier=1):
    # send received vars to API and get data
    BARS_API_URL = textwrap.dedent(
        """
            https://api.polygon.io/v2/aggs/ticker/{stocks_ticker}/range/{multiplier}/{timespan}/{date_from}/{date_to}?adjusted=true&sort=asc&apiKey={API_KEY}
        """
    ).format(
        stocks_ticker=stocks_ticker,
        multiplier=multiplier,
        timespan=timespan,
        date_from=date_from,
        date_to=date_to,
        API_KEY=API_KEY
    ).strip()

    try:
        response = requests.get(BARS_API_URL)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "NOT FOUND":
            raise Exception(f"\n{Fore.RED}ERROR: {data['message']}{Style.RESET_ALL}\n")

    except requests.exceptions.RequestException as e:
        print(f"\n{Fore.RED}ERROR: {e}{Style.RESET_ALL}\n")

    dataframe_fmt(data["results"])


def dataframe_fmt(c):
    open = []
    high = []
    low = []
    close = []
    volume = []
    dates = [datetime.fromtimestamp(candle["t"] / 1000, tz=timezone.utc).strftime("%Y-%m-%d") for candle in c]

    for candle in c:
        open.append(candle["o"])
        high.append(candle["h"])
        low.append(candle["l"])
        close.append(candle["c"])
        volume.append(candle["v"])

    data = {
        "Date": dates,
        "Open": open,
        "High": high,
        "Low": low,
        "Close": close,
        "Volume": volume
    }

    display_ag_data(data)


def display_ag_data(data):
    df = pd.DataFrame(data)
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)

    mf.plot(df, type="candle", volume=True, style="yahoo", figscale=1.5)

    restart = input(f"\n{Fore.GREEN}[C] CONTINUE{Style.RESET_ALL}\n{Fore.RED}[Q] QUIT{Style.RESET_ALL}\nEnter choice: ").upper()
    if restart == 'Q':
        display_quit_message()

# ==================== DAILY OPEN/CLOSE ====================