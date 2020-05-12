from eospy.cleos import Cleos

ce = Cleos(url='http://192.168.1.205:8888')

block = ce.get_block(120283689, "trace")

trx_cnt = len(block["transactions"])
act_cnt = 0
for trx in block["transactions"]:
    act_cnt += len(trx["actions"])

print("Transaction count: {} and action count: {}".format(trx_cnt, act_cnt))