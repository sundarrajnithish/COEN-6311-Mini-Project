from main_data import Kid


def welcome():
    print("Welcome to the Family Bank Wallet (Kids Edition)! \nType the corresponding numbers for navigating the menu.")
    users = input("\n Type your name number below for Login: \n 1. Jake Williams \n 2. Tony Williams \n 3. Mickey "
                  "Williams \n 4. Sofia Williams \n 5. Mia Williams \n 6. Shakira Williams \n 7. Amber Williams \n 8. "
                  "Ambani Williams \n Your choice: ")
    return users


jake = Kid('jake')
tony = Kid('tony')
mickey = Kid('mickey')
sofia = Kid('sofia')
mia = Kid('mia')
shakira = Kid('shakira')
amber = Kid('amber')
ambani = Kid('ambani')



while True:
    users = welcome()
    if users == '1':
        task = input("Welcome {}! \n You wallet balance is ${} \n What would you like to do? \n 1. Pay 2. Check wallet "
              "balance" .format(jake.name, jake.daily_limit))
        if task == '1':
            jake.transaction(shop_name=input("Enter the merchant name: "), amount=input("Enter the amount: $"))


