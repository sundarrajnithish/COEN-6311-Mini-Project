#import os
import time
from backend import Family_Wallet

sarah_williams = Family_Wallet.Mom()
williams_hemisphere = Family_Wallet.Dad()


# Welcome screen for the parent console
def welcome():
    print("Welcome to the Family Bank Wallet! \nType the corresponding numbers for navigating the menu.")
    users = input("\n Type your name number below for Login: \n 1. Sarah Williams (Mom)\n 2. Williams Hemisphere ("
                  "Dad). \n Your choice: ")
    return users


# Menu after logging in
def menu(users):
    if users == '1' or users == '2':
        menus = input("Choose any option below: \n 1. Withdraw (Bank) \n 2. Deposit (Bank) \n 3. Family Wallet "
                      "\n 4. Logout \n Your choice: ")
        return menus


# Menu actions for mom
def mom(user_mom):
    mom_wallet = Family_Wallet('mom')
    menus = menu(user_mom)
    if menus == '1' and user_mom == '1':
        sarah_williams.withdraw((input("How much would you like to withdraw? $ ")))
        time.sleep(0.2)
        mom(user_mom)
    if menus == '2' and user_mom == '1':
        sarah_williams.deposit((input("How much would you like to deposit? $ ")))
        mom(user_mom)
    if menus == '3' and user_mom == '1':
        mom_wallet.parent_wallet_access()
        mom(user_mom)
    if menus == '4' and user_mom == '1':
        time.sleep(1)
        print("You have successfully logged out! \n\n\n")


# Menu actions for dad
def dad(user_dad):
    dad_wallet = Family_Wallet('dad')
    menus = menu(user_dad)
    if menus == '1' and user_dad == '2':
        williams_hemisphere.withdraw((input("How much would you like to withdraw? $ ")))
        dad(user_dad)
    if menus == '2' and user_dad == '2':
        williams_hemisphere.deposit(input("How much would you like to deposit? $ "))
        dad(user_dad)
    if menus == '3' and user_dad == '2':
        dad_wallet.parent_wallet_access()
        dad(user_dad)
    if menus == '4' and user_dad == '2':
        time.sleep(1)
        print("You have successfully logged out! \n\n\n")


# While loop to perform all the tasks repeatedly

while 1:
    # os.system('cls')
    time.sleep(1)
    user = welcome()
    if user == '1':
        mom(user)
    elif user == '2':
        dad(user)
    elif user == 'close':
        exit()
    else:
        print("Invalid Entry! Try Again!")
