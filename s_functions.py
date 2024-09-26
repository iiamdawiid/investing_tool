import os
import re
import sys
from tabulate import tabulate
import mplfinance as mf
import pandas as pd
import textwrap
from datetime import datetime, timezone, timedelta
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
        ),
        end="",
    )
    print(
        f"{Fore.YELLOW}Please enter the following data to receive candlesticks...{Style.RESET_ALL}"
    )
    timespan_options = {
        "second",
        "minute",
        "hour",
        "day",
        "week",
        "month",
        "quarter",
        "year",
    }
    try:
        stocks_ticker = input("Stocks ticker: ")
        while True:
            try:
                multiplier = int(input("Multiplier (default=1): "))
                break
            except ValueError:
                print(
                    f"\n{Fore.RED}ERROR: Multiplier must be an integer{Style.RESET_ALL}\n"
                )

        timespan = input("Candlestick timespan: ").lower()
        while timespan not in timespan_options:
            print(
                f"\n{Fore.RED}ERROR: Enter a valid timespan: ({', '.join(timespan_options)}){Style.RESET_ALL}\n"
            )
            timespan = input("Candlestick timespan: ").lower()

        while True:
            date_from = input("From (YYYY-MM-DD): ")
            while not validate_date(date_from):
                print(
                    f"\n{Fore.RED}ERROR: Date must be in format: {Fore.YELLOW}YYYY-MM-DD{Style.RESET_ALL}\n"
                )
                date_from = input("From (YYYY-MM-DD): ")

            date_to = input("Till (YYYY-MM-DD): ")
            while not validate_date(date_to):
                print(
                    f"\n{Fore.RED}ERROR: Date must be in format: {Fore.YELLOW}YYYY-MM-DD{Style.RESET_ALL}\n"
                )
                date_to = input("To (YYYY-MM-DD): ")

            date1 = datetime.strptime(date_from, "%Y-%m-%d")
            date2 = datetime.strptime(date_to, "%Y-%m-%d")
            if date1 > date2:
                print(
                    f"\n{Fore.RED}ERROR: First date can not exceed second date{Style.RESET_ALL}\n"
                )
            else:
                break

        get_ag_data(stocks_ticker, timespan, date_from, date_to, multiplier)

    except Exception as e:
        print(f"\n{Fore.RED}ERROR: {e}{Style.RESET_ALL}\n")


def get_ag_data(stocks_ticker, timespan, date_from, date_to, multiplier=1):
    # send received vars to API and get data
    BARS_API_URL = (
        textwrap.dedent(
            """
            https://api.polygon.io/v2/aggs/ticker/{stocks_ticker}/range/{multiplier}/{timespan}/{date_from}/{date_to}?adjusted=true&sort=asc&apiKey={API_KEY}
        """
        )
        .format(
            stocks_ticker=stocks_ticker,
            multiplier=multiplier,
            timespan=timespan,
            date_from=date_from,
            date_to=date_to,
            API_KEY=API_KEY,
        )
        .strip()
    )

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
    dates = [
        datetime.fromtimestamp(candle["t"] / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
        for candle in c
    ]

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
        "Volume": volume,
    }

    display_ag_data(data)


def display_ag_data(data):
    df = pd.DataFrame(data)
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)

    mf.plot(df, type="candle", volume=True, style="yahoo", figscale=1.5)

    restart = input(
        f"\n{Fore.GREEN}[C] CONTINUE{Style.RESET_ALL}\n{Fore.RED}[Q] QUIT{Style.RESET_ALL}\nEnter choice: "
    ).upper()
    if restart == "Q":
        display_quit_message()


# ==================== DAILY OPEN/CLOSE ====================
def get_oc_vars():
    print(
        textwrap.dedent(
            """
          ========================
              DAILY OPEN/CLOSE
          ========================
        """
        ),
        end="",
    )
    print(
        f"{Fore.YELLOW}Please enter the following data to receive Daily Open/Close data...{Style.RESET_ALL}"
    )
    try:
        stocks_ticker = input("Stocks ticker: ")
        while True:
            date = input("Date (YYYY-MM-DD): ")
            current_date = datetime.strptime(date, "%Y-%m-%d")
            if current_date > datetime.now():
                print(
                    f"\n{Fore.RED}ERROR: Date can not be in the future{Style.RESET_ALL}\n"
                )
                continue
            else:
                while not validate_date(date):
                    print(
                        f"\n{Fore.RED}ERROR: Date must be in format: {Fore.YELLOW}YYYY-MM-DD{Style.RESET_ALL}\n"
                    )
                    date = input("Date (YYYY-MM-DD): ")
                break

        get_oc_data(stocks_ticker, date)

    except Exception as e:
        print(f"ERROR: {e}")


def get_oc_data(stocks_ticker, date, growth=False):
    OC_API_URL = (
        textwrap.dedent(
            """
            https://api.polygon.io/v1/open-close/{stocks_ticker}/{date}?adjusted=true&apiKey={API_KEY}
        """
        )
        .format(stocks_ticker=stocks_ticker, date=date, API_KEY=API_KEY)
        .strip()
    )

    try:
        response = requests.get(OC_API_URL)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "NOT FOUND":
            raise Exception(f"\n{Fore.RED}ERROR: {data['message']}{Style.RESET_ALL}\n")

    except requests.exceptions.RequestException as e:
        print(f"\n{Fore.RED}ERROR: {e}{Style.RESET_ALL}\n")

    # if this function is called from growth calculator, return instead of display
    if growth:
        if data:
            return data["close"]
        else:
            return ""
    else:
        fmt_display_table(data)


def fmt_display_table(data):
    date, symbol, premarket, open, high, low, close, afterhours, volume = (
        data["from"],
        data["symbol"],
        data["preMarket"],
        data["open"],
        data["high"],
        data["low"],
        data["close"],
        data["afterHours"],
        data["volume"],
    )
    table = [
        ["Date", date],
        ["Symbol", symbol],
        ["Pre-Market", premarket],
        ["Open", open],
        ["High", high],
        ["Low", low],
        ["Close", close],
        ["After-Hours", afterhours],
        ["Volume", volume],
    ]

    display_oc_data(table)


def display_oc_data(table):
    print(tabulate(table, tablefmt="grid"))


# ==================== INVESTMENT GROWTH CALCULATOR ====================
def is_holiday(date):
    user_date = datetime.strptime(date, "%Y-%m-%d")
    year = user_date.year
    MARKET_HOLIDAYS = [
        f"{year}-01-01",
        f"{year}-01-15",
        f"{year}-02-20",
        f"{year}-04-07",
        f"{year}-05-29",
        f"{year}-06-19",
        f"{year}-07-04",
        f"{year}-09-04",
        f"{year}-11-23",
        f"{year}-11-24",
        f"{year}-12-25",
    ]
    return not date in MARKET_HOLIDAYS


def is_market_open(date):
    user_date = datetime.strptime(date, "%Y-%m-%d")
    if user_date.weekday() >= 5:
        return False
    return True


def get_growth_vars():
    print(
        textwrap.dedent(
            """
          =========================
              GROWTH CALCULATOR
          =========================
        """
        ),
        end="",
    )
    print(
        f"{Fore.YELLOW}Please enter the following data to calculate growth...{Style.RESET_ALL}"
    )
    try:
        while True:
            past_date = input("Past date: ")
            if validate_date(past_date):
                # break
                if is_market_open(past_date):
                    if is_holiday(past_date):
                        break
                    else:
                        print(
                            f"\n{Fore.RED}ERROR: Date can not be holiday{Style.RESET_ALL}\n"
                        )
                else:
                    print(
                        f"\n{Fore.RED}ERROR: Must be valid trading day{Style.RESET_ALL}\n"
                    )
            else:
                print(
                    f"\n{Fore.RED}ERROR: Date must be in YYYY-MM-DD format{Style.RESET_ALL}\n"
                )

        stock_ticker = input("Stock ticker: ")

        while True:
            try:
                itl_inv = float(input("Investment amount: "))
                if itl_inv < 0:
                    print(
                        f"\n{Fore.RED}ERROR: Investment must be greater than 0{Style.RESET_ALL}\n"
                    )
                else:
                    break

            except ValueError:
                print(f"{Fore.RED}ERROR: Please enter a number{Style.RESET_ALL}\n")

    except Exception as e:
        print(f"{Fore.RED}ERROR: {e}{Style.RESET_ALL}")

    current_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    past_price = float(get_oc_data(stock_ticker, past_date, growth=True))
    current_price = float(get_oc_data(stock_ticker, current_date, growth=True))

    amt_growth, pct_growth, current_value = calculate_growth(
        itl_inv, past_price, current_price
    )
    # build function to color specific parts of table
    stock_ticker, past_date, past_price, current_date, current_price, itl_inv = (
        colorfmt_table(
            stock_ticker, past_date, past_price, current_date, current_price, itl_inv
        )
    )
    # call function to format for display
    fmt_growth_table = fmt_growth_table_display(
        stock_ticker,
        past_date,
        past_price,
        current_date,
        current_price,
        amt_growth,
        pct_growth,
        current_value,
        itl_inv,
    )
    display_growth(fmt_growth_table)


def calculate_growth(itl_inv, past_price, current_price):
    num_shares = itl_inv / past_price

    current_value = num_shares * current_price
    fmt_current_value = f"{current_value:,.2f}"
    past_value = num_shares * past_price

    amt_growth = current_value - itl_inv
    fmt_amt_growth = f"{amt_growth:,.2f}"
    pct_growth = (current_value / itl_inv) * 100
    fmt_pct_growth = f"{pct_growth:,.2f}"
    if amt_growth < 0:
        amt_growth = f"{Fore.RED}- ${fmt_amt_growth}{Style.RESET_ALL}"
        pct_growth = f"{Fore.RED}- %{fmt_pct_growth}{Style.RESET_ALL}"
    else:
        amt_growth = f"{Fore.GREEN}+ ${fmt_amt_growth}{Style.RESET_ALL}"
        pct_growth = f"{Fore.GREEN}+ %{fmt_pct_growth}{Style.RESET_ALL}"

    if current_value < past_value:
        current_value = f"{Fore.RED}${fmt_current_value}{Style.RESET_ALL}"
    else:
        current_value = f"{Fore.GREEN}${fmt_current_value}{Style.RESET_ALL}"

    return amt_growth, pct_growth, current_value


def colorfmt_table(
    stock_ticker, past_date, past_price, current_date, current_price, itl_inv
):
    stock_ticker = f"{Fore.GREEN}{stock_ticker}{Style.RESET_ALL}"
    past_date = f"{Fore.YELLOW}{past_date}{Style.RESET_ALL}"
    fmt_past_price = f"{past_price:,.2f}"
    past_price = f"{Fore.YELLOW}${fmt_past_price}{Style.RESET_ALL}"
    current_date = f"{Fore.GREEN}{current_date}{Style.RESET_ALL}"
    fmt_current_price = f"{current_price:,.2f}"
    current_price = f"{Fore.GREEN}${fmt_current_price}{Style.RESET_ALL}"
    fmt_itl_inv = f"{itl_inv:,.2f}"
    itl_inv = f"{Fore.YELLOW}${fmt_itl_inv}{Style.RESET_ALL}"

    return stock_ticker, past_date, past_price, current_date, current_price, itl_inv


def fmt_growth_table_display(
    stock_ticker,
    past_date,
    past_price,
    current_date,
    current_price,
    amt_growth,
    pct_growth,
    current_value,
    itl_inv,
):
    table = [
        [past_date, current_date, current_date],
        [past_price, current_price, pct_growth],
        [itl_inv, current_value, amt_growth],
    ]
    headers = ["PAST", "CURRENT", f"Δ $ ({stock_ticker})"]
    return tabulate(table, headers, tablefmt="grid")


def display_growth(fmt_growth_table):
    print(fmt_growth_table)
