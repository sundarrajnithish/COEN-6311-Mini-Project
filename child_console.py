
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
        user = Family_Wallet.Kid('jake')
    if users == '2':
        user = Family_Wallet.Kid('tony')
    if users == '3':
        user = Family_Wallet.Kid('mickey')
        user.transaction_reset()
        print("This is the output it provides", user.overpay_amount[user.name])
        print("This is the whole list", user.overpay_amount)
    if users == '4':
        user = Family_Wallet.Kid('sofia')
        user.transaction_reset()
        print("This is the output it provides", user.overpay_amount[user.name])
        print("This is the whole list", user.overpay_amount)
    if users == '5':
        user = Family_Wallet.Kid('mia')
    if users == '6':
        user = Family_Wallet.Kid('shakira')
    if users == '7':
        user = Family_Wallet.Kid('amber')
    if users == '8':
        user = Family_Wallet.Kid('ambani')


def login():
    global user
    user.transaction_reset()
    my_wallet = Family_Wallet(user.name)
    if not my_wallet.blocked_user_flag:
        task = input("Welcome {}! \n You daily balance is ${} \n What would you like to do? \n 1. Pay "
                     " \n 2. Logout".format(user.name, user.overpay_amount[user.name]))
        if task == '1':
            user.transaction(shop_name=input("Enter the merchant name: "), amount=input("Enter the amount: $"))
            login()
        if task == '2':
            print("Loading...")
            time.sleep(1)
            welcome()
        if task == 'print':
            print(user.transaction_list)
            login()
    else:
        print("You have been blocked from using the wallet \n Request Dad to Unblock")
        welcome()

while True:
    if logged_in:
        login()
    else:
        welcome()
