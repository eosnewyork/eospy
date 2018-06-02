import argparse
from cleos import Cleos
import pprint


def vote_for_bps():
    parser = argparse.ArgumentParser(description='vote for block producers')
    parser.add_argument('--api-version', type=str, default='v1', action='store', dest='api_version')
    parser.add_argument('--url', type=str, action='store', required=True, dest='url')
    parser.add_argument('--wallet-url', type=str, action='store', required=True, dest='wallet_url')
    parser.add_argument('--wallet-name', type=str, default='default', action='store', dest='wallet_name')
    raise NotImplementedError
    args = parser.parse_args()
    # connect to http endpoint
    ce = Cleos(url=args.url, wallet_url=args.wallet_url, version=args.api_version)
    # get chain infomation
    info = ce.get_info()
    pprint.pprint(info)
    wallets = ce.wallet_list()
    if args.wallet_name in wallets :
        print('Wallet {0} already exists',args.wallet_name)
    else :
        print('creating wallet')
    open_wallet = ce.wallet_open()
    pprint.pprint(open_wallet)

def validate_chain():
    parser = argparse.ArgumentParser(description='validate the chain')
    parser.add_argument('--api-version', help='version of the api to connect to', type=str, default='v1', action='store', dest='api_version')
    parser.add_argument('--url',help='url endpoint for the chain', type=str, action='store', required=True, dest='url')
    parser.add_argument('--truncate', help='Used for testing only. Will only look at the <n> number of accounts', type=int, default=0, action='store', dest='truncate_num')
    parser.add_argument('--snapshot', help='snapshot file to checkout', type=str, action='store', dest='snapshot')
    parser.add_argument('--snapshot-hash', help='expected hash of the snapshot', type=str, action='store', dest='snapshot_hash')
    parser.add_argument('--check-accounts', help='Whether to check the snapshot accounts',  action='store_true', dest='check_accts')
    parser.add_argument('--ignore-errors', help='Whether to run through the whole process or exit on first error',  action='store_true', dest='ignore_errors')
    parser.add_argument('--eosio-code', help='expected hash of the eosio system contract', type=str, action='store', dest='eosio_code')
    parser.add_argument('--token-code', help='expected hash of the eosio.token contract', type=str, action='store', dest='token_code')
    parser.add_argument('--msig-code', help='expected hash of the eosio.msig contract', type=str, action='store', dest='msig_code')
    parser.add_argument('--unregd-code', help='expected hash of the eosio.unregd contract', type=str, action='store', dest='unregd_code')
    parser.add_argument('--currency-check',help='expected hash of the eosio system contract', type=str, action='store', dest='currency_chk')
    parser.add_argument('--check-sys-accounts', help='check the system accounts are all correct', action='store_true', dest='check_sys_accts')
    args = parser.parse_args()

    # connect to http endpoint
    ce = Cleos(url=args.url)
    # get chain infomation
    print('Getting chain information')
    info = ce.get_info()
    pprint.pprint(info)

    try:
        # if python 3
        from math import isclose
    except :
        # running in python 2
        def isclose(a, b, rel_tol=1e-09, abs_tol=0.0) :
            return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
    
    def sha256sum(fname) :
        import hashlib
        hash_sha256 = hashlib.sha256()
        with open(fname, "rb") as f :
            for chunk in iter(lambda: f.read(4096), b"") :
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def check_code(user, supplied_hash) :
        ''' '''
        if supplied_hash :
            code = ce.get_code(user)
            code_hash = code['code_hash']
            if supplied_hash == code_hash:
                print('SUCCESS!!! {0} code hash MATCHES:'.format(user))
            else :
                print('HELP!!! {0} code hash DO NOT MATCH:'.format(user))
            print('{0} <--> {1}'.format(supplied_hash, code_hash))
        else :
            print('WARNING --- not checking {0} code matches'.format(user))
            
    # check snapshot
    if args.snapshot and args.snapshot_hash :
        hash = sha256sum(args.snapshot)
        if hash == args.snapshot_hash :
            print('Snapshot matches:')
        else :
            print('HELP!!! Snapshots DO NOT MATCH:')
        print('{0} <--> {1}'.format(hash, args.snapshot_hash))
    else :
        print('WARNING --- not checking snapshot')
    
    # check that the system user's code matches your expectations
    check_code('eosio', args.eosio_code)
    check_code('eosio.token', args.token_code)
    # check privilege 
    check_code('eosio.msig', args.msig_code)
    check_code('eosio.unregd', args.unregd_code)

    # check the token create was valid
    if args.currency_chk :
        currency = ce.get_currency('eosio.token', 'EOS')
        #pprint.pprint(currency)
        if args.currency_chk == currency['EOS']['max_supply'] :
            print('Max EOS supply matches:')
        else :
            print('HELP!!! discrepency in initial token create')
        print('{0} <--> {1}'.format(args.currency_chk, currency['EOS']['max_supply']))
    else :
        print('WARNING --- not checking initial token creation')
       
    # check if snapshot is valid
    if args.check_accts :
        total_account_errors = 0
        # load up the csv file and check accounts
        with open(args.snapshot) as f :
            import csv
            cnt = 0
            snap = csv.reader(f, delimiter=',')
            for row in snap :
                account_errors = 0
                if args.truncate_num and cnt >= args.truncate_num :
                    print('WARNING!!! only checked {0} accounts'.format(cnt))
                    break
                # parse row
                acct_name = row[1]
                acct_key = row[2]
                acct_balance = row[3]
                try:
                    acct = ce.get_account(acct_name)
                except :
                    print('HELP!!! It appears {0} this account was not added.'.format(acct_name))
                    if not args.ignore_errors :
                        exit(1)
                    account_errors = 0
                # redundant check
                if acct_name == acct['account_name'] :
                    # check keys
                    for perm in acct['permissions'] :
                        for keys in perm['required_auth']['keys'] :
                            if not acct_key == keys['key']:
                                print('HELP!!! {0} has mismatched keys expected {0} and got {1}'.format(acct_key, key))
                                if not args.ignore_errors :
                                    exit(1)
                                account_errors += 1
                    # check last code update
                    if u'1970-01-01T00:00:00.000' != acct['last_code_update'] :
                        print('HELP!!! this {0}\'s code has been updated'.format(acct_name))
                        if not args.ignore_errors :
                            exit(1)
                        account_errors += 1
                    # check if account is privileged
                    if acct['privileged'] :
                        print('HELP!!! this {0} has been set to privileged'.format(acct_name))
                        if not args.ignore_errors :
                            exit(1)
                        account_errors += 1
                    # check account balance is correct
                    balance = ce.get_currency_balance(acct_name, 'eosio.token', 'EOS')
                    if len(balance) != 1 :
                        print('HELP!!! account {0} has invalid number of balances'.format(acct_name))
                        if not args.ignore_errors :
                            exit(1)
                        account_errors += 1
                    try :
                        #pprint.pprint(acct['total_resources'])
                        bal = float(balance[0].strip(' EOS'))
                        cpu = float(acct['total_resources']['cpu_weight'].strip(' EOS'))
                        net = float(acct['total_resources']['net_weight'].strip(' EOS'))
                        # add plus one for ram
                        total_balance = cpu + net + bal + float(0.1)
                        #print('{:10.4f} {:10.4f} {:10.4f} {:10.4f} {}'.format(cpu, net, bal, total_balance, acct_balance))
                    except Exception as ex:
                        total_balance = 0
                        print(ex)
                    if not isclose(total_balance, float(acct_balance)):
                        print('HELP!!! account {0} has invalid balance'.format(acct_name))
                        print('{:10.4f} != {:10.4f}'.format(float(acct_balance), total_balance))
                        if not args.ignore_errors :
                            exit(1)
                        account_errors += 1
                    if account_errors == 0 :
                        print('SUCCESS!!! account: {0} appears vaild with {1} EOS, no contract set, and not privileged'.format(acct_name, acct_balance))
                    else :
                        print('This account had {0} failure(s)'.format(account_errors))
                        total_account_errors += account_errors
                else :
                    print('HELP!!! account name did not match for some reason')
                    print('This is a nightmare how did this happen?')
                    print('{0} != {1}'.format(acct_name, acct['account_name']))
                    exit(1)
                # increment count
                cnt += 1
        print('Total accounts: {0} with {1} errors'.format(cnt,total_account_errors))

    
