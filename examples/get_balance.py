from eospy.cleos import Cleos

ce = Cleos(url='https://api.eosargentina.io')

account = input('Account: ') # name of the account to search
arguments = {
    "account": "{}".format(account),
    "code":"eosio.token",
    "symbol":"EOS",
}

# Get Balance of the account
get_bal=ce.get_currency_balance(arguments['account'], arguments['code'], arguments['symbol'])
print(get_bal)
