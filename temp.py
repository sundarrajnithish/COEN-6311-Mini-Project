# # # # #
# # # # # #from wallet import Family_Walletfrom datetime import datetime
# # # # #
import pickle
# #
# # # #
# # # # input("Press Enter to go back to the menu")
# # # #
# # # if my_mom.balance_request(self.name):
# # #
# # #     if my_dad.balance_request(self.name):
# #
# # # from main_data import Mom
# #
# # # dummy = Mom()
# # # dummy.check_overpay()

transaction_flag = {"jake": 0,
                     "tony": 0,
                     "mickey": 0,
                     "sofia": 0,
                     "mia": 0,
                     "shakira": 0,
                     "amber": 0,
                     "ambani": 0}

with open('data/transaction_flag.pickle', 'wb') as handle:
    pickle.dump(transaction_flag, handle, protocol=pickle.HIGHEST_PROTOCOL)



# #
transaction_valid = {"jake": True,
                     "tony": True,
                     "mickey": True,
                     "sofia": True,
                     "mia": True,
                     "shakira": True,
                     "amber": True,
                     "ambani": True}
# #
# # overpay_amount = {"jake": 50,
# #                   "tony": 50,
# #                   "mickey": 50,
# #                   "sofia": 50,
# #                   "mia": 50,
# #                   "shakira": 50,
# #                   "amber": 50,
# #                   "ambani": 50}
#
# # transaction_list = [('name', 'shop_name', 'amount', 'date_time')]
#
# # # for request in overpay_request:
# # #     if overpay_request[request]:
# # #         print("This is true {}".format(request))
# # #         if overpay_amount[request] > 0:
# # #             print(overpay_amount[request])
# #
# with open('data/transaction_valid.pickle', 'wb') as handle:
#     pickle.dump(transaction_valid, handle, protocol=pickle.HIGHEST_PROTOCOL)
#
# # # #
# # # # #
# # # # # # blocked = ()
# # # # # #
# # # # # #dad_balance = 0
# # # # #
# # # #input("\n Type your name number below for Login: \n 1. Jake Williams \n 2. Tony Williams \n 3. Mickey "
# # #                   # "Williams \n 4. Sofia Williams \n 5. Mia Williams \n 6. Shakira Williams \n 7. Amber Williams \n 8. "
# # #                   # "Ambani Williams \n Your choice: ")
# # # kids_list = ['Jake Williams', 'Tony Williams', "Mickey Williams", "Sofia Williams", "Mia Williams", "Shakira Williams", "Amber Williams", "Ambani Williams"]
# # # with open('kids_list.pickle', 'wb') as handle:
# # #     pickle.dump(kids_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
# # # # # # #
# # # # # # print(blocked)
# # # # #
# # # # # # transaction_list = []
# # # # # #
# # # # # # with open('transaction_list.pickle', 'wb') as handle:
# # # # # #     pickle.dump(transaction_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
# # # # #
# # # # #
# # # # #
# # # # # # dateTimeObj = datetime.now()
# # # # # # print(dateTimeObj.date())
# # # # # #
# # # # # #
# # # # # # wallet = Family_Wallet("nabeel")
# # # # # # #wallet.unblock("nabeel")
# # # # # # wallet.deposit(100, "dad")
# # # # # # #wallet.withdraw(70, "dad")
# # # # # # wallet.bal()
# # # # # #
# # # # # # wallet.block('nabeel')
# # # # # # #wallet.check_block(("kulo"))
# # # # # # #wallet.overpay_request("sarah")
