from colorama import Fore, Style


def start_menu():
    print("""
        =====================
            STOCK MONITOR
        =====================
    """)
    while True:
        try:
            user_choice = int(
                input(
                    f"{Fore.GREEN}[1] Stock Menu{Style.RESET_ALL}\n{Fore.YELLOW}[2] Crypto Menu{Style.RESET_ALL}\nEnter choice: "
                )
            )
            if user_choice not in {1, 2}:
                print(f"{Fore.RED}ERROR: Please enter 1 or 2{Style.RESET_ALL}")
            else:
                break
        except Exception as e:
            print(f"{Fore.RED}ERROR: {e}{Style.RESET_ALL}")

    if user_choice == 1:
        stock_menu()
    else:
        crypto_menu()


def stock_menu():
    print("""
        ==================
            STOCK MENU
        ==================
    """)
    while True:
        try:
            user_choice = int(
                input(
                    f"{Fore.RED}[1] Aggregates (Bars){Style.RESET_ALL}\n{Fore.YELLOW}[2] Daily Open/Close{Style.RESET_ALL}\n{Fore.GREEN}[3] Investment Growth Calculator{Style.RESET_ALL}\nEnter choice: "
                )
            )
            if user_choice not in {1, 2, 3}:
                print(f"{Fore.RED}ERROR: Please enter a number (1-3){Style.RESET_ALL}")
            else:
                break
        except Exception as e:
            print(f"ERROR: {e}")
    # to be continued
    match user_choice:
        case 1: ... # figure out logic and plan out functions needed
        case 2: ... # same as above
        case 3: ... # ^
        case 4: ... # ^


def crypto_menu():
    print("""
        ===================
            CRYPTO MENU
        ===================
    """)
    user_choice = input(
        f"{Fore.RED}[1] Aggregates (Bars){Style.RESET_ALL}\n{Fore.YELLOW}[2] Daily Open/Close{Style.RESET_ALL}\n{Fore.GREEN}[3] Investment Growth Calculator{Style.RESET_ALL}\nEnter choice: "
    )
    # to be continued
    print(user_choice)
