from eospy.cleos import Cleos

ce = Cleos(url='https://api.eosargentina.io')

# Get info
get_info=ce.get_info()
print(get_info)

# Get head block number from info
head = get_info['head_block_num']
print('Head Block number is', head)
