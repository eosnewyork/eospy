import eospy.cleos

ce = eospy.cleos.Cleos(url='http://api.pennstation.eosnewyork.io:7001')

payload = [
        {
            'args': {
                "from": "eosio",  # sender
                "to": "bob123451234",  # receiver
                "quantity": '1.0000 EOS',  # In EOS
                "memo": "EOS to the moon",
            },
            "account": "eosio.token",
            "name": "transfer",
            "authorization": [{
                "actor": "eosio",
                "permission": "active",
            }],
        }
    ]
#Converting payload to binary
data=ce.abi_json_to_bin(payload[0]['account'],payload[0]['name'],payload[0]['args'])
#Inserting payload binary form as "data" field in original payload
payload[0]['data']=data['binargs']
#Removing the arguments field
payload[0].pop('args')
#final transaction formed
trx = {"actions":[payload[0]]}

# use a string or EOSKey for push_transaction
key = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
# use EOSKey:
# import eospy.keys
# key = eospy.keys.EOSKey('5HuaTWKeGzZhqyzuzFAjjFjPnnnjdgcp562oBSS8Wv1qgDSkR2W')
resp = ce.push_transaction(trx, key, broadcast=True)
print('------------------------------------------------')
print(resp)
print('------------------------------------------------')
