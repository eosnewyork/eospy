#
# cleos.py
#

from .dynamic_url import DynamicUrl
from .keys import EOSKey
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
    
    #
    # get methods
    #
    
    def get_info(self) :
        ''' '''
        return self.get('chain.get_info')
    
    def get_block(self, block_num) :
        ''' '''
        return self.post('chain.get_block', params=None, json={'block_num_or_id' : block_num})

    def get_account(self, acct_name) :
        ''' '''
        return self.post('chain.get_account', params=None, json={'account_name' : acct_name})

    def get_code(self, acct_name, code_as_wasm=False) :
        ''' '''
        return self.post('chain.get_code', params=None, json={'account_name':acct_name, 'code_as_wasm':code_as_wasm})
    
    def get_accounts(self, public_key) :
        ''' '''
        return self.post('history.get_key_accounts', params=None, json={'public_key':public_key})

    def get_abi(self, acct_name) :
        ''' '''
        return self.post('chain.get_abi', params=None, json={'account_name' : acct_name})
        
    def get_actions(self, acct_name, pos=-1, offset=-20) :
        '''
        POST /v1/history/get_actions
        {"account_name":"eosnewyorkio","pos":-1,"offset":-20}
        '''
        json={'account_name' : acct_name, "pos" : pos, "offset" : offset}
        return self.post('history.get_actions', params=None, json=json)

    def get_currency(self, code='eosio.token', symbol='EOS') :
        '''
        POST /v1/chain/get_currency_stats HTTP/1.0
        {"json":false,"code":"eosio.token","symbol":"EOS"}
        '''
        json={'json':False, 'code':code, 'symbol':symbol}
        return self.post('chain.get_currency_stats', params=None, json=json)

    def get_currency_balance(self, account, code='eosio.token', symbol='EOS') :
      '''
      POST /v1/chain/get_currency_balance HTTP/1.0
      {"account":"eosio","code":"eosio.token","symbol":"EOS"}
      '''
      json={'account':account, 'code':code, 'symbol':symbol}
      return self.post('chain.get_currency_balance', params=None, json=json)
    
    def get_servants(self, acct_name) :
        ''' '''
        return self.post('account_history.get_controlled_accounts', params=None, json={'controlling_account':acct_name})

    def get_transaction(self, trans_id) :
        ''' '''
        return self.post('history.get_transaction', params=None, json={'transaction_id':trans_id})

    def get_table(self, code, scope, table, table_key, lower_bound='0', upper_bound='-1', limit=10) :
        '''
        POST /v1/chain/get_table_rows
        {"json":true,"code":"eosio","scope":"eosio","table":"producers","table_key":"","lower_bound":"","upper_bound":"","limit":10}
        '''
        json = {"json":True, "code":code, "scope":scope, "table":table, "table_key":table_key, "lower_bound": lower_bound, "upper_bound": upper_bound, "limit": limit}
        return self.post('chain.get_table_rows', params=None, json=json)

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

    def create_account(self, creator, acct_name, owner_key, active_key, stake, cpu, ramkb) :
        ram_json = {'code':'eosio','action':'buy', 'args':{'payer':'eosio', 'receiver':acct_name, 'bytes': ramkb*1024} }
        ram_ret = self.post('chain.abi_json_to_bin',params=None, json=json)

    def register_producer() :
        json = {}
        return self.post()
    
    #####
    # wallet functions
    #####
    def wallet_list(self) :
        return self.get_wallet('wallet.list_wallets')
    
    def wallet_open(self, name='default') :
        return self.get_wallet('wallet.open', params=None, json={"wallet_name":name})
    
