from backend import Kid
from backend import Family_Wallet
import time

user = ""
logged_in = False


# Welcome page for the kids wallet access
def welcome():
    global user
    global logged_in
    print("Welcome to the Family Bank Wallet (Kids Edition)! \nType the corresponding numbers for navigating the menu.")
    users = input("\n Type your name number below for Login: \n 1. Jake Williams \n 2. Tony Williams \n 3. Mickey "
                  "Williams \n 4. Sofia Williams \n 5. Mia Williams \n 6. Shakira Williams \n 7. Amber Williams \n 8. "
                  "Ambani Williams \n Your choice: ")
    logged_in = True
    if users == '1':
        user = Kid('jake')
    if users == '2':
        user = Kid('tony')
    if users == '3':
        user = Kid('mickey')
    if users == '4':
        user = Kid('sofia')
    if users == '5':
        user = Kid('mia')
    if users == '6':
        user = Kid('shakira')
    if users == '7':
        user = Kid('amber')
    if users == '8':
        user = Kid('ambani')


def login():
    global user
    my_wallet = Family_Wallet(user.name)
    task = input("Welcome {}! \n You wallet balance is ${} \n What would you like to do? \n 1. Pay 2. Check daily "
                 "balance \n 3. Logout".format(user.name, user.daily_balance))
    if task == '1':
        user.transaction(shop_name=input("Enter the merchant name: "), amount=input("Enter the amount: $"))
        login()
    if task == '2':
        print("Your available balance is {}".format(user.daily_balance))
        login()
    if task == '3':
        print("Loading...")
        time.sleep(1)
        welcome()
    if task == '4':
        print(user.transaction_list)
        login()


while True:
    if logged_in:
        login()
    else:
        welcome()
