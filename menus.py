import textwrap
from colorama import Fore, Style
from s_functions import display_quit_message, get_ag_vars


def start_menu():
    while True:
        print(textwrap.dedent("""
            =====================
                STOCK MONITOR
            =====================
            """), end="")
        while True:
            try:
                user_choice = int(
                    input(
                        f"{Fore.RED}[0] Quit{Style.RESET_ALL}\n{Fore.GREEN}[1] Stock Menu{Style.RESET_ALL}\n{Fore.YELLOW}[2] Crypto Menu{Style.RESET_ALL}\nEnter choice: "
                    )
                )
                if user_choice not in {0, 1, 2}:
                    print(f"\n{Fore.RED}ERROR: Please enter an integer (0-3){Style.RESET_ALL}\n")
                else:
                    break

            except Exception as e:
                print(f"\n{Fore.RED}ERROR: {e}{Style.RESET_ALL}\n")

        if user_choice == 1:
            stock_menu()
        elif user_choice == 2:
            crypto_menu()
        else:
            display_quit_message()


def stock_menu():
    print(textwrap.dedent("""
          ==================
              STOCK MENU
          ==================
        """), end="")
    while True:
        try:
            user_choice = int(
                input(
                    f"{Fore.RED}[0] Quit{Style.RESET_ALL}\n{Fore.BLUE}[1] Candlesticks{Style.RESET_ALL}\n{Fore.YELLOW}[2] Daily Open/Close{Style.RESET_ALL}\n{Fore.GREEN}[3] Investment Growth Calculator{Style.RESET_ALL}\nEnter choice: "
                )
            )
            if user_choice not in {0, 1, 2, 3}:
                print(f"\n{Fore.RED}ERROR: Please enter a number (1-3){Style.RESET_ALL}\n")
            else:
                break

        except Exception as e:
            print(f"\n{Fore.RED}ERROR: {e}{Style.RESET_ALL}\n")
    # to be continued
    match user_choice:
        case 0: display_quit_message()
        case 1: get_ag_vars()
        case 2: ...
        case 3: ... 
        case 4: ... 


def crypto_menu():
    print(textwrap.dedent("""
          ======================
              CRYPTO MONITOR
          ======================
        """), end="")
    user_choice = input(
        f"{Fore.RED}[1] Aggregates (Bars){Style.RESET_ALL}\n{Fore.YELLOW}[2] Daily Open/Close{Style.RESET_ALL}\n{Fore.GREEN}[3] Investment Growth Calculator{Style.RESET_ALL}\nEnter choice: "
    )
    # to be continued
    print(user_choice)
