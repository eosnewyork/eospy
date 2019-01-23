import eospy.cleos
import os

ce = eospy.cleos.Cleos(url='http://api.pennstation.eosnewyork.io:7001')

arguments = {
            "from": "eosio",  # sender
            "to": "bob123451234",  # receiver
            "quantity": '1.0000 EOS',  # In EOS
            "memo": "EOS to the moon",
        }
payload = {
        "account": "eosio.token",
        "name": "transfer",
        "authorization": [{
            "actor": "eosio",
            "permission": "active",
        }],
    }
#Converting payload to binary
data=ce.abi_json_to_bin(payload['account'],payload['name'],arguments)
#Inserting payload binary form as "data" field in original payload
payload['data']=data['binargs']
#final transaction formed
trx = {"actions": [payload]}

# use a string or EOSKey for push_transaction
key = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
# use EOSKey:
# import eospy.keys
# key = eospy.keys.EOSKey('5HuaTWKeGzZhqyzuzFAjjFjPnnnjdgcp562oBSS8Wv1qgDSkR2W')
resp = ce.push_transaction(trx, key, broadcast=True)
print('------------------------------------------------')
print(resp)
print('------------------------------------------------')

script_dir = os.path.dirname(os.path.realpath(__file__))
key_file = os.path.join(script_dir,'pennstation_eosio.key')

# wait to send transaction
import time
print('Pushing a transaction after 10 seconds using key_file: {}'.format(key_file))
time.sleep(10)

arguments = {
            "from": "eosio",  # sender
            "to": "bob123451234",  # receiver
            "quantity": '2.0000 EOS',  # In EOS
            "memo": "EOS to the moon",
        }

#Converting payload to binary
data=ce.abi_json_to_bin(payload['account'],payload['name'],arguments)
#Inserting payload binary form as "data" field in original payload
payload['data']=data['binargs']
#final transaction formed
trx = {"actions": [payload]}

resp = ce.push_transaction(trx, key_file, broadcast=True)
print('------------------------------------------------')
print(resp)
print('------------------------------------------------')
