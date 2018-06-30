# eospy library

This library is very much a work in progress however it has enough implemented to validate a chain.

## Installation

```
# create virtual environment
mkdir -p ~/envs/eospy
virtualenv ~/envs/eospy
# activate the environment
source ~/envs/eospy/bin/activate
# install the library
pip install git+https://github.com/eosnewyork/eospy
```

## Command line Tool Examples
```
# Get chain information
pycleos --url https://api.eosnewyork.io get info

# get information about a block
pycleos --url https://api.eosnewyork.io get block 447

# Retrieve an account from the blockchain
pycloes --url https://api.eosnewyork.io get account --account eosio

# Retrieve the code and ABI for an account
pycleos --url https://api.eosnewyork.io get code --account eosio

# Retrieve the ABI for an account
pycleos --url https://api.eosnewyork.io get abi --account eosio

# Retrieve the contents of a database table
pycleos --url https://api.eosnewyork.io get table --code eosio --scope eosio --table producers

# Retrive currency information
pycleos --url https://api.eosnewyork.io get currency balance --code eosio.token --symbol EOS --account aaaaaaaaaaaa
pycleos --url https://api.eosnewyork.io get currency stats --code eosio.token --symbol EOS

# get accounts associated with public key
pycleos --url https://api.eosnewyork.io get accounts --key EOS52gpRqAPfggYHLXbMuC4TSQd8WWWo94KrMq4umgUcjM62Y2dWF

# get transaction information
pycleos --url https://api.eosnewyork.io get transaction --transaction 42dacd5722001b734be46a2140917e06cd21d42425f927f506c07b4388b07f62

# get account actions
pycleos --url https://api.eosnewyork.io get actions --account aaaaaaaaaaaa

```

## More Documentation to come!!!!

## Chain Validation
To validate a chain run something like the following:

```
validate_chain --url http://localhost:8888 \
               --snapshot ~/git/eosnewyork/snapshots/348/0/snapshot.csv \
               --snapshot-hash 08526b5373761badde60423ccb1d6d12ab920268f9c9a2f3b77250ff93d7f6e1 \
               --eosio-code 21c6343a1c7cda9b14e34d46764b41dbe6b0377568af9c44517dc7980d6a774c \
               --token-code 3e0cf4172ab025f9fff5f1db11ee8a34d44779492e1d668ae1dc2d129e865348 \
               --msig-code 5cf017909547b2d69cee5f01c53fe90f3ab193c57108f81a17f0716a4c83f9c0 \
               --unregd-code 6c48d8a571e74e6d0cd1e42aac154d35392b6766b6390351ef6a3632be584fa0 \
               --currency-check "10000000000.0000 EOS" \
               --check-accounts \
               --truncate 20 

```

Walking through the above command options:

```
# the --url is used to point to a chain http(s) endpoint 
--url http://35.190.58.19:80
# the local snapshot file
--snapshot ~/git/eosnewyork/snapshots/348/0/snapshot.csv
# the sha256 hash of the snapshot file
--snapshot-hash 08526b5373761badde60423ccb1d6d12ab920268f9c9a2f3b77250ff93d7f6e1
# (optional) the eosio contract hash returned from `cleos get code eosio`
--eosio-code 21c6343a1c7cda9b14e34d46764b41dbe6b0377568af9c44517dc7980d6a774c
# (optional) the eosio.token contract hash returned from `cleos get code eosio.token
--token-code 3e0cf4172ab025f9fff5f1db11ee8a34d44779492e1d668ae1dc2d129e865348
# (optional) the eosio.msig contract hash returned from `cleos get code eosio.msig`
--msig-code 5cf017909547b2d69cee5f01c53fe90f3ab193c57108f81a17f0716a4c83f9c0 
# (optional) the eosio.unregd (if implemented) contract hash returned from `cleos get code eosio.unregd`
--unregd-code 6c48d8a571e74e6d0cd1e42aac154d35392b6766b6390351ef6a3632be584fa0 
# (optional) amount of EOS that should have been issued
--currency-check "10000000000.0000 EOS" 
# boolean flag to determine if you want to check if the accounts have the correct balances 
--check-accounts
# (optional) only to be used when you only want to check the first <n> of accounts
--truncate 20

```
