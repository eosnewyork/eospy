
import timeit

setup_str = '''
from eospy.cleos import EOSKey
import binascii
k = EOSKey("5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3")
digest=binascii.hexlify("This is a test string1")
'''
number=10
results=timeit.timeit('k.sign(digest)', setup=setup_str, number=number)

print("Ran {} times and averaged {} seconds/run".format(number, results/number))

