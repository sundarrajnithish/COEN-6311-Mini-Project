from datetime import datetime
import logging
import pickle
import time
import os

# Object to log the date and time
dateTimeObj = datetime.now()
# Creating a log file using the logging library
logging.basicConfig(filename="data/log.txt", level=logging.INFO)

# All the required data files are loaded into the memory and made ready to access.
# So the information stays upto date even when multiple users are accessing the console at the same time.

# Blocked list: Users in this list other than mom and dad will not be allowed to access the family wallet
with open('data/blocked.pickle', 'rb') as handle:
    blocked_list = pickle.load(handle)

# Wallet Balance: This is a data file that stores the wallet balance which can be accessed whenever required.
with open('data/balance.pickle', 'rb') as handle:
    wallet_balance = pickle.load(handle)

# Overpay request dictionary is a request flag assigned to each member
with open('data/overpay_request.pickle', 'rb') as handle:
    overpay_request = pickle.load(handle)

# Overpay amount list contains the daily balance of every member in the kid class
with open('data/overpay_amount.pickle', 'rb') as handle:
    overpay_amount = pickle.load(handle)

# Permission request list contains flag for request multiple transactions for members in the kid class
with open('data/permission_request.pickle', 'rb') as handle:
    permission_request = pickle.load(handle)

# Transaction valid status list holds a flag for valid kid class member transaction status
with open('data/transaction_valid.pickle', 'rb') as handle:
    transaction_valid = pickle.load(handle)

# History of transactions list contains all the entries of a transaction
with open('data/transaction_list.pickle', 'rb') as handle:
    transaction_list = pickle.load(handle)

# Balance request variable which holds flag for indicating not sufficient balance from a kid
with open('data/balance_request.pickle', 'rb') as handle:
    balance_request = pickle.load(handle)

# File that holds mom's account balance
with open('data/mom_balance.pickle', 'rb') as handle:
    mom_balance = pickle.load(handle)

# File that holds dad's account balance
with open('data/dad_balance.pickle', 'rb') as handle:
    dad_balance = pickle.load(handle)

# File that holds dad's overpay flag when an overpay request is transferred from mom
with open('data/overpay_dad.pickle', 'rb') as handle:
    overpay_dad = pickle.load(handle)

# File that contains flag to indicate that the user is allowed to do more than 2 transactions when the request is
# accepted.
with open('data/transaction_flag.pickle', 'rb') as handle:
    transaction_flag = pickle.load(handle)


# Note #1: Most of these variables and flag could have been included in a list and could have resulted in lesser
#          complication of the code. Planning to work on that in the future updates of this program!

# Note #2: All of these data files will be retrieved and stored directly to the file when accessed to make the
#         information stay updated.


# Family wallet class to perform all the wallet functions
class Family_Wallet:
    def __init__(self, name):

        # All the required data files assigned to an object
        self.transaction_list = transaction_list
        # All the required data files assigned to an object
        self.wallet_balance_request = balance_request
        self.accessed_blocked = blocked_list
        self.wallet_balance = wallet_balance
        self.overpay_request = overpay_request
        self.overpay_amount = overpay_amount
        self.permission_request = permission_request
        self.transaction_valid = transaction_valid
        self.dad_balance = dad_balance
        self.mom_balance = mom_balance

        # Temporary flags
        self.transaction_flag = transaction_flag
        self.ignore = 0
        self.mom_overpay_flag = 0
        self.already_accepted_flag = 0
        self.overpay_flag = True
        self.overpay_dad = overpay_dad
        self.blocked_user_flag = False

        # Name of the person accessing the wallet
        self.name = name
        # Empty blocked list so that we can append only non-repeated characters to the blocked list
        # Example: When dad blocks the same person twice.
        self.blocked = []

        # Removing the repeated names (if any) in the blocked list
        with open('data/blocked.pickle', 'rb') as handle:
            self.accessed_blocked = pickle.load(handle)
        [self.blocked.append(name) for name in self.accessed_blocked if name not in self.blocked]
        with open('data/blocked.pickle', 'wb') as handle:
            pickle.dump(self.blocked, handle, protocol=pickle.HIGHEST_PROTOCOL)

        #print("Debug: Blocked list", self.blocked)
        # Checking if the user is blocked from the wallet
        for names in self.blocked:
            if names == self.name and names != 'dad' and names != 'mom':
                print("{} you dont have access to the wallet".format(name))
                input("Press Enter to go back to the menu")
                logging.info("Wallet tried to access by {} {}".format(name, dateTimeObj))
                self.blocked_user_flag = True

        logging.info("Wallet accessed by {} {}".format(name, dateTimeObj))

    # Basic transaction functionalities (deposit, withdraw and check balance) (access only for Mom and Dad)

    # ----------------------------------------------------------------------------------------------------
    def deposit(self, amount, member):
        if member == "dad":
            if self.dad_balance >= int(amount):
                self.dad_balance -= int(amount)
                with open('data/dad_balance.pickle', 'wb') as handle:
                    pickle.dump(self.dad_balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
                self.wallet_balance += amount
                print("\n You have deposited $", amount)
                print("\n Your bank account balance is ${}".format(self.dad_balance))
            logging.info("{}'s deposit for ${} accepted {}".format(member, amount, dateTimeObj))
        if member == "mom":
            if self.mom_balance >= int(amount):
                # print("Before mom",self.mom_balance)
                self.mom_balance -= int(amount)
                # print("after mom",self.mom_balance)
                with open('data/mom_balance.pickle', 'wb') as handle:
                    pickle.dump(self.mom_balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
                # print("Before wallet",self.wallet_balance)
                self.wallet_balance += amount
                # print("after wallet",self.wallet_balance)
                with open('data/balance.pickle', 'wb') as handle:
                    pickle.dump(self.wallet_balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
                print("\n You have deposited $", amount)
                print("\n Your bank account balance is ${}".format(self.mom_balance))
            logging.info("{}'s deposit for ${} accepted {}".format(member, amount, dateTimeObj))

    def withdraw(self, amount, member):
        if self.wallet_balance >= amount:
            if member == "dad":
                self.wallet_balance -= amount
                with open('data/balance.pickle', 'wb') as handle:
                    pickle.dump(self.wallet_balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
                self.dad_balance += int(amount)
                with open('data/dad_balance.pickle', 'wb') as handle:
                    pickle.dump(self.dad_balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
                print("You have withdrawn $", amount)
                print("\n Your bank account balance is ${}".format(self.dad_balance))
                logging.info("{} Withdraw {} {}".format(member, amount, dateTimeObj))
            if member == "mom":
                self.wallet_balance -= amount
                with open('data/balance.pickle', 'wb') as handle:
                    pickle.dump(self.wallet_balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
                self.mom_balance += int(amount)
                with open('data/mom_balance.pickle', 'wb') as handle:
                    pickle.dump(self.mom_balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
                print("You have withdrawn $", amount)
                print("\n Your bank account balance is ${}".format(self.mom_balance))
                logging.info("{} Withdraw {} {}".format(member, amount, dateTimeObj))
        else:
            print("\n Insufficient balance \n Your balance is ${}\n Add balance from the menu section".format(
                self.wallet_balance))
            logging.info("Insufficient Balance {} {}".format(member, dateTimeObj))

    def balance(self):
        print("\n Total available balance=", self.wallet_balance)
        return self.wallet_balance

    # ----------------------------------------------------------------------------------------------------

    # Manual transaction status control incase an overpay request gets ignored or error due to a pile of requests
    def transaction_status_setting(self):
        with open('data/transaction_valid.pickle', 'rb') as handle:
            self.transaction_valid = pickle.load(handle)
        print("Transaction Status List: \n")
        for tx in self.transaction_valid:
            print(tx, self.transaction_valid[tx])
        name = input("\n Enter the name of the person to change their transaction status: ")
        status = input("\n Enter the transaction status. '1' for True and '2' for False: ")
        if status == '1':
            self.transaction_valid[name] = True
            with open('data/transaction_valid.pickle', 'wb') as handle:
                pickle.dump(self.transaction_valid, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print("Updated Transaction List: ")
            for tx in self.transaction_valid:
                print(tx, self.transaction_valid[tx])
        if status == '2':
            self.transaction_valid[name] = False
            with open('data/transaction_valid.pickle', 'wb') as handle:
                pickle.dump(self.transaction_valid, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print("Updated Transaction List: ")
            for tx in self.transaction_valid:
                print(tx, self.transaction_valid[tx])
        decision = input("Would you like to make any changes? Type (y/n)")
        if decision == 'y':
            self.transaction_status_setting()
            input("\n Press Enter to go back to the menu")
        else:
            input("\n Press Enter to go back to the menu")

    # Parent wallet access section where they have control over all the wallet functions
    def parent_wallet_access(self):
        os.system('cls')
        with open('data/balance.pickle', 'rb') as handle:
            self.wallet_balance = pickle.load(handle)
        balances = self.wallet_balance
        print("Available Balance = ${}".format(balances))
        dad_string = ""
        if self.name == 'dad':
            dad_string = "\n 5. Block Settings"
        decision = input("You have accessed the family wallet section: \n Please type any of the options below:  "
                         "\n 1. Deposit \n 2. Withdraw \n 3. View Transactions \n 4. Notifications {} \n 6. "
                         "Transaction Status Setting \n 7. Main Menu".format(dad_string))
        if decision == '1':
            self.deposit(int(input("How much would you like to deposit? $")), self.name)
            input("Press Enter to go back to the menu")
            self.parent_wallet_access()
        if decision == '2':
            self.withdraw(int(input("How much would you like to withdraw? $")), self.name)
            input("Press Enter to go back to the menu")
            self.parent_wallet_access()
        if decision == '3':
            print("Transaction List \n")
            with open('data/transaction_list.pickle', 'rb') as handle:
                temp_transaction_list = pickle.load(handle)
            # print(temp_transaction_list)
            for temp_tx in temp_transaction_list:
                print(temp_tx)
            # print(self.transaction_list)
            # time.sleep(0.5)
            input("Press Enter to go back to the menu")
            # time.sleep(0.5)
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
                    with open('data/blocked.pickle', 'rb') as handle:
                        self.blocked = pickle.load(handle)
                    self.blocked.append(block)
                    with open('data/blocked.pickle', 'wb') as handle:
                        pickle.dump(self.blocked, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    input("Press Enter to go back to the menu")
                    self.parent_wallet_access()
                if status == '2':
                    unblock = input("Enter the name of the person to be unblocked: ")
                    with open('data/blocked.pickle', 'rb') as handle:
                        self.blocked = pickle.load(handle)
                    self.blocked.remove(unblock)
                    with open('data/blocked.pickle', 'wb') as handle:
                        pickle.dump(self.blocked, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    input("Press Enter to go back to the menu")
                    self.parent_wallet_access()
            else:
                print("\n Please enter a valid option... \n")
                self.parent_wallet_access()
        if decision == '6':
            self.transaction_status_setting()
            self.parent_wallet_access()
        if decision == '7':
            print("Loading...")
            time.sleep(1)

    # ----------------------------------------------------------------------------------------------------
    # Function to check whether the kids have requested for a wallet balance top up
    def balance_request_check(self):
        with open('data/balance_request.pickle', 'rb') as handle:
            self.wallet_balance_request = pickle.load(handle)
        for name in self.wallet_balance_request:
            if self.wallet_balance_request[name]:
                decision = input("{} has requested for a balance. Would you like to deposit? Type (y/n)".format(name))
                if decision == 'y':
                    self.wallet_balance_request[name] = False
                    with open('data/balance_request.pickle', 'wb') as handle:
                        pickle.dump(self.wallet_balance_request, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    self.deposit(int(input("How much would you like to deposit? $")), self.name)
                    input("Press Enter to go back to the menu")

    # Function to check whether the kids have requested to use the wallet more than once
    def permission_request_check(self):
        with open('data/permission_request.pickle', 'rb') as handle:
            self.permission_request = pickle.load(handle)
        with open('data/transaction_flag.pickle', 'rb') as handle:
            self.transaction_flag = pickle.load(handle)
        for name in self.permission_request:
            if self.permission_request[name]:
                decision = input("{} has used the wallet more than twice. Would you like to grant permission for his "
                                 "transaction? Type (y/n)".format(name))
                if decision == 'y':
                    self.transaction_flag[name] = 1
                    with open('data/transaction_flag.pickle', 'wb') as handle:
                        pickle.dump(self.transaction_flag, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    self.permission_request[name] = False
                    with open('data/permission_request.pickle', 'wb') as handle:
                        pickle.dump(self.permission_request, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    self.transaction_valid[name] = True
                    with open('data/transaction_valid.pickle', 'wb') as handle:
                        pickle.dump(self.transaction_valid, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    print("You acceptance has been registered")
                elif decision == 'n':
                    self.transaction_valid[name] = False
                    with open('data/transaction_valid.pickle', 'wb') as handle:
                        pickle.dump(self.transaction_valid, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    print("{} is not permitted to make transactions".format(name))

    # Mom's overpay request function. Mom can either take action or transfer to Dad
    def overpay_req_mom(self, name, amount, balance):
        decision = input("Do you want to accept overpay request of ${} for {}? Press (y/n). Press any other key to "
                         "request Dad".format(amount, name))
        if decision == "y":
            self.overpay_request[name] = False
            with open('data/overpay_request.pickle', 'wb') as handle:
                pickle.dump(self.overpay_request, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print("Your acceptance has been registered")
            self.overpay_amount[name] = amount
            with open('data/overpay_amount.pickle', 'wb') as handle:
                pickle.dump(self.overpay_amount, handle, protocol=pickle.HIGHEST_PROTOCOL)
            self.transaction_valid[name] = True
            with open('data/transaction_valid.pickle', 'wb') as handle:
                pickle.dump(self.transaction_valid, handle, protocol=pickle.HIGHEST_PROTOCOL)
        elif decision == "n":
            self.overpay_request[name] = False
            with open('data/overpay_request.pickle', 'wb') as handle:
                pickle.dump(self.overpay_request, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print("Your denial has been registered")
            self.overpay_amount[name] = balance
            with open('data/overpay_amount.pickle', 'wb') as handle:
                pickle.dump(self.overpay_amount, handle, protocol=pickle.HIGHEST_PROTOCOL)
            self.transaction_valid[name] = False
            with open('data/transaction_valid.pickle', 'wb') as handle:
                pickle.dump(self.transaction_valid, handle, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            self.mom_overpay_flag = 1
            with open('data/overpay_dad.pickle', 'rb') as handle:
                self.overpay_dad = pickle.load(handle)
            self.overpay_dad.append(name, amount, balance)
            with open('data/overpay_dad.pickle', 'wb') as handle:
                pickle.dump(self.overpay_dad, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # Dad's overpay request function. Dad can either take action or ignore the request.
    # Transaction status stays invalid until changes are made.
    def overpay_req_dad(self):
        with open('data/overpay_dad.pickle', 'rb') as handle:
            self.overpay_dad = pickle.load(handle)
        if self.overpay_dad:
            name = self.overpay_dad[0]
            amount = self.overpay_dad[1]
            balance = self.overpay_dad[2]
            decision = input(
                "Do you want to accept overpay request of ${} for {}? Press (y/n). ".format(amount,
                                                                                            name))
            if decision == "y":
                self.overpay_request[name] = False
                with open('data/overpay_request.pickle', 'wb') as handle:
                    pickle.dump(self.overpay_request, handle, protocol=pickle.HIGHEST_PROTOCOL)
                self.overpay_amount[name] = amount
                with open('data/overpay_amount.pickle', 'wb') as handle:
                    pickle.dump(self.overpay_amount, handle, protocol=pickle.HIGHEST_PROTOCOL)
                print("Your acceptance has been registered")
                self.transaction_valid[name] = True
                with open('data/transaction_valid.pickle', 'wb') as handle:
                    pickle.dump(self.transaction_valid, handle, protocol=pickle.HIGHEST_PROTOCOL)
            elif decision == "n":
                self.overpay_request[name] = False
                with open('data/overpay_request.pickle', 'wb') as handle:
                    pickle.dump(self.overpay_request, handle, protocol=pickle.HIGHEST_PROTOCOL)
                print("Your denial has been registered")
                self.overpay_amount[name] = balance
                with open('data/overpay_amount.pickle', 'wb') as handle:
                    pickle.dump(self.overpay_amount, handle, protocol=pickle.HIGHEST_PROTOCOL)
                self.transaction_valid[name] = False
                with open('data/transaction_valid.pickle', 'wb') as handle:
                    pickle.dump(self.transaction_valid, handle, protocol=pickle.HIGHEST_PROTOCOL)
                self.overpay_dad = []
                with open('data/overpay_dad.pickle', 'wb') as handle:
                    pickle.dump(self.overpay_dad, handle, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            self.overpay_dad = []
            with open('data/overpay_dad.pickle', 'wb') as handle:
                pickle.dump(self.overpay_dad, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print("You have denied the overpay request.. \n You require to change the transaction status manually to "
                  "allow a family member make transactions")

    # Parent wallet notifications function provides all the notifications to the parents including the overpay
    # request, wallet balance request and multiple transaction requests.
    def parent_wallet_notifications(self):
        balance = int(self.wallet_balance)
        if balance < 100 and self.ignore == 0:
            print("\n{}, your family wallet balance is less than $100".format(self.name))
            decision = input("Would you like to deposit some money? Type (y/n)")
            if decision == 'y':
                self.deposit(int(input("Enter the Amount: $")), self.name)
                # ignore flag to not show this message again when user accesses the notifications' menu!
                self.ignore = 1
                input("Press Enter to go back to the menu")
            else:
                self.ignore = 1
                self.parent_wallet_notifications()
        else:
            print("\nHello {}!, your family wallet balance is ${}".format(self.name, self.wallet_balance))
            self.balance_request_check()
            self.permission_request_check()
            with open('data/overpay_request.pickle', 'rb') as handle:
                self.overpay_request = pickle.load(handle)
                #print("Overpay request file", self.overpay_request)
            with open('data/overpay_amount.pickle', 'rb') as handle:
                self.overpay_amount = pickle.load(handle)
                #print("Overpay amount file", self.overpay_amount)
            for name in self.overpay_request:
                with open('data/overpay_request.pickle', 'rb') as handle:
                    self.overpay_request = pickle.load(handle)
                with open('data/overpay_amount.pickle', 'rb') as handle:
                    self.overpay_amount = pickle.load(handle)
                if self.overpay_request[name]:
                    # self.overpay_request = overpay_request
                    for name in self.overpay_request:
                        # print(self.overpay_amount[name])
                        if self.already_accepted_flag == 0:
                            if int(self.overpay_amount[name]) > 50:
                                if self.name == 'mom':
                                    self.overpay_req_mom(name, self.overpay_amount[name],
                                                         self.Kid(name).overpay_amount[name])
                                    self.already_accepted_flag = 1
                                    self.overpay_flag = False
                                elif self.name == 'dad' and self.mom_overpay_flag == 1:
                                    self.overpay_req_dad()
                                    self.already_accepted_flag = 1
                                    self.overpay_flag = False
                else:
                    self.overpay_flag = False
                    # elif name == len(self.overpay_request) - 1:
            if not self.overpay_flag:
                # if not self.overpay_request[name]:
                print("No overpay requests")

            input("Press Enter to go back to the menu")

    # Kid class which includes all the necessary functionality of the kid's section.
    # Every kid object is assigned to this class.

    class Kid:
        def __init__(self, name):
            # Assigned required data files to an object
            self.transaction_list = transaction_list
            self.wallet_balance_request = balance_request
            self.permission_request = permission_request
            #self.kids_list = kids_list
            self.overpay_request = overpay_request
            self.overpay_amount = overpay_amount
            with open('data/overpay_amount.pickle', 'rb') as handle:
                self.overpay_amount = pickle.load(handle)
            self.wallet_balance = wallet_balance
            self.transaction_valid = transaction_valid

            self.transaction_flag = transaction_flag
            self.trans_flag = False

            self.name = name
            self.request = ""
            #self.kids_list = kids_list
            self.use_count = 0
            self.daily_balance = self.daily_balance_refresh(self.name)
            self.wallet_balance_check()
            self.my_wallet = Family_Wallet(self.name)

        # This function automatically checks for the wallet balance and sends request to parents upon user input
        def wallet_balance_check(self):
            if self.wallet_balance < 100:
                decision = input("Your wallet balance is low. Do you want to request your parents for a top up? Type "
                                 "(y/n). ")
                if decision == 'y':
                    self.wallet_balance_request[self.name] = True
                    with open('data/balance_request.pickle', 'wb') as handle:
                        pickle.dump(self.wallet_balance_request, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    print("Your request is sent!")

        @staticmethod
        def daily_balance_refresh(name):
            with open('data/overpay_amount.pickle', 'rb') as handle:
                temp_overpay_amount = pickle.load(handle)
            daily_balance = int(temp_overpay_amount[name])
            return daily_balance

        # def permission_notification(self):
        #     if not self.permission_request[self.name]:
        #         print("You are allowed to pay!")
        #     else:
        #         print("You are not allowed to pay")

        def request_overpay(self, amount):
            decision = input("Would you like to request Mom for overpay? Type (y/n)")
            if decision == 'y':
                self.overpay_request[self.name] = True
                with open('data/overpay_request.pickle', 'wb') as handle:
                    pickle.dump(self.overpay_request, handle, protocol=pickle.HIGHEST_PROTOCOL)
                self.overpay_amount[self.name] = amount
                with open('data/overpay_amount.pickle', 'wb') as handle:
                    pickle.dump(self.overpay_amount, handle, protocol=pickle.HIGHEST_PROTOCOL)
                print("Your request has been sent to Mom")
                input("Press Enter to go back to the menu")

        # This function updates the daily limits with previous day's overall overpay limit count.
        # So that in a new day the limit is set back to $50
        def transaction_reset(self):
            with open('data/transaction_list.pickle', 'rb') as handle:
                self.transaction_list = pickle.load(handle)
            with open('data/transaction_list.pickle', 'rb') as handle:
                self.transaction_list = pickle.load(handle)
            with open('data/overpay_amount.pickle', 'rb') as handle:
                self.overpay_amount = pickle.load(handle)

            tx_done_today = False
            for tx in self.transaction_list:
                if tx[0] == self.name and tx[3] == dateTimeObj.date():
                    tx_done_today = True

            for tx in self.transaction_list:
                if tx[0] == self.name and tx[3] != dateTimeObj.date() and not tx_done_today:
                    self.overpay_amount[self.name] = 50
                    #print("debug: transaction amount reset")
                    with open('data/overpay_amount.pickle', 'wb') as handle:
                        pickle.dump(self.overpay_amount, handle, protocol=pickle.HIGHEST_PROTOCOL)

        # This function performs a kid's transaction by requesting the shop name and amount details and appends it to
        # the transaction list.
        def transaction(self, amount, shop_name):
            with open('data/overpay_amount.pickle', 'rb') as handle:
                self.overpay_amount = pickle.load(handle)
            with open('data/transaction_list.pickle', 'rb') as handle:
                self.transaction_list = pickle.load(handle)
            self.trans_flag = True
            self.transaction_reset()
            with open('data/transaction_valid.pickle', 'rb') as handle:
                self.transaction_valid = pickle.load(handle)

            if int(amount) > int(self.overpay_amount[self.name]) and self.overpay_amount[self.name] !=0:
                self.request_overpay(amount)
            else:
                if self.transaction_valid[self.name]:
                    #print("Transaction is valid")
                    if self.daily_limit_check():
                        logging.info("Transaction: {} {} {}".format(shop_name, amount, dateTimeObj))
                        current_transaction = [self.name, shop_name, amount, dateTimeObj.date()]
                        self.transaction_list.append(current_transaction)
                        with open('data/transaction_list.pickle', 'wb') as handle:
                            pickle.dump(self.transaction_list, handle, protocol=pickle.HIGHEST_PROTOCOL)

                        #print("Debug: Current Transaction", current_transaction)
                        balance_amount = 0
                        with open('data/overpay_amount.pickle', 'rb') as handle:
                            self.overpay_amount = pickle.load(handle)
                        balance_amount = int(self.overpay_amount[self.name]) - int(amount)
                        #print("Debug: Balance Amount = ", balance_amount)
                        with open('data/balance.pickle', 'rb') as handle:
                            self.wallet_balance = pickle.load(handle)
                        self.wallet_balance -= int(amount)
                        with open('data/balance.pickle', 'wb') as handle:
                            pickle.dump(self.wallet_balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
                        self.overpay_amount[self.name] = balance_amount
                        #print("Debug: Overpay Amount List", self.overpay_amount)
                        with open('data/overpay_amount.pickle', 'wb') as handle:
                            pickle.dump(self.overpay_amount, handle, protocol=pickle.HIGHEST_PROTOCOL)
                            #print("Overpay saved during trasnsaction")
                        print("Your transaction is successful")
                    else:
                        print("\n You have exceeded your daily limit! Your request has been registered.")
                else:
                    print("Your transaction status is invalid \n Please request your parents to make changes!")

        # def check_transaction_valid(self):
        #     transaction_validity = self.transaction_valid[self.name]
        #     return transaction_validity

        def daily_limit_check(self):
            with open('data/transaction_flag.pickle', 'rb') as handle:
                self.transaction_flag = pickle.load(handle)
            # print("Trans Flag" ,self.transaction_flag)
            count = 0
            # print("Hello 1 ")

            # if not self.transaction_list:
            #     # print("not transaction list (empty list)", self.transaction_list)
            #     return True
            for tx in self.transaction_list:
                # print("Hello 2 ")
                #print(tx[0], self.name, tx[3], dateTimeObj.date())
                if tx[0] == self.name and tx[3] == dateTimeObj.date():
                    temp_list = [self.name, dateTimeObj.date()]
                    # print(temp_list)
                    count += 1
                    #print("Count is ", count)
                    # self.transaction_valid[self.name] = False
                    # with open('data/transaction_valid.pickle', 'wb') as handle:
                    #     pickle.dump(self.transaction_valid, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    # print("for loop is checking the list", self.transaction_list)
            # print("Final Count: ", count)
            if self.transaction_valid[self.name]:
                #print("Debug: Transaction flag status = ", self.transaction_flag)
                if self.transaction_flag[self.name] != 1:
                    # print("Transaction flag passed")
                    # Note that transaction flag 1 is an exception for making 1 transaction
                    if count > 1:  # and self.transaction_flag[self.name] == 0:
                        decision = input(
                            "You have requested payment for more than once! \n Type '1' to request permission for "
                            "wallet \n Press Enter to go back to the menu")
                        # self.transaction_flag[self.name] = 1
                        # with open('data/transaction_flag.pickle', 'wb') as handle:
                        #     pickle.dump(self.transaction_flag, handle, protocol=pickle.HIGHEST_PROTOCOL)
                        if decision == '1':
                            self.permission_request[self.name] = True
                            # print("Debug: Permission request list", self.permission_request)
                            with open('data/permission_request.pickle', 'wb') as handle:
                                pickle.dump(self.permission_request, handle, protocol=pickle.HIGHEST_PROTOCOL)
                            # print("Debug: Transaction valid list", self.transaction_valid)
                            self.transaction_valid[self.name] = False
                            with open('data/transaction_valid.pickle', 'wb') as handle:
                                pickle.dump(self.transaction_valid, handle, protocol=pickle.HIGHEST_PROTOCOL)
                            # print("Your request has been sent")
                            return False
                        else:
                            self.transaction_flag[self.name] = 0
                            with open('data/transaction_flag.pickle', 'wb') as handle:
                                pickle.dump(self.transaction_flag, handle, protocol=pickle.HIGHEST_PROTOCOL)
                            return False
                    else:
                        self.transaction_flag[self.name] = 0
                        with open('data/transaction_flag.pickle', 'wb') as handle:
                            pickle.dump(self.transaction_flag, handle, protocol=pickle.HIGHEST_PROTOCOL)
                        return True
                else:
                    self.transaction_flag[self.name] = 0
                    with open('data/transaction_flag.pickle', 'wb') as handle:
                        pickle.dump(self.transaction_flag, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    return True

    # Mom's personal banking account related functions
    class Mom:
        def __init__(self):
            self.name = "Sarah Williams"
            self.my_balance = mom_balance
            self.overpay_request = overpay_request
            self.overpay_amount = overpay_amount

        def deposit(self, amount):
            with open('data/mom_balance.pickle', 'rb') as handle:
                self.my_balance = pickle.load(handle)
            self.my_balance += int(amount)
            with open('data/mom_balance.pickle', 'wb') as handle:
                pickle.dump(self.my_balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print("You have deposited $ {}".format(amount))
            print("Your account balance is ${}".format(self.my_balance))
            input("Press Enter to go back to the menu")

        def withdraw(self, amount):
            with open('data/mom_balance.pickle', 'rb') as handle:
                self.my_balance = pickle.load(handle)
            if self.my_balance >= int(amount):
                self.my_balance -= int(amount)
                #print(self.my_balance,"Logging aftrer withdrawal")
                with open('data/mom_balance.pickle', 'wb') as handle:
                    pickle.dump(self.my_balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
                print("Your account balance is ${}".format(self.my_balance))
                print("You have withdrawn $ {}".format(amount))
                input("Press Enter to go back to the menu")
            else:
                print("{}, you have insufficient funds!".format(self.name))

    # Dad's personal banking account related functions
    class Dad:
        def __init__(self):
            self.name = "Williams Hemisphere"
            self.my_balance = dad_balance
            self.overpay_request = overpay_request
            self.overpay_amount = overpay_amount

        def deposit(self, amount):
            with open('data/dad_balance.pickle', 'rb') as handle:
                self.my_balance = pickle.load(handle)
            self.my_balance += int(amount)
            with open('data/dad_balance.pickle', 'wb') as handle:
                pickle.dump(self.my_balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print("You have deposited $ {}".format(amount))
            print("Your account balance is ${}".format(self.my_balance))
            input("Press Enter to go back to the menu")

        def withdraw(self, amount):
            with open('data/dad_balance.pickle', 'rb') as handle:
                self.my_balance = pickle.load(handle)
            if self.my_balance >= int(amount):
                self.my_balance -= int(amount)
                with open('data/dad_balance.pickle', 'wb') as handle:
                    pickle.dump(self.my_balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
                print("Your account balance is ${}".format(self.my_balance))
                print("You have withdrawn $ {}".format(amount))
                input("Press Enter to go back to the menu")
            else:
                print("{}, you have insufficient funds!".format(self.name))


# -------------------x--------------x-----------------x------------------x---------------x----------------x-----------x-
# End of Code
# Author GitHub - @sundarrajnithish
# Submitted to mini project submission for COEN 6311 - Software Engineering (Fall 2022)
# Lecturer - Tariq Daradkeh
