import os
from main_data import Dad, Mom, Family_Wallet
import time

sarah_williams = Mom()
williams_hemisphere = Dad()


# einstein = kids.Kid('einstein')
# tesla = kids.Kid('tesla')


def welcome():
    print("Welcome to the Family Bank Wallet! \nType the corresponding numbers for navigating the menu.")
    users = input("\n Type your name number below for Login: \n 1. Sarah Williams (Mom)\n 2. Williams Hemisphere ("
                  "Dad). \n Your choice: ")
    return users


def menu(users):
    if users == '1' or users == '2':
        menus = input("What would you like to do today? \n 1. Withdraw (Bank) \n 2. Deposit (Bank) \n 3. Family Wallet "
                      "\n 4. Notifications. \n 5. Logout \n Your choice: ")
        return menus



def mom(user):
    mom_wallet = Family_Wallet('mom')
    menus = menu(user)
    if menus == '1' and user == '1':
        sarah_williams.withdraw((input("How much would you like to withdraw? $ ")))
        time.sleep(0.2)
        mom(user)
    if menus == '2' and user == '1':
        sarah_williams.deposit((input("How much would you like to deposit? $ ")))
        mom(user)
    if menus == '3' and user == '1':
        mom_wallet.family_wallet()
        mom(user)
    if menus == '4' and user == '1':
        mom_wallet.notification(Mom.my_name())
        mom(user)
    if menus == '5' and user == '1':
        time.sleep(1)
        print("You have successfully logged out! \n\n\n")


def dad(user):
    wallet = Family_Wallet('dad')
    menus = menu(user)
    if menus == '1' and user == '2':
        williams_hemisphere.withdraw((input("How much would you like to withdraw? $ ")))
        dad(user)
    if menus == '2' and user == '2':
        williams_hemisphere.deposit(input("How much would you like to deposit? $ "))
        dad(user)
    if menus == '3' and user == '2':
        Dad.view_transaction()
        dad(user)
    if menus == '4' and user == '2':
        wallet.notification(Dad.my_name())
        dad(user)
    if menus == '5' and user == '2':
        time.sleep(1)
        print("You have successfully logged out! \n\n\n")


while 1:
    os.system('cls')
    time.sleep(1)
    user = welcome()
    if user == '1':
        mom(user)
    elif user == '2':
        dad(user)
    else:
        print("Invalid Entry! Try Again!")
