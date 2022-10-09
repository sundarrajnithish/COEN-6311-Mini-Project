import mom
import dad
import logging
import datetime
import pickle
from wallet import Family_Wallet

my_wallet = Family_Wallet('kulo')
my_mom = mom.Mom()
my_dad = dad.Dad()


#transaction_list = []

with open('kids_transaction.pickle', 'rb') as handle:
    transaction_list = pickle.load(handle)

class Kid:
    def __init__(self, name):
        self.name = name
        self.request = ""
        self.use_count = 0
        self.daily_limit = 50
        Kid.balance_check()

    @staticmethod
    def balance_check():
        if my_wallet.balance < 400:
            Kid.request_for_balance(
                input("Your wallet balance is low. Do you want to request your parents for a top up? Type 'd' for Dad "
                      "and 'm' for Mom"))

    def request_for_balance(self, parent):
        if parent == 'd':
            if my_dad.balance_request(self.name):
                print("Your wallet is recharged")
            else:
                print("Your request is denied")
        elif parent == 'm':
            if my_mom.balance_request(self.name):
                print("Your wallet is recharged")
            else:
                print("Your request is denied")
        else:
            print("Invalid request. Please try again.")
            Kid.balance_check()

    def permission_for_wallet(self):
        if self.use_count > 2 :
            if my_dad.permission_for_wallet(self.name):
                return True
            else:
                return False

    def request_overpay(self, amount):
        decision = input("Would you like to request Mom for overpay? Type (y/n)")
        if decision == 'y':
            my_mom.overpay_request(self.name, amount)

    @staticmethod
    def transaction(amount, shop_name):
        global transaction_list
        dateTimeObj = datetime.datetime.now()
        logging.basicConfig(filename="transaction_log.txt", level=logging.INFO)
        logging.info("{} {} {}".format(shop_name, amount, dateTimeObj))
        transaction_list.append((shop_name, amount, dateTimeObj))
        with open('transaction_list.pickle', 'wb') as handle:
            pickle.dump(transaction_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print(transaction_list)






