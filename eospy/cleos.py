#
# cleos.py
#

from .dynamic_url import DynamicUrl
from .keys import EOSKey, check_wif
from .utils import sig_digest
from .types import EOSEncoder, Transaction 
import json

class Cleos :
    
    def __init__(self, url='http://localhost:8888', wallet_url='http://localhost:8888', version='v1') :
        ''' '''
        self._prod_url = url
        self._wallet_url = wallet_url
        self._version = version
        self._dynurl = DynamicUrl(url=self._prod_url, version=self._version)
        self._walleturl = DynamicUrl(url=self._wallet_url, version=self._version)
        
    def get(self, func='', **kwargs) :
        ''' '''
        cmd = eval('self._dynurl.{0}'.format(func))
        url = cmd.create_url()
        return cmd.get_url(url, **kwargs)

    def post(self, func='', **kwargs) :
        ''' '''
        cmd = eval('self._dynurl.{0}'.format(func))
        url = cmd.create_url()
        return cmd.post_url(url, **kwargs)
    
    def get_wallet(self, func='', **kwargs) :
        ''' '''
        get_cmd = eval('self._walleturl.{0}'.format(func))
        url = get_cmd.create_url()
        return get_cmd.get_url(url, **kwargs)

    def post_wallet(self, func='', **kwargs) :
        ''' '''
        post_cmd = eval('self._walleturl.{0}'.format(func))
        url = post_cmd.create_url()
        return post_cmd.get_url(url, **kwargs)
    
    #
    # wallet functions
    #
    def wallet_unlock(self, password, name="default",):
        if not password:
            raise NotImplementedError
        return self.post_wallet('wallet.unlock', params=[name,password], json=None)
    
    #####
    # get methods
    #####
    def get_info(self, timeout=30) :
        ''' '''
        return self.get('chain.get_info', timeout=timeout)

    def get_chain_lib_info(self, timeout=30) :
        ''' '''
        chain_info = self.get('chain.get_info', timeout=timeout)
        lib_info = self.get_block(chain_info['last_irreversible_block_num'], timeout=timeout)
        return chain_info, lib_info
        
    def get_block(self, block_num, timeout=30) :
        ''' '''
        return self.post('chain.get_block', params=None, json={'block_num_or_id' : block_num}, timeout=timeout)
        
    def get_account(self, acct_name, timeout=30) :
        ''' '''
        return self.post('chain.get_account', params=None, json={'account_name' : acct_name}, timeout=timeout)

    def get_code(self, acct_name, code_as_wasm=True, timeout=30) :
        ''' '''
        return self.post('chain.get_code', params=None, json={'account_name':acct_name, 'code_as_wasm':code_as_wasm}, timeout=timeout)
    
    def get_accounts(self, public_key, timeout=30) :
        ''' '''
        return self.post('history.get_key_accounts', params=None, json={'public_key':public_key}, timeout=timeout)

    def get_abi(self, acct_name, timeout=30) :
        ''' '''
        return self.post('chain.get_abi', params=None, json={'account_name' : acct_name}, timeout=timeout)
        
    def get_actions(self, acct_name, pos=-1, offset=-20, timeout=30) :
        '''
        POST /v1/history/get_actions
        {"account_name":"eosnewyorkio","pos":-1,"offset":-20}
        '''
        json={'account_name' : acct_name, "pos" : pos, "offset" : offset}
        return self.post('history.get_actions', params=None, json=json, timeout=timeout)

    def get_currency(self, code='eosio.token', symbol='EOS', timeout=30) :
        '''
        POST /v1/chain/get_currency_stats HTTP/1.0
        {"json":false,"code":"eosio.token","symbol":"EOS"}
        '''
        json={'json':False, 'code':code, 'symbol':symbol}
        return self.post('chain.get_currency_stats', params=None, json=json, timeout=timeout)

    def get_currency_balance(self, account, code='eosio.token', symbol='EOS', timeout=30) :
      '''
      POST /v1/chain/get_currency_balance HTTP/1.0
      {"account":"eosio","code":"eosio.token","symbol":"EOS"}
      '''
      json={'account':account, 'code':code, 'symbol':symbol}
      return self.post('chain.get_currency_balance', params=None, json=json, timeout=timeout)

    def get_currency_stats(self, code, symbol, timeout=30) :
        return self.post('chain.get_currency_stats', json={'code':code, 'symbol':symbol})
    
    def get_servants(self, acct_name, timeout=30) :
        ''' '''
        return self.post('account_history.get_controlled_accounts', params=None, json={'controlling_account':acct_name}, timeout=timeout)

    def get_transaction(self, trans_id, timeout=30) :
        '''
        POST /v1/history/get_transaction
        {"id":"abcd1234"}
        '''
        return self.post('history.get_transaction', params=None, json={'id': trans_id}, timeout=timeout)

    def get_table(self, code, scope, table, table_key='', lower_bound='', upper_bound='', limit=10, timeout=30) :
        '''
        POST /v1/chain/get_table_rows
        {"json":true,"code":"eosio","scope":"eosio","table":"producers","table_key":"","lower_bound":"","upper_bound":"","limit":10}
        '''
        json = {"json":True, "code":code, "scope":scope, "table":table, "table_key":table_key, "lower_bound": lower_bound, "upper_bound": upper_bound, "limit": limit}
        return self.post('chain.get_table_rows', params=None, json=json, timeout=timeout)

    def get_producers(self, lower_bound='', limit=50, timeout=30) :
        '''
        POST /v1/chain/get_producers HTTP/1.0
        {"json":true,"lower_bound":"","limit":50}
        '''
        return self.post('chain.get_producers', params=None, json={'json':True, 'lower_bound':lower_bound, 'limit':limit}, timeout=timeout)

    #####
    # transactions
    #####
    def push_transaction(self, transaction, keys, broadcast=True, compression='none', timeout=30) :
        ''' '''
        chain_info,lib_info = self.get_chain_lib_info()
        trx = Transaction(transaction, chain_info, lib_info)
        #encoded = trx.encode()
        digest = sig_digest(trx.encode(), chain_info['chain_id'])
        # sign the transaction
        signatures = []
        if not isinstance(keys, list) :
            keys = [keys]
        for key in keys :
            if check_wif(key) :
                k = EOSKey(key)
            elif isinstance(key, EOSKey) :
                k = key
            else :
                raise ValueError('Must pass a WIF string or EOSKey')
            signatures.append(k.sign(digest))
        # build final trx
        
        final_trx = {
                'compression' : compression,
                'transaction' : trx.__dict__,
                'signatures' : signatures
        }
        data = json.dumps(final_trx, cls=EOSEncoder)
        if broadcast :
            return self.post('chain.push_transaction', params=None, data=data, timeout=timeout)
        return data
        

    def push_block(self, timeout=30) :
        raise NotImplementedError
        
    #####
    # bin/json 
    #####
    
    def abi_bin_to_json(self, code, action, binargs, timeout=30) :
        ''' '''
        json = {'code':code, 'action':action, 'binargs': binargs}
        return self.post('chain.abi_bin_to_json', params=None, json=json, timeout=timeout)

    def abi_json_to_bin(self, code, action, args, timeout=30) :
        ''' '''
        json = {'code':code, 'action':action, 'args': args}
        return self.post('chain.abi_json_to_bin', params=None, json=json, timeout=timeout)
        
    #####
    # create keys
    #####

    def create_key(self) :
        ''' '''
        k = EOSKey()
        return k
        
    #####
    # multisig
    #####
    
    #def multisig_review(self, )
        
    #####
    # system functions
    #####

    def vote_producers(self, voter, proxy, producers) :
        return self.get('chain.abi_json_to_bin', params=None,json={"voter":voter, "proxy":proxy,"producers":producers})


    def create_account(self, creator, creator_privkey, acct_name, owner_key, 
                       active_key='', stake_net='1.0000 EOS', stake_cpu='1.0000 EOS', ramkb=8, permission='active', 
                       transfer=False, broadcast=True, timeout=30) :
        ''' '''

        # check account doesn't exist
        try : 
            self.get_account(acct_name)
            #print('{} already exists.'.format(acct_name))
            raise ValueError('{} already exists.'.format(acct_name))
        except: 
            pass
        if not active_key :
            active_key = owner_key
        # create newaccount trx
        owner_auth = {
                "threshold": 1,
                "keys": [{
                    "key": owner_key,
                    "weight": 1
                }],
                "accounts": [],
                "waits": []
            }
        active_auth ={
                "threshold": 1,
                "keys": [{
                    "key": active_key,
                    "weight": 1
                } ],
                "accounts": [],
                "waits": []
            }
        print({
                'creator' : creator, 
                'name' : acct_name, 
                'owner' : owner_auth, 
                'active' : active_auth
        })
        
        newaccount_data = self.abi_json_to_bin('eosio', 'newaccount',{'creator' : creator, 'name' : acct_name, 'owner': owner_auth, 'active':active_auth})
        print(newaccount_data)
        newaccount_json = {
            'account' : 'eosio',
            'name' : 'newaccount',
            'authorization' : [
            {
                'actor' : creator,
                'permission' : permission
            } ],
            'data' : newaccount_data['binargs']
        }
        # create buyrambytes trx
        buyram_data = self.abi_json_to_bin('eosio', 'buyrambytes', {'payer':creator, 'receiver':acct_name, 'bytes': ramkb*1024})
        buyram_json = {
            'account' : 'eosio',
            'name' : 'buyrambytes',
            'authorization' : [
                {
                    'actor' : creator,
                    'permission' : permission
                } ],
            'data' : buyram_data['binargs']
        }
        # create delegatebw
        delegate_data = self.abi_json_to_bin('eosio', 'delegatebw', 
            {'from': creator, 'receiver': acct_name, 'stake_net_quantity':stake_net, 'stake_cpu_quantity': stake_cpu, 'transfer': transfer })
        delegate_json = {
            'account' : 'eosio',
            'name' : 'delegatebw',
            'authorization' : [
                {
                    'actor' : creator,
                    'permission' : permission
                } ],
            'data' : delegate_data['binargs']
        }

        trx = {"actions":
            [newaccount_json, buyram_json, delegate_json]
        }
        # push transaction
        return self.push_transaction(trx, creator_privkey, broadcast=broadcast, timeout=timeout)

    def register_producer(self) :
        json = {}
        return self.post()
    
    #####
    # wallet functions
    #####
    def wallet_list(self) :
        return self.get_wallet('wallet.list_wallets')
    
    def wallet_open(self, name='default') :
        return self.get_wallet('wallet.open', params=None, json={"wallet_name":name})
    
