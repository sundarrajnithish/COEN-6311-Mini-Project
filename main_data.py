from datetime import datetime
import logging
import pickle
import time

dateTimeObj = datetime.now()
logging.basicConfig(filename="log.txt", level=logging.INFO)


####### Family Wallet ###################

class Family_Wallet:
    def __init__(self, name):
        with open('blocked.pickle', 'rb') as handle:
            blocked = pickle.load(handle)
        with open('balance.pickle', 'rb') as handle:
            wallet_balance = pickle.load(handle)
        with open('overpay_request.pickle', 'rb') as handle:
            self.overpay_request = pickle.load(handle)
        with open('overpay_amount.pickle', 'rb') as handle:
            self.overpay_amount = pickle.load(handle)
        self.ignore = 0
        self.name = name
        self.balance = wallet_balance
        self.blocked = []
        [self.blocked.append(x) for x in blocked if x not in self.blocked]
        # print(self.blocked)
        # print("Block list before changes {}".format(self.blocked))
        for names in self.blocked:
            if names == self.name:
                print("{} you dont have access to the wallet".format(name))
                logging.info("Wallet tried to access by {} {}".format(name, dateTimeObj))

        # print("Welcome {}".format(name))
        logging.info("Wallet accessed by {} {}".format(name, dateTimeObj))

    def family_wallet(self):
        balances = self.balance
        print("Available Balance = ${}".format(balances))
        decision = input("You have accessed the family wallet section: \n Please type any of the options below:  \n "
                         "1. Deposit \n 2. Withdraw \n 3. View Transactions \n 4. Notifications \n 5. Main Menu")
        if decision == '1':
            self.deposit(int(input("How much would you like to deposit? $")), 'mom')
            input("Press Enter to go back to the menu")
            self.family_wallet()
        if decision == '2':
            self.withdraw(int(input("How much would you like to withdraw? $")), 'mom')
            self.family_wallet()
        if decision == '3':
            Kid.view_transaction_list()
            self.family_wallet()
        if decision == '4':
            self.my_notifications()
            self.family_wallet()
        if decision == '5':
            print("Loading...")
            time.sleep(1)

    def my_notifications(self):
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
                self.my_notifications()
        else:
            print("\nHello {}!, your family wallet balance is ${}".format(self.name, balance))
            overpay_check = self.check_overpay()
            if overpay_check:
                for name in self.overpay_request:
                    if self.overpay_amount[name] > 0:
                        self.overpay_req(name, self.overpay_amount[name])
            else:
                print("No overpay request")
            input("Press Enter to go back to the menu")

    def check_overpay(self):
        for name in self.overpay_request:
            if self.overpay_request[name]:
                return True
            else:
                return False

    @staticmethod
    def overpay_req(name, amount):
        decision = input("Do you want to accept overpay request of ${} for {}? Press (y/n). Press any other key to "
                         "request Dad".format(amount, name))
        if decision == "y":
            print("true")
            return True
        elif decision == "n":
            print("false")
            return False


    def deposit(self, amount, member):
        if member == "dad" or member == "mom":
            self.balance += amount
            with open('balance.pickle', 'wb') as handle:
                pickle.dump(self.balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print("\n Amount Deposited:", amount)
            logging.info("{}'s deposit for ${} accepted {}".format(member, amount, dateTimeObj))
        else:
            print("You cannot deposit")
            logging.info("{}'s deposit for ${} denied {}".format(member, amount, dateTimeObj))

    def withdraw(self, amount, member):
        if self.balance >= amount:
            if member == "dad" or member == "mom":
                self.balance -= amount
                with open('balance.pickle', 'wb') as handle:
                    pickle.dump(self.balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
                print("Amount Withdrawn: ${}".format(amount))
                logging.info("{} Withdraw {} {}".format(member, amount, dateTimeObj))
            elif member == "kid" and amount <= 50:
                self.balance -= amount
                with open('balance.pickle', 'wb') as handle:
                    pickle.dump(self.balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
                logging.info("{} Withdraw {} {}".format(member, amount, dateTimeObj))
            else:
                print("You have exceeded your daily limit")
                logging.info("Accessed Family Wallet {}".format(dateTimeObj))
        else:
            print("\n Insufficient balance  ")
            logging.info("Insufficient Balance {} {}".format(member, dateTimeObj))

    def balance(self):
        print("\n Net Available Balance=", self.balance)
        with open('balance.pickle', 'wb') as handle:
            pickle.dump(self.balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return self.balance

    def block(self, name):
        temp_blocklist = []
        for names in self.blocked:
            if names == name:
                print("{} is already blocked".format(name))
            else:
                temp_blocklist.append(name)
                [temp_blocklist.append(x) for x in self.blocked if x not in temp_blocklist]

        self.blocked = temp_blocklist
        with open('blocked.pickle', 'wb') as handle:
            pickle.dump(self.blocked, handle, protocol=pickle.HIGHEST_PROTOCOL)

        print("Blocked members {}".format(self.blocked))

        exit()

    def unblock(self, name):
        for names in self.blocked:
            if names == name:
                self.blocked.remove(str(name))
        with open('blocked.pickle', 'wb') as handle:
            pickle.dump(self.blocked, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print("Unblock function {}".format(self.blocked))

    def notification(self, name):
        names = name
        print("    NOTIFICATIONS")

    def check_block(self, name):
        for names in self.blocked:
            if names == name:
                return True

    # def overpay_request(self, name):
    #     if self.check_block(name):
    #         print("You don't have access {}".format(name))
    #     else:
    #         return True


############# Dad #############

with open('dad_balance.pickle', 'rb') as handle:
    dad_balance = pickle.load(handle)


class Dad:
    def __init__(self):
        global dad_balance
        self.my_balance = dad_balance

    @staticmethod
    def my_name():
        return 'Williams Hemisphere'

    def deposit(self, amount):
        self.my_balance += int(amount)
        print("You have deposited $ {}".format(amount))

    def withdraw(self, amount):
        if self.my_balance >= int(amount):
            self.my_balance -= int(amount)
            print("You have withdrawn $ {}".format(amount))
            print("Your account balance is ${}".format(self.my_balance))
        else:
            print("Dad, you have insufficient funds!")

    def add_to_wallet(self, amount):
        if self.my_balance >= amount:
            self.my_balance -= amount
            Family_Wallet.deposit(amount, "dad")

    @staticmethod
    def balance_request(name):
        decision = input(
            "{} has requested for money in the wallet. Would you like to add funds?. Press (y/n)".format(name))
        if decision == 'y':
            amount = input("How much would you like to add?")
            Dad.add_to_wallet(amount)
            return True
        else:
            return False

    @staticmethod
    def permission_for_wallet(name):
        decision = input("Do you want to accept {}'s request for multiple access? Type (y/n)".format(name))
        if decision == 'y':
            return True
        else:
            return False

    @staticmethod
    def view_transaction():
        print(transaction_list)

    @staticmethod
    def overpay_request(name, amount):
        decision = input("Do you want to accept overpay request of ${} for {}. Press (y/n)".format(amount, name))
        if decision == "y":
            return True
        else:
            return False

    def block_user(name):
        Family_Wallet.block(name)


# All the functions in Mom's view

dad_permission = Dad()

with open('mom_balance.pickle', 'rb') as handle:
    mom_balance = pickle.load(handle)


class Mom:
    def __init__(self):
        global mom_balance
        self.my_balance = mom_balance
        with open('mom_balance.pickle', 'wb') as handle:
            pickle.dump(self.my_balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open('overpay_request.pickle', 'rb') as handle:
            self.overpay_request = pickle.load(handle)
        with open('overpay_amount.pickle', 'rb') as handle:
            self.overpay_amount = pickle.load(handle)
        # with open('overpay_request.pickle', 'wb') as handle:
        #     pickle.dump(self.overpay_request, handle, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def my_name():
        return 'Sarah Williams'

    # def my_notifications(self):
    #     balance = Family_Wallet.balance()
    #     if self.ignore == 0:
    #         if balance < 100:
    #             print("\n{}, your family wallet balance is less than $100".format(self.my_name))
    #             decision = input("Would you like to deposit some money? Type (y/n)")
    #             if decision == 'y':
    #                 Family_Wallet.deposit(int(input("Enter the Amount: $")), 'mom')
    #                 self.ignore = 1
    #                 input("Press Enter to go back to the menu")
    #             else:
    #                 self.ignore = 1
    #                 self.my_notifications()
    #     elif self.ignore == 1:
    #         print("\nHello {}!, your family wallet balance is ${}".format(self.my_name(), balance))
    #         self.overpay_req(self.check_overpay())
    #         input("Press Enter to go back to the menu")

    # def check_overpay(self):
    #     for name in self.overpay_request:
    #         if self.overpay_request[name]:
    #             if self.overpay_amount[name] > 0:
    #                 return name, self.overpay_amount[name]
    #             else:
    #                 print("No amount request!")

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
            print("Mom, you have insufficient funds!")

    def add_to_wallet(self, amount):
        if self.my_balance >= int(amount):
            self.my_balance -= int(amount)
            with open('mom_balance.pickle', 'wb') as handle:
                pickle.dump(self.my_balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
            Family_Wallet.deposit(amount, "mom")

    @staticmethod
    def view_transaction():
        print(transaction_list)

    @staticmethod
    def balance_request(name):
        decision = input(
            "{} has requested for money in the wallet. Would you like to add funds?. Press (y/n)".format(name))
        if decision == 'y':
            amount = int(input("How much would you like to add?"))
            Mom.add_to_wallet(amount)
            return True
        else:
            return False

    # @staticmethod
    # def overpay_req(name, amount):
    #     decision = input("Do you want to accept overpay request of ${} for {}? Press (y/n). Press any other key to "
    #                      "request Dad".format(amount, name))
    #     if decision == "y":
    #         return True
    #     elif decision == "n":
    #         return False
    #     else:
    #         dad_permission.overpay_request()


####### KIDS ############

my_mom = Mom()
my_dad = Dad()

with open('kids_transaction.pickle', 'rb') as handle:
    transaction_list = pickle.load(handle)


class Kid:
    def __init__(self, name):
        with open('kids_list.pickle', 'rb') as handle:
            kids_list = pickle.load(handle)
        with open('overpay_request.pickle', 'rb') as handle:
            self.overpay_request = pickle.load(handle)
        with open('overpay_amount.pickle', 'rb') as handle:
            self.overpay_amount = pickle.load(handle)
        self.name = name
        self.request = ""
        self.kids_list = kids_list
        self.use_count = 0
        self.daily_balance = 50
        self.overpay_amount = 0
        self.balance_check()
        self.my_wallet = Family_Wallet(self.name)

    def daily_limit(self):
        return print(self.daily_limit())

    @staticmethod
    def view_transaction_list():
        if not transaction_list:
            print("No transactions have been made")
        else:
            print("Transaction List")
            print(transaction_list)

    def balance_check(self):
        if self.daily_balance < 400:
            self.request_for_balance(
                input("Your wallet balance is low. Do you want to request your parents for a top up? Type 'd' for Dad "
                      "and 'm' for Mom"))

    def request_for_balance(self, parent):
        if parent == 'd':
            print("Your request is sent!")
        if parent == 'm':
            print("Your request is sent!")
        else:
            print("Invalid request. Please try again.")
            self.balance_check()

    def permission_for_wallet(self):
        if self.use_count > 2:
            if my_dad.permission_for_wallet(self.name):
                return True
            else:
                return False

    def request_overpay(self, amount):
        decision = input("Would you like to request Mom for overpay? Type (y/n)")
        if decision == 'y':
            self.overpay_request[self.name] = True
            self.overpay_amount[self.name] = amount
            print("Your request has been sent to Mom")

    def transaction(self, amount, shop_name):
        global transaction_list
        if amount > 50:
            self.request_overpay(amount)
        else:
            logging.basicConfig(filename="transaction_log.txt", level=logging.INFO)
            logging.info("{} {} {}".format(shop_name, amount, dateTimeObj))
            transaction_list.append((shop_name, amount, dateTimeObj))
            with open('transaction_list.pickle', 'wb') as handle:
                pickle.dump(transaction_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print(transaction_list)
