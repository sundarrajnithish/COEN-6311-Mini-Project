import mom
import dad
import time
import pickle

# import kids

sarah_williams = mom.Mom()
williams_hemisphere = dad.Dad()


# einstein = kids.Kid('einstein')
# tesla = kids.Kid('tesla')

def welcome():
    print("Welcome to the Family Bank Wallet! \nType the corresponding numbers for navigating the menu.")
    users = input("\n Type your name number below for Login: \n 1. Sarah Williams (Mom)\n 2. Williams Hemisphere ("
                  "Dad). \n Your choice: ")
    return users


def menu(users):
    if users == '1' or users == '2':
        menus = input("What would you like to do today? \n 1. Withdraw \n 2. Deposit \n 3. View wallet transactions "
                      "\n 4. Notifications. \n 5. Logout \n Your choice: ")
        return menus


def mom(user):
    if menu(user) == '1' and user == '1':
        sarah_williams.withdraw((input("How much would you like to withdraw? $ ")))
        time.sleep(0.2)
        menu(user)
    if menu(user) == '2' and user == '1':
        sarah_williams.deposit((input("How much would you like to deposit? $ ")))
        menu(user)
    if menu(user) == '3' and user == '1':
        # sarah_williams.deposit((input("How much would you like to deposit? $ ")))
        menu(user)
    if menu(user) == '4' and user == '1':
        # sarah_williams.deposit((input("How much would you like to deposit? $ ")))
        menu(user)


def dad(user):
    if menu(user) == '1' and user == '2':
        williams_hemisphere.withdraw((input("How much would you like to withdraw? $ ")))
        menu(user)
    elif menu(user) == '2' and user == '2':
        williams_hemisphere.deposit(input("How much would you like to deposit? $ "))
        menu(user)
    if menu(user) == '3' and user == '2':
        # sarah_williams.deposit((input("How much would you like to deposit? $ ")))
        menu(user)
    elif menu(user) == '4' and user == '2':
        # sarah_williams.deposit((input("How much would you like to deposit? $ ")))
        menu(user)
    if menu(user) == '5' and user == '2':
        time.sleep(0.5)
        exit()


while 1:
    user = welcome()
    if user == '1':
        mom(user)
    elif user == '2':
        dad(user)
    else:
        print("Invalid Entry! Try Again!")
        welcome()

