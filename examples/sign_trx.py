
import timeit

setup_str = '''
from eospy.cleos import EOSKey
import binascii
k = EOSKey("5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3")
digest=binascii.hexlify(b"This is a test string1")
'''
number=10
key_results=timeit.timeit('k=EOSKey("5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3")',
                          setup="from eospy.cleos import EOSKey", number=number)
print("Creating Key: Ran {} times and averaged {} seconds/run".format(number, key_results/number))

results=timeit.timeit('k.sign(digest)', setup=setup_str, number=number)

print("Signing: Ran {} times and averaged {} seconds/run".format(number, results/number))

