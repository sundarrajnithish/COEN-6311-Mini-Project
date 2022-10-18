import os
import pickle
from backend_stable import Family_Wallet
import time

user1 = ""
logged_in = False


# Welcome page for the kids wallet access
def welcome():
    global user1
    global logged_in
    os.system('cls')
    print("Welcome to the Family Bank Wallet (Kids Edition)! \nType the corresponding numbers for navigating the menu.")
    users = input("\n Type your name number below for Login: \n 1. Jake Williams \n 2. Tony Williams \n 3. Mickey "
                  "Williams \n 4. Sofia Williams \n 5. Mia Williams \n 6. Shakira Williams \n 7. Amber Williams \n 8. "
                  "Ambani Williams \n Your choice: ")
    logged_in = True
    if users == '1':
        user1 = Family_Wallet.Kid('jake')
    if users == '2':
        user1 = Family_Wallet.Kid('tony')
    if users == '3':
        user1 = Family_Wallet.Kid('mickey')
        user1.transaction_reset()
        print("This is the output it provides", user1.overpay_amount[user1.name])
        print("This is the whole list", user1.overpay_amount)
    if users == '4':
        user1 = Family_Wallet.Kid('sofia')
        user1.transaction_reset()
        print("This is the output it provides", user1.overpay_amount[user1.name])
        print("This is the whole list", user1.overpay_amount)
    if users == '5':
        user1 = Family_Wallet.Kid('mia')
    if users == '6':
        user1 = Family_Wallet.Kid('shakira')
    if users == '7':
        user1 = Family_Wallet.Kid('amber')
    if users == '8':
        user1 = Family_Wallet.Kid('ambani')


def balance_refresh(name):
    with open('data/overpay_amount.pickle', 'rb') as handle:
        my_balance = pickle.load(handle)
        #print("Yes, balance is updated")
        #print("balance list is ", my_balance)
    return my_balance[name]


def login():
    global user
    user1.transaction_reset()
    my_wallet = Family_Wallet(user1.name)
    if not my_wallet.blocked_user_flag:
        bal = balance_refresh(user1.name)

        task = input("Welcome {}! \n You daily balance is ${} \n What would you like to do? \n 1. Pay "
                     " \n 2. Logout".format(user1.name, bal))  # user1.overpay_amount[user1.name]
        if task == '1':
            if bal != 0:
                user1.transaction(shop_name=input("Enter the merchant name: "), amount=input("Enter the amount: $"))
                login()
            else:
                print("You don't have sufficient balance!")
                input("Press Enter to go back to the menu")
        if task == '2':
            print("Loading...")
            time.sleep(1)
            welcome()
        if task == 'print':
            print(user1.transaction_list)
            login()
    else:
        print("You have been blocked from using the wallet \n Request Dad to Unblock")
        welcome()


while True:
    os.system('cls')
    if logged_in:
        login()
    else:
        welcome()
