# eospy library

This library is still a work in progress but currently has the ability to perform all `cleos get` functions without compiling the code.

The library now supports signing transactions/key creation for both python 2.7 and 3.x. This is the first iteration and is very rough. The key creation has not been tested fully and should be used at your own risk.

The cleos commands currently implemented.
```
Usage: /usr/local/bin/cleos get SUBCOMMAND

Subcommands:
  get
    info                        Get current blockchain information
    block                       Retrieve a full block from the blockchain
    account                     Retrieve an account from the blockchain
    code                        Retrieve the code and ABI for an account
    abi                         Retrieve the ABI for an account
    table                       Retrieve the contents of a database table
    currency                    Retrieve information related to standard currencies
    accounts                    Retrieve accounts associated with a public key
    servants                    Retrieve accounts which are servants of a given account
    transaction                 Retrieve a transaction from the blockchain
    actions                     Retrieve all actions with specific account name referenced in authorization or receiver
  system
    newaccount                  Create an account, buy ram, stake for bandwidth for the account
```

This library is very much a work in progress.

## Installation

### Linux
```
# create virtual environment
mkdir -p ~/envs/eospy
virtualenv ~/envs/eospy
# activate the environment
source ~/envs/eospy/bin/activate
# install the library
pip install git+https://github.com/eosnewyork/eospy
```

### Windows

1. Install python
You can use either Python 2.7 or 3.7 however we suggest python 3.7 as we have tested that version more thoroughly.
https://www.howtogeek.com/197947/how-to-install-python-on-windows/
[Python 2.7](https://www.python.org/downloads/release/python-2715/)
[Python 3.7](https://www.python.org/downloads/release/python-370/)

2. Install git
https://www.atlassian.com/git/tutorials/install-git

3. Install eospy
```
pip install git+https://github.com/eosnewyork/eospy
```

## API Endpoints
For a more complete list of API endpoints check out:

https://www.eosdocs.io/resources/apiendpoints/

## Command line Tool Examples
```
# Get chain information
pycleos --url https://api.eosnewyork.io get info

# get information about a block
pycleos --url https://api.eosnewyork.io get block 447

# Retrieve an account from the blockchain
pycleos --url https://api.eosnewyork.io get account --account eosio

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

## Examples

Check out the examples directory for some examples of how to use the library

