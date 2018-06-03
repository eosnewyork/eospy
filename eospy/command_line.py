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
    parser.add_argument('--ram-fee', help='Guesstimate on cost of ram over time', type=float, default=0, action='store', dest='ram_fee')
    parser.add_argument('--num-threads', help='number of threads to run', type=int, default=16, action='store', dest='num_thds')
    parser.add_argument('--out-file', help='out file to right to', default='validation.txt', type=str, action='store', dest='out_file')
    
    args = parser.parse_args()
    # imports
    from threading import Thread
    # global write buffer
    global write_buffer
    write_buffer = []
    # whack the file
    with open(args.out_file,'w') :
        print('Resetting file {}'.format(args.out_file))
    # connect to http endpoint
    ce = Cleos(url=args.url)
    # get chain infomation
    print('Getting chain information')
    info = ce.get_info()
    pprint.pprint(info)

    ########################
    # functions
    ########################
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
            code_diff = '{0} <--> {1}'.format(supplied_hash, code_hash)
            if supplied_hash == code_hash:
                append_output('SUCCESS!!! {0} code hash MATCHES: {1}\n'.format(user, code_diff))
            else :
                append_output('ERROR!!! {0} code hash DO NOT MATCH: {1}\n'.format(user, code_diff))
        else :
            append_output('WARNING --- not checking {0} code matches\n'.format(user))

    def append_output(line) :
        write_buffer.append(line)

    def flush_output() :
        with open(args.out_file,'a') as wb :
            try: 
                line = write_buffer.pop()
                while line :
                    wb.write(str(line))
                    line = write_buffer.pop()
            except IndexError:
                pass

    def check_sys_accounts(acct_name) :
        account_errors = 0
        output = []
        try :
            acct = ce.get_account(acct_name)
        except :
            output.append('ERROR!!! It appears {0} this account was not added.'.format(acct_name))
            account_errors += 1
            exit(1)
        #pprint.pprint(acct)
        # check owner/active is owned by eosio
        for perm in acct['permissions'] :
            accounts = perm['required_auth']['accounts']
            valid_owner = 'eosio'
            if acct_name == valid_owner :
                valid_owner = 'eosio.prods'
            if len(accounts) > 1 or accounts[0]['permission']['actor'] != valid_owner :
                output.append('ERROR!!! accounts for {} is wrong: too many actors {} or bad actor {}'.format(acct_name, len(accounts), accounts[0]['permission']['actor']))
                account_errors += 1
            
        if account_errors == 0 :
            output.append('SUCCESS!!! {0} was created and looks good.'.format(acct_name))
        append_output('\n'.join(output)+'\n')
            
    def check_acct(eth_key, acct_name, acct_key, acct_balance) :
        output = []
        account_errors = 0   
        try:
            acct = ce.get_account(acct_name)
        except :
            output.append('ERROR!!! It appears {0} was not added.'.format(acct_name))
            account_errors += 1
        # redundant check
        if account_errors == 0 and acct_name == acct['account_name'] :         
            # check keys
            for perm in acct['permissions'] :
                for keys in perm['required_auth']['keys'] :
                    if not acct_key == keys['key']:
                        output.append('ERROR!!! {0} has mismatched keys expected {1} and got {2}'.format(acct_name, acct_key, keys['key']))
                        account_errors += 1
            # check last code update
            if u'1970-01-01T00:00:00.000' != acct['last_code_update'] :
                output.append('ERROR!!! this {0}\'s code has been updated'.format(acct_name))
                account_errors += 1
            # check if account is privileged
            if acct['privileged'] :
                output.append('ERROR!!! this {0} has been set to privileged'.format(acct_name))
                account_errors += 1
            # check account balance is correct
            balance = ce.get_currency_balance(acct_name, 'eosio.token', 'EOS')
            if len(balance) != 1 :
                output.append('ERROR!!! account {0} has invalid number of balances: {1}'.format(acct_name,len(balance)) )
                account_errors += 1
            try :
                #poutput.append.poutput.append(acct['total_resources'])
                bal = float(balance[0].strip(' EOS'))
                cpu = float(acct['total_resources']['cpu_weight'].strip(' EOS'))
                net = float(acct['total_resources']['net_weight'].strip(' EOS'))
                total_balance = cpu + net + bal + args.ram_fee
                #output.append('cpu:{:10.4f},net:{:10.4f},bal:{:10.4f},total_balance:{:10.4f},expected_balance:{}'.format(cpu, net, bal, total_balance, acct_balance))
            except Exception as ex:
                total_balance = 0
                output.append(str(ex))
            if not isclose(total_balance, float(acct_balance)):
                output.append('ERROR!!! account {} has invalid balance: {:10.4f} != {:10.4f}'.format(acct_name, float(acct_balance), total_balance))
                account_errors += 1

            if account_errors == 0 :
                output.append('SUCCESS!!! account: {0} appears vaild with {1} EOS, no contract set, and not privileged'.format(acct_name, acct_balance))
        #else :
        #    output.append('ERROR!!! {0} does not appear to exist'.format(acct_name))
        # append all output to global buffer
        append_output('\n'.join(output)+'\n')
        return account_errors

    ########################
    # checks
    ########################
    
    # check snapshot
    if args.snapshot and args.snapshot_hash :
        hash = sha256sum(args.snapshot)
        if hash == args.snapshot_hash :
            append_output('Snapshot matches:\n')
        else :
            append_output('ERROR!!! Snapshots DO NOT MATCH:\n')
        append_output('{0} <--> {1}\n'.format(hash, args.snapshot_hash))
    else :
        append_output('WARNING --- not checking snapshot\n')
    
    # check that the system user's code matches your expectations
    check_code('eosio', args.eosio_code)
    check_code('eosio.token', args.token_code)
    # check privilege 
    check_code('eosio.msig', args.msig_code)
    check_code('eosio.unregd', args.unregd_code)
    
    # check the token create was valid
    if args.currency_chk :
        currency = ce.get_currency('eosio.token', 'EOS')
        curr_string = '{0} <--> {1}'.format(args.currency_chk, currency['EOS']['max_supply'])
        #pappend_output.pappend_output(currency)
        if args.currency_chk == currency['EOS']['max_supply'] :
            append_output('Max EOS supply matches: {0}\n'.format(curr_string))
        else :
            append_output('ERROR!!! discrepency in initial token create: {0}\n'.format(curr_string))
    else :
        append_output('WARNING --- not checking initial token creation\n')
    # write to the log    
    flush_output()
    # check if snapshot is valid
    if args.check_accts :
        # check the system accounts
        for acct in ['eosio', 'eosio.bpay', 'eosio.msig', 'eosio.names','eosio.ram','eosio.ramfee','eosio.saving','eosio.stake','eosio.token', 'eosio.vpay'] :
            check_sys_accounts('{0}'.format(acct))
            
        num_thds = args.num_thds
        if args.truncate_num and args.truncate_num < num_thds :
            append_output(args.truncate_num)
            num_thds = args.truncate_num
        total_account_errors = 0
        # load up the csv file and check accounts
        with open(args.snapshot) as f :
            import csv
            cnt = 0
            snap = list(csv.reader(f, delimiter=',') )
            append_output('Checking {0} accounts\n'.format(len(snap)))
            flush_output()
            #for row in range(len(snap)-num_thds+1) :
            while cnt < len(snap) :
                if args.truncate_num and cnt >= args.truncate_num :
                    append_output('WARNING!!! only checked {0} accounts\n'.format(cnt))
                    break
                threads = []
                cnt_thds=0
                # get list of accounts
                proc_list = snap[cnt:cnt+num_thds]
                while cnt_thds < num_thds :
                    t = Thread(target=check_acct, args=(proc_list[cnt_thds]) )
                    t.start()
                    threads.append(t)
                    cnt_thds += 1
                for thd in threads :
                    thd.join()
                # flush output
                flush_output()             
            
                # increment count/errors
                #total_account_errors += errors
                cnt += num_thds
        #print('Total accounts: {0} with {1} errors'.format(cnt,total_account_errors))
        append_output('Total accounts: {0}\n'.format(cnt))
        flush_output()
    
