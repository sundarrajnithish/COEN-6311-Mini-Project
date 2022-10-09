# from wallet import Family_Wallet
import dad as Dad
import pickle

dad_permission = Dad.Dad()

with open('mom_balance.pickle', 'rb') as handle:
    balance = pickle.load(handle)


class Mom:
    def __init__(self):
        global balance
        self.my_balance = balance
        with open('mom_balance.pickle', 'wb') as handle:
            pickle.dump(self.my_balance, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def deposit(self, amount):
        self.my_balance += int(amount)
        with open('mom_balance.pickle', 'wb') as handle:
            pickle.dump(self.my_balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print("You have deposited $ {}".format(amount))

    def withdraw(self, amount):
        if self.my_balance >= int(amount):
            self.my_balance -= int(amount)
            with open('mom_balance.pickle', 'wb') as handle:
                pickle.dump(self.my_balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print("You have withdrawn $ {}". format(amount))
        else:
            print("Mom, you have insufficient funds!")

    def add_to_wallet(self, amount):
        if self.my_balance >= int(amount):
            self.my_balance -= int(amount)
            with open('mom_balance.pickle', 'wb') as handle:
                pickle.dump(self.my_balance, handle, protocol=pickle.HIGHEST_PROTOCOL)
            Family_Wallet.deposit(amount, "mom")

    def balance_request(self, name):
        decision = input("{} has requested for money in the wallet. Would you like to add funds?. Press (y/n)" .format(name))
        if decision == 'y':
            amount = int(input("How much would you like to add?"))
            Mom.add_to_wallet(amount)
            return True
        else:
            return False

    @staticmethod
    def overpay_request(name, amount):
        decision = input("Do you want to accept overpay request of ${} for {}? Press (y/n). Press any other key to "
                         "request Dad".format(amount, name))
        if decision == "y":
            return True
        elif decision == "n":
            return False
        else:
            dad_permission.overpay_request()
