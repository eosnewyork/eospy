import argparse
from .cleos import Cleos
import json

def console_print(data):
    print(json.dumps(data, indent=4))

def cleos():
    parser = argparse.ArgumentParser(description='Command Line Interface to EOSIO via python')
    parser.add_argument('--api-version','-v', type=str, default='v1', action='store', dest='api_version')
    parser.add_argument('--url', '-u', type=str, action='store', default='https://api.eosnewyork.io', dest='url')
    parser.add_argument('--time-out', type=int, action='store', default=30, dest='timeout')
    subparsers = parser.add_subparsers(dest='subparser')
    # get
    get_parser = subparsers.add_parser('get')
    get_subparsers = get_parser.add_subparsers(dest='get')
    # info
    get_subparsers.add_parser('info')
    # block
    block_parser = get_subparsers.add_parser('block')
    #block_parser.add_argument('block', type=str)
    block_parser.add_argument('--block','-b', type=str, action='store', required=True, dest='block')
    # account
    account_parser = get_subparsers.add_parser('account')
    account_parser.add_argument('--account','-a', type=str, action='store', required=True, dest='account')
    #account_parser.add_argument('account', type=str)
    # code
    code_parser = get_subparsers.add_parser('code')
    code_parser.add_argument('--account','-a', type=str, action='store', required=True, dest='account')
    #code_parser.add_argument('account', type=str)
    # abi
    abi_parser = get_subparsers.add_parser('abi')
    abi_parser.add_argument('--account','-a', type=str, action='store', required=True, dest='account')
    #abi_parser.add_argument('account', type=str)
    # table
    table_parser = get_subparsers.add_parser('table')
    table_parser.add_argument('--code', '-c', type=str, action='store', required=True, dest='code')
    table_parser.add_argument('--scope', '-S', type=str, action='store', required=True, dest='scope')
    table_parser.add_argument('--table','-t', type=str, action='store', required=True, dest='table')
    #table_parser.add_argument('contract', type=str, help='The contract who owns the table (required)')
    #table_parser.add_argument('scope', type=str, help='The scope within the contract in which the table is found (required)')
    #table_parser.add_argument('table', type=str, help='The name of the table as specified by the contract abi (required)')
    table_parser.add_argument('--table-key', type=str, action='store', default="", dest='table_key', help='The maximum number of rows to return')
    table_parser.add_argument('--lower-bound', type=int, action='store', default=0, dest='lower_bound', help='The name of the key to index by as defined by the abi, defaults to primary key')
    table_parser.add_argument('--upper-bound', type=int, action='store', default=-1, dest='upper_bound')
    table_parser.add_argument('--limit', type=int, action='store', default=1000, dest='limit')
    # currency
    currency = get_subparsers.add_parser('currency')
    currency.add_argument('type',choices=['balance','stats'], type=str)
    currency.add_argument('--code','-c', type=str, action='store', required=True, dest='code')
    currency.add_argument('--symbol','-s', type=str, action='store', required=True, dest='symbol')
    currency.add_argument('--account','-a', type=str, action='store', dest='account')
    # accounts
    accounts = get_subparsers.add_parser('accounts')
    accounts.add_argument('--key','-k', type=str, action='store', required=True, dest='key')
    # transaction
    transaction = get_subparsers.add_parser('transaction')
    transaction.add_argument('--transaction','-t', type=str, action='store', required=True, dest='transaction')
    # actions
    actions = get_subparsers.add_parser('actions')
    actions.add_argument('--account','-a', type=str, action='store', required=True, dest='account')
    actions.add_argument('--pos', type=int, action='store', default=-1, dest='pos')
    actions.add_argument('--offset', type=int, action='store', default=-20, dest='offset')
    # bin2json
    bin_json = get_subparsers.add_parser('bin2json')
    bin_json.add_argument('--code','-c', type=str, action='store', required=True, dest='code')
    bin_json.add_argument('--action','-a', type=str, action='store', required=True, dest='action')
    bin_json.add_argument('--binargs','-b', type=str, action='store', required=True, dest='binargs')
    # json2bin
    # create
    create_parser = subparsers.add_parser('create')
    create_subparsers = create_parser.add_subparsers(dest='create')
    # create EOS key
    create_subparsers.add_parser('key')
    # system commands
    system_parser = subparsers.add_parser('system')
    system_subparsers = system_parser.add_subparsers(dest='system')
    # account
    newacct_parser = system_subparsers.add_parser('newaccount')
    newacct_parser.add_argument('creator', type=str, action='store')
    newacct_parser.add_argument('creator_key', type=str, action='store')
    newacct_parser.add_argument('account', type=str, action='store')
    newacct_parser.add_argument('owner', type=str, action='store')
    newacct_parser.add_argument('--active','-a', type=str, action='store', dest='active')
    newacct_parser.add_argument('--stake-net', type=str, action='store', default='1.0000 EOS', dest='stake_net')
    newacct_parser.add_argument('--stake-cpu', type=str, action='store', default='1.0000 EOS', dest='stake_cpu')
    newacct_parser.add_argument('--buy-ram-kbytes', type=int, action='store', default=8, dest='ramkb')
    newacct_parser.add_argument('--permission','-p', type=str, action='store', default='active', dest='permission')
    newacct_parser.add_argument('--transfer', action='store_true', default=False, dest='transfer')
    newacct_parser.add_argument('--broadcast', action='store_false', default=True, dest='broadcast')
    # process args
    args = parser.parse_args()
    # 
    # connect 
    ce = Cleos(url=args.url, version=args.api_version)

    # run commands based on subparser
    if args.subparser == 'get' :
        if args.get == 'info' :
            console_print(ce.get_info(timeout=args.timeout))
        elif args.get == 'block' :
            console_print(ce.get_block(args.block, timeout=args.timeout))
        elif args.get == 'account' :
            console_print(ce.get_account(args.account, timeout=args.timeout))
        elif args.get == 'code' :
            console_print(ce.get_code(args.account, timeout=args.timeout))
        elif args.get == 'abi' :
            console_print(ce.get_abi(args.account, timeout=args.timeout))
        elif args.get == 'table' :
            table = ce.get_table(code=args.code, scope=args.scope, table=args.table, table_key=args.table_key, lower_bound=args.lower_bound, upper_bound=args.upper_bound, limit=args.limit, timeout=args.timeout)
            console_print(table)
        elif args.get == 'currency' :
            if args.type == 'balance' :
                if args.account :
                    console_print(ce.get_currency_balance(args.account, code=args.code, symbol=args.symbol, timeout=args.timeout))
                else :
                    raise ValueError('--account is required')
            else :
                console_print(ce.get_currency(code=args.code, symbol=args.symbol, timeout=args.timeout))
        elif args.get == 'accounts' :
            console_print(ce.get_accounts(args.key, timeout=args.timeout))
        elif args.get == 'transaction' :
            console_print(ce.get_transaction(args.transaction, timeout=args.timeout))
        elif args.get == 'actions' :
            console_print(ce.get_actions(args.account, pos=args.pos, offset=args.offset, timeout=args.timeout))
        elif args.get == 'bin2json' :
            console_print(ce.abi_bin_to_json(args.code, args.action, args.binargs, timeout=args.timeout))
    elif args.subparser == 'create' :
        if args.create == 'key' :
            k = ce.create_key()
            print('Private key:{}'.format(k.to_wif()))
            print('Public key: {}'.format(k.to_public()))
    elif args.subparser == 'system' :
        if args.system == 'newaccount' :
            resp = ce.create_account(args.creator, args.creator_key, args.account, args.owner, args.active, 
                                     stake_net=args.stake_net, stake_cpu=args.stake_cpu, ramkb=args.ramkb, 
                                     permission=args.permission, transfer=args.transfer, broadcast=args.transfer, 
                                     timeout=args.timeout)
            console_print(resp)

