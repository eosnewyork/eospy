#
# cleos.py
#

from dynamic_url import DynamicUrl
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
        print(''+url)
        return get_cmd.get_url(url, **kwargs)

    #
    # get methods
    #
    
    def get_info(self) :
        ''' '''
        return self.get('chain.get_info')
    
    def get_block(self, block_num) :
        ''' '''
        return self.get('chain.get_block', params=None, json={'block_num_or_id' : block_num})

    def get_account(self, acct_name) :
        ''' '''
        return self.post('chain.get_account', params=None, json={'account_name' : acct_name})

    def get_code(self, acct_name, code_as_wasm=False) :
        ''' '''
        return self.post('chain.get_code', params=None, json={'account_name':acct_name, 'code_as_wasm':code_as_wasm})
    
    def get_table(self) :
        ''' '''
        raise NotImplementedError

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
    
    def get_accounts(self, public_key) :
        ''' '''
        return self.get('account_history.get_key_accounts', params=None, json={'public_key':public_key})

    def get_servants(self, acct_name) :
        ''' '''
        return self.get('account_history.get_controlled_accounts', params=None, json={'controlling_account':acct_name})

    def get_transaction(self, trans_id) :
        ''' '''
        return self.get('account_history.get_transaction', params=None, json={'transaction_id':trans_id})
    #####
    # system functions
    #####

    def vote_producers(self, voter, proxy, producers) :
        return self.get('chain.abi_json_to_bin', params=None,json={"voter":voter, "proxy":proxy,"producers":producers})

    #####
    # wallet functions
    #####
    def wallet_list(self) :
        return self.get_wallet('wallet.list_wallets')
    
    def wallet_open(self, name='default') :
        return self.get_wallet('wallet.open', params=None, json={"wallet_name":name})
    
