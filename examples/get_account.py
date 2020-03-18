from eospy.cleos import Cleos

ce = Cleos(url='https://api.eosargentina.io')

account = input('Account: ')
arguments = {
    "account": "{}".format(account),  # name of the account to search
}

# Get account
get_acc=ce.get_account(arguments['account'])
print(get_acc)
