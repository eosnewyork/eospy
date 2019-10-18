from eospy.cleos import EOSKey
import binascii

# public key EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV
k = EOSKey("5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3")

digest = b"9d8815193d76ee236ef08e8b9fb675e6def3af8d8209d7665540ab9e17944e19"

sig = k.sign(digest)
print(sig)

# sign string
print("string: " + k.sign_string("i am a string"))

# signed by EOS5YMv2UBcuiExv1C8fZjjnE4evofRdBh5Nrt8TYz44G7KC5tZNq
sig = "SIG_K1_K7RtmvZ7k3oNUqZFHGJJrtJBsA2NW2w7LC25c8M45t2MEQcARbnVSVQzL3toFvF48ujjhGnaFi5Z89ZFYNvtDbTY5NCV4T"
trx_digest = b"29218b0d9dbfa0a4cd5b19256f23d70ebd36f7624f392fac562bbaa61c7087b0"
print("should be False: " + str(k.verify(sig, digest)))
