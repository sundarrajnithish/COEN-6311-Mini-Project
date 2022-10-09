import pickle
#
# import kids
from wallet import Family_Wallet

with open('dad_balance.pickle', 'rb') as handle:
    balance = pickle.load(handle)


class Dad:
    def __init__(self):
        global balance
        self.my_balance = balance

    def deposit(self, amount):
        self.my_balance += int(amount)
        print("You have deposited $ {}".format(amount))

    def withdraw(self, amount):
        if self.my_balance >= int(amount):
            self.my_balance -= int(amount)
            print("You have withdrawn $ {}".format(amount))
        else:
            print("Dad, you have insufficient funds!")

    def add_to_wallet(self, amount):
        if self.my_balance >= amount:
            self.my_balance -= amount
            Family_Wallet.deposit(amount, "dad")

    @staticmethod
    def balance_request(name):
        decision = input("{} has requested for money in the wallet. Would you like to add funds?. Press (y/n)" .format(name))
        if decision == 'y':
            amount = input("How much would you like to add?")
            Dad.add_to_wallet(amount)
            return True
        else:
            return False

    def permission_for_wallet(self, name):
        decision = input("Do you want to accept {}'s request for multiple access? Type (y/n)".format(name))
        if decision == 'y':
            return True
        else:
            return False

    def view_transaction(self):
        print(kids.transaction_list)


    @staticmethod
    def overpay_request(name, amount):
        decision = input("Do you want to accept overpay request of ${} for {}. Press (y/n)".format(amount, name))
        if decision == "y":
            return True
        else:
            return False

    def block_user(name):
        Family_Wallet.block(name)
