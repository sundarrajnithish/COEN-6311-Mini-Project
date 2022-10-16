from datetime import datetime
import logging
import pickle
import time

# Object to log the date and time
dateTimeObj = datetime.now()
# Creating a log file
logging.basicConfig(filename="data/log.txt", level=logging.INFO)

# All the required data files
with open('data/blocked.pickle', 'rb') as handle:
    blocked = pickle.load(handle)
with open('data/balance.pickle', 'rb') as handle:
    wallet_balance = pickle.load(handle)
with open('data/overpay_request.pickle', 'rb') as handle:
    overpay_request = pickle.load(handle)
with open('data/overpay_amount.pickle', 'rb') as handle:
    overpay_amount = pickle.load(handle)
with open('data/permission_request.pickle', 'rb') as handle:
    permission_request = pickle.load(handle)
with open('data/transaction_valid.pickle', 'rb') as handle:
    transaction_valid = pickle.load(handle)
with open('data/transaction_list.pickle', 'rb') as handle:
    transaction_list = pickle.load(handle)
with open('data/kids_list.pickle', 'rb') as handle:
    kids_list = pickle.load(handle)
with open('data/balance_request.pickle', 'rb') as handle:
    balance_request = pickle.load(handle)
with open('mom_balance.pickle', 'rb') as handle:
    mom_balance = pickle.load(handle)
with open('dad_balance.pickle', 'rb') as handle:
    dad_balance = pickle.load(handle)


# Family wallet class to perform all the wallet functions
class Family_Wallet:
    def __init__(self, name):
        # with open('data/transaction_list.pickle', 'rb') as handle:
        self.transaction_list = transaction_list
        # All the required data files assigned to an object
        self.accessed_blocked = blocked
        self.wallet_balance = wallet_balance
        self.overpay_request = overpay_request
        self.overpay_amount = overpay_amount
        self.permission_request = permission_request
        self.transaction_valid = transaction_valid
        # Temporary flags
        self.ignore = 0
        self.mom_overpay_flag = 0
        # Name of the person accessing the wallet
        self.name = name
        self.balance = wallet_balance
        self.blocked = []
        self.req_name = ""
        self.req_amount = 0
        # Removing the repeated names (if any) in the blocked list
        [self.blocked.append(name) for name in self.accessed_blocked if name not in self.blocked]
        # Checking if the user is blocked from the wallet
        for names in self.blocked:
            if names == self.name and names != 'dad' and names != 'mom':
                print("{} you dont have access to the wallet".format(name))
                logging.info("Wallet tried to access by {} {}".format(name, dateTimeObj))

        logging.info("Wallet accessed by {} {}".format(name, dateTimeObj))

    # Basic transaction functionalities (access only for Mom and Dad)
    def deposit(self, amount, member):
        if member == "dad" or member == "mom":
            self.balance += amount
            with open('data/balance.pickle', 'wb') as handle:
                pickle.dump(self.balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print("\n You have deposited $", amount)
            logging.info("{}'s deposit for ${} accepted {}".format(member, amount, dateTimeObj))

    def withdraw(self, amount, member):
        if self.balance >= amount:
            if member == "dad" or member == "mom":
                self.balance -= amount
                with open('data/balance.pickle', 'wb') as handle:
                    pickle.dump(self.balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
                print("You have withdrawn $", amount)
                logging.info("{} Withdraw {} {}".format(member, amount, dateTimeObj))
        else:
            print("\n Insufficient balance \n Your balance is ${}\n Add balance from the menu section".format(
                self.balance()))
            logging.info("Insufficient Balance {} {}".format(member, dateTimeObj))

    def balance(self):
        print("\n Total available balance=", self.balance)
        return self.balance

    # ----------------------------------------------------------------------------------------------

    def parent_notification(self):
        print("Hello {}!".format(self.name))

    def parent_wallet_access(self):
        balances = self.balance
        print("Available Balance = ${}".format(balances))
        dad_string = ""
        if self.name == 'dad':
            dad_string = "\n 5. Block Settings"
        decision = input("You have accessed the family wallet section: \n Please type any of the options below:  "
                         "\n 1. Deposit \n 2. Withdraw \n 3. View Transactions \n 4. Notifications {} \n 6. Main "
                         "Menu".format(dad_string))
        if decision == '1':
            self.deposit(int(input("How much would you like to deposit? $")), 'mom')
            input("Press Enter to go back to the menu")
            self.parent_wallet_access()
        if decision == '2':
            self.withdraw(int(input("How much would you like to withdraw? $")), 'mom')
            self.parent_wallet_access()
        if decision == '3':
            print("Transaction List \n")
            print(self.transaction_list)
            input("Press Enter to go back to the menu")
            self.parent_wallet_access()
        if decision == '4':
            self.parent_wallet_notifications()
            self.parent_wallet_access()
        if decision == '5':
            if self.name == 'dad':
                status = input("You have accessed the block section. \n Select one of the options below: \n 1. Block "
                               "\n 2. Unblock")
                if status == '1':
                    block = input("Enter the name of the person to be blocked: ")
                    self.blocked.append(block)
                if status == '2':
                    unblock = input("Enter the name of the person to be unblocked: ")
                    self.blocked.remove(unblock)
            else:
                print("\n Please enter a valid option... \n")
                self.parent_wallet_access()
        if decision == '6':
            print("Loading...")
            time.sleep(1)

    # ----------------------------------------------------------------------------------------
    # Permission when the kid requests to use the wallet more than once
    def permission_request_check(self):
        for name in self.permission_request:
            if self.permission_request[name]:
                decision = input("{} has used the wallet more than twice. Would you like to grant permission for his "
                                 "transaction? Type (y/n)".format(name))
                if decision == 'y':
                    self.permission_request[name] = True

    # Checks the overpay request from the accessed file
    def check_overpay(self):
        for name in self.overpay_request:
            if self.overpay_request[name]:
                return True
            else:
                return False

    # Mom's overpay action function
    def overpay_req_mom(self, name, amount):
        decision = input("Do you want to accept overpay request of ${} for {}? Press (y/n). Press any other key to "
                         "request Dad".format(amount, name))
        if decision == "y":
            print("Your acceptance has been registered")
            self.overpay_amount[name] = amount
            self.transaction_valid[name] = True
        elif decision == "n":
            print("Your denial has been registered")
            self.transaction_valid[name] = False
        else:
            self.mom_overpay_flag = 1
            self.req_name = name
            self.req_amount = amount

    # Dad's overpay action function
    def overpay_req_dad(self):
        if self.req_name and self.req_amount:
            name = self.req_name
            amount = self.req_amount
            decision = input(
                "Do you want to accept overpay request of ${} for {}? Press (y/n). ".format(self.req_amount,
                                                                                            self.req_name))
            if decision == "y":
                self.overpay_amount[name] = amount
                print("Your acceptance has been registered")
                self.transaction_valid[name] = True
            elif decision == "n":
                print("Your denial has been registered")
                self.transaction_valid[name] = False
        else:
            pass

    def parent_wallet_notifications(self):
        balance = self.balance
        if balance < 100 and self.ignore == 0:
            print("\n{}, your family wallet balance is less than $100".format(self.name))
            decision = input("Would you like to deposit some money? Type (y/n)")
            if decision == 'y':
                Family_Wallet.deposit(int(input("Enter the Amount: $")), 'mom')
                self.ignore = 1
                input("Press Enter to go back to the menu")
            else:
                self.ignore = 1
                self.parent_wallet_notifications()
        else:
            print("\nHello {}!, your family wallet balance is ${}".format(self.name, balance))
            self.permission_request_check()
            overpay_check = self.check_overpay()
            if overpay_check:
                for name in self.overpay_request:
                    if self.overpay_amount[name] > 50:
                        if self.name == 'mom':
                            self.overpay_req_mom(name, self.overpay_amount[name])
                        elif self.name == 'dad' and self.mom_overpay_flag == 1:
                            self.overpay_req_dad()
            else:
                print("No overpay requests")

            input("Press Enter to go back to the menu")


# Kid class which includes all the necessary functionality of the kid's section

class Kid:
    def __init__(self, name):
        # Assigned required data files to an object
        self.transaction_list = transaction_list
        self.balance_request = balance_request
        self.permission_request = permission_request
        self.kids_list = kids_list
        self.overpay_request = overpay_request
        self.overpay_amount = overpay_amount
        self.transaction_valid = transaction_valid

        self.name = name
        self.request = ""
        self.kids_list = kids_list
        self.use_count = 0
        self.daily_balance = self.overpay_amount[self.name]
        self.daily_balance_check()
        self.my_wallet = Family_Wallet(self.name)

    def daily_balance_check(self):
        if self.daily_balance < 400:
            decision = input("Your wallet balance is low. Do you want to request your parents for a top up? Type "
                             "(y/n). ")
            if decision == 'y':
                self.balance_request[self.name] = True
                print("Your request is sent!")

    def permission_notification(self):
        if not self.permission_request[self.name]:
            print("You are allowed to pay!")
        else:
            print("You are not allowed to pay")

    def request_overpay(self, amount):
        decision = input("Would you like to request Mom for overpay? Type (y/n)")
        if decision == 'y':
            self.overpay_request[self.name] = True
            self.overpay_amount[self.name] = amount
            print("Your request has been sent to Mom")
            input("Press Enter to go back to the menu")

    def transaction(self, amount, shop_name):
        if int(amount) > 50:
            self.request_overpay(amount)
        else:
            if self.transaction_valid:
                if self.daily_limit_check():
                    #logging.basicConfig(filename="transaction_log.txt", level=logging.INFO)
                    logging.info("{} {} {}".format(shop_name, amount, dateTimeObj))
                    current_transaction = (self.name, shop_name, amount, dateTimeObj.now().date())
                    transaction_list.append(current_transaction)
                    with open('data/transaction_list.pickle', 'wb') as handle:
                        pickle.dump(transaction_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    print("heee",current_transaction)
                    self.daily_balance -= int(amount)
                    print("Your transaction is successful")
                else:
                    print("You have exceeded your daily limit! Your request has been registered.")
            else:
                print("Your transaction status is invalid")

    def check_transaction_valid(self):
        transaction_validity = self.transaction_valid[self.name]
        return transaction_validity

    def daily_limit_check(self):
        count = 0
        if not self.transaction_list:
            return True
        for tx in self.transaction_list:
            if tx[0] == self.name and tx[3] == dateTimeObj.now().date():
                count += 1
                return True

        if count >= 2 and not self.transaction_valid:
            decision = input("You have requested payment for more than once! \n Type '1' to request permission for "
                             "wallet \n Press Enter to go back to the menu")

            if decision == '1':
                self.permission_request[self.name] = True
                print("Your request has been sent")
                return False


# Mom account related functions

class Mom:
    def __init__(self):
        self.name = "Sarah Williams"
        self.my_balance = mom_balance
        self.overpay_request = overpay_request
        self.overpay_amount = overpay_amount

    def deposit(self, amount):
        self.my_balance += int(amount)
        with open('mom_balance.pickle', 'wb') as handle:
            pickle.dump(self.my_balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print("You have deposited $ {}".format(amount))
        print("Your account balance is ${}".format(self.my_balance))
        input("Press Enter to go back to the menu")

    def withdraw(self, amount):
        if self.my_balance >= int(amount):
            self.my_balance -= int(amount)
            with open('mom_balance.pickle', 'wb') as handle:
                pickle.dump(self.my_balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print("Your account balance is ${}".format(self.my_balance))
            print("You have withdrawn $ {}".format(amount))
            input("Press Enter to go back to the menu")
        else:
            print("{}, you have insufficient funds!".format(self.name))

    def add_to_wallet(self, amount):
        if self.my_balance >= int(amount):
            self.my_balance -= int(amount)
            with open('mom_balance.pickle', 'wb') as handle:
                pickle.dump(self.my_balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
            Family_Wallet.deposit(amount, "mom")


# Dad account related functions

class Dad:
    def __init__(self):
        self.name = "Williams Hemisphere"
        self.my_balance = dad_balance
        self.overpay_request = overpay_request
        self.overpay_amount = overpay_amount

    def deposit(self, amount):
        self.my_balance += int(amount)
        with open('dad_balance.pickle', 'wb') as handle:
            pickle.dump(self.my_balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print("You have deposited $ {}".format(amount))
        print("Your account balance is ${}".format(self.my_balance))
        input("Press Enter to go back to the menu")

    def withdraw(self, amount):
        if self.my_balance >= int(amount):
            self.my_balance -= int(amount)
            with open('dad_balance.pickle', 'wb') as handle:
                pickle.dump(self.my_balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print("Your account balance is ${}".format(self.my_balance))
            print("You have withdrawn $ {}".format(amount))
            input("Press Enter to go back to the menu")
        else:
            print("{}, you have insufficient funds!".format(self.name))

    def add_to_wallet(self, amount):
        if self.my_balance >= int(amount):
            self.my_balance -= int(amount)
            with open('dad_balance.pickle', 'wb') as handle:
                pickle.dump(self.my_balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
            Family_Wallet.deposit(amount, "dad")
