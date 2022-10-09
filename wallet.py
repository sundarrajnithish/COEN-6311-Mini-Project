from datetime import datetime
import logging
import pickle

dateTimeObj = datetime.now()
logging.basicConfig(filename="log.txt", level=logging.INFO)

with open('blocked.pickle', 'rb') as handle:
    blocked = pickle.load(handle)


class Family_Wallet:
    def __init__(self, name):
        self.name = name
        self.balance = 0
        global blocked
        self.blocked = []
        [self.blocked.append(x) for x in blocked if x not in self.blocked]
        print(self.blocked)
        print("Block list before changes {}".format(self.blocked))
        for names in self.blocked:
            if names == self.name:
                print("{} you dont have access to the wallet".format(name))
                logging.info("Wallet tried to access by {} {}".format(name, dateTimeObj))

        print("Welcome {}".format(name))
        logging.info("Wallet accessed by {} {}".format(name, dateTimeObj))

    def deposit(self, amount, member):
        if member == "dad" or member == "mom":
            self.balance += amount
            print("\n Amount Deposited:", amount)
            logging.info("{}'s deposit for ${} accepted {}".format(member, amount, dateTimeObj))
        else:
            print("You cannot deposit")
            logging.info("{}'s deposit for ${} denied {}".format(member, amount, dateTimeObj))

    def withdraw(self, amount, member):
        if self.balance >= amount:
            if member == "dad" or member == "mom":
                self.balance -= amount
                logging.info("{} Withdraw {} {}".format(member, amount, dateTimeObj))
            elif member == "kid" and amount <= 50:
                self.balance -= amount
                logging.info("{} Withdraw {} {}".format(member, amount, dateTimeObj))
            else:
                print("You have exceeded your member limit")
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

        exit()

    def check_block(self, name):
        global blocked
        for names in blocked:
            if names == name:
                return True

        exit()

    def overpay_request(self, name):
        if self.check_block(name):
            print("You don't have access {}".format(name))
        else:
            return True

        exit()
