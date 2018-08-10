import eospy.cleos

ce = eospy.cleos.Cleos(url='http://api.pennstation.eosnewyork.io:7001')

data = ce.abi_json_to_bin('eosio.token', 'transfer', {"from":"eosio", "to":"bob123451234", "quantity" : "1.0000 EOS", "memo":"test"})
print(data)

# create base transaction
trx = {"actions":[{"account":"eosio.token","name":"transfer","authorization":[{"actor":"eosio","permission":"active"}],"data":data['binargs']}]}

print('actions: '+str(trx))

# use a string or EOSKey for push_transaction
key = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
# use EOSKey:
# import eospy.keys
# key = eospy.keys.EOSKey('5HuaTWKeGzZhqyzuzFAjjFjPnnnjdgcp562oBSS8Wv1qgDSkR2W')
resp = ce.push_transaction(trx, key, broadcast=True)
print('------------------------------------------------')
print(resp)
print('------------------------------------------------')
