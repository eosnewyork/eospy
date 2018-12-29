
from .schema import ActionSchema, PermissionLevelSchema, ChainInfoSchema, BlockInfoSchema, TransactionSchema
import datetime as dt
import pytz
from .utils import sha256, string_to_name, int_to_hex
import json
import binascii
import struct
import six

def convert_little_endian(buf, format='q') :
    ''' '''
    return struct.pack('<{}'.format(format), buf)

def convert_big_endian(buf) :
    ''' '''
    return struct.pack('>{}'.format(format), buf)

# json encoder
class EOSEncoder(json.JSONEncoder) :
    def default(self, o) :
        if isinstance(o, Action) :
            return o.__dict__
        if isinstance(o, Authorization) :
            return o.__dict__
        if isinstance(o, dt.datetime) :
            return o.isoformat()

class Name(str) : pass
class AccountName(Name) : pass
class PermissionName(Name) : pass
class ActionName(Name) : pass
class TableName(Name) : pass
class ScopeName(Name) : pass

class Byte(int) : pass
class UInt16(int) : pass
class UInt32(int) : pass
class UInt64(int) : pass

if six.PY3 :
    class long(int) : pass

class VarUInt :
    def __init__(self, val):
        ''' '''
        self._val = val
        self._b_arr = bytearray()

    def _push_byte(self, val) :
        self._b_arr.append(int(val))
    
    def encode(self) :
        ''' '''
        # ensure value is an int
        val = int(self._val)
        buf = (val) & 0x7f
        val >>= 7
        buf |= (((val > 0) if 1 else 0) << 7)
        self._push_byte(buf)
        while val :
            buf = int((val) & 0x7f)
            val >>= 7
            buf |= (((val > 0) if 1 else 0) << 7)
            self._push_byte(buf)
        return self._b_arr

#
class BaseObject(object) :
    def __init__(self, d) :
        ''' '''
        self._obj = self._validator.deserialize(d)
        # instantiate the class
        for k,v in self._obj.items() :
            setattr(self, k, v)
        # clean up
        del self._obj
        del self._validator
        
    def __repr__(self) :
        ''' '''
        return '{}({})'.format(self.__class__, self.__dict__)
        
    def _encode_buffer(self, value) :
        ''' '''
        return EOSBuffer(value).encode()

    def _create_obj_array(self, arr, class_type) :
        ''' '''
        new_arr = []
        for item in arr :
            new_arr.append(class_type(item))
        return new_arr

class Action(BaseObject) :
    def __init__(self, d) :
        ''' '''
        self._validator = ActionSchema()
        super(Action, self).__init__(d)
        # setup permissions
        self.authorization = self._create_obj_array(self.authorization, Authorization)
        
    def encode(self) :
        ''' '''
        acct = self._encode_buffer(AccountName(self.account))
        name = self._encode_buffer(Name(self.name))
        auth = self._encode_buffer(self.authorization)
        # need to figure out how to process data
        # get length
        data_len = self._encode_buffer(VarUInt(len(self.data)/2))
        data =  data_len + self.data
        return '{}{}{}{}'.format(acct, name, auth, data)

class Asset :
    def __init__(self, amt=0.0000, sym='EOS') :
        self.amount = amt
        self.symbol = sym

    def __str__(self) :
        return '{0:.4f} {1}'.format(self.amount, self.symbol)
        
    def __add__(self, other) :
        if self.symbol != other.symbol :
            raise TypeError('Symbols must match: {} != {}', self.symbol, other.symbol)
        return Asset(self.amount+other.amount, self.symbol)

    def __sub__(self, other) :
        if self.amount - other.amount < 0 :
            raise ValueError('Subtraction would result in a negative.')
        if self.symbol != other.symbol :
            raise TypeError('Symbols must match: {} != {}', self.symbol, other.symbol)
        return Asset(self.amount-other.amount, self.symbol)

    def from_string(self, s) :
        splt = s.split()
        try :
            self.amount = float(splt[0])
            self.symbol = splt[1]
        except IndexError:
            raise IndexError('Invalid string format given. Must be in the formst <float> <currency_type>')
        
class Authorization(BaseObject):
    def __init__(self, d) :
        ''' '''
        # create validator
        self._validator = PermissionLevelSchema()
        super(Authorization, self).__init__(d)

    def encode(self) :
        ''' '''
        actor = self._encode_buffer(AccountName(self.actor))
        perms = self._encode_buffer(PermissionName(self.permission))
        return '{}{}'.format(actor, perms)

class ChainInfo(BaseObject) :
    def __init__(self, d) :
        ''' '''
        self._validator = ChainInfoSchema()
        super(ChainInfo, self).__init__(d)

class BlockInfo(BaseObject) :
    def __init__(self, d) :
        ''' '''
        self._validator = BlockInfoSchema()
        super(BlockInfo, self).__init__(d)


class Transaction(BaseObject) :
    def __init__(self, d, chain_info, lib_info) :
        ''' '''
        # add defaults
        if 'expiration' not in d :
            d['expiration'] = str((dt.datetime.utcnow() + dt.timedelta(seconds=30)).replace(tzinfo=pytz.UTC))
        if 'ref_block_num' not in d :
            d['ref_block_num'] = chain_info['last_irreversible_block_num'] & 0xFFFF
        if 'ref_block_prefix' not in d :
            d['ref_block_prefix'] = lib_info['ref_block_prefix']
        # validate
        self._validator = TransactionSchema()
        super(Transaction, self).__init__(d)
        # parse actions
        self.actions = self._create_obj_array(self.actions, Action)
    
    def _encode_hdr(self) :
        ''' '''
        # convert
        tz = dt.tzinfo(self.expiration)
        exp_ts = (self.expiration - dt.datetime(1970, 1, 1, tzinfo=self.expiration.tzinfo)).total_seconds()
        exp = self._encode_buffer(UInt32(exp_ts))
        ref_blk = self._encode_buffer(UInt16(self.ref_block_num))
        ref_block_prefix = self._encode_buffer(UInt32(self.ref_block_prefix))
        net_usage_words = self._encode_buffer(VarUInt(self.net_usage_words))
        max_cpu_usage_ms = self._encode_buffer(Byte(self.max_cpu_usage_ms))
        delay_sec = self._encode_buffer(VarUInt(self.delay_sec))
        # create hdr buffer
        hdr = '{}{}{}{}{}{}'.format(exp, ref_blk, ref_block_prefix, net_usage_words, max_cpu_usage_ms, delay_sec)
        return hdr

    def encode(self) :
        ''' '''
        hdr_buf = self._encode_hdr()
        context_actions = self._encode_buffer(self.context_free_actions)
        actions = self._encode_buffer(self.actions)
        trans_exts = self._encode_buffer(self.transaction_extensions)
        return bytearray.fromhex(hdr_buf + context_actions + actions + trans_exts)
        
    def get_id(self) :
        return sha256(self.encode())

class EOSBuffer :
    def __init__(self, v) :
        self._value = v
        self._count = 0
    
    def _write_number(self, val, format='q') :
        ''' '''
        le = convert_little_endian(val, format)
        return binascii.hexlify(le).decode()

    def _write_name(self, w_str) :
        ''' '''
        val = string_to_name(w_str)
        le = convert_little_endian(val, 'Q')
        return binascii.hexlify(le).decode()

    def _write_str(self, w_str) :
        return binascii.hexlify(chr(len(w_str)) +w_str).decode()

    def _write_varuint(self, vuint) :
        buf = vuint.encode()
        return binascii.hexlify(buf).decode()
        
    def encode(self, val=None) :
        if not val :
            val = self._value
        if (isinstance(val, Name) or
           isinstance(val, AccountName) or
           isinstance(val, PermissionName) or
           isinstance(val, ActionName) or
           isinstance(val, TableName) or
           isinstance(val, ScopeName) ) :
            val = self._write_name(val)
            return val
        elif(isinstance(val, str)) :
            return self._write_str(val)
        elif(isinstance(val, Byte) or
             isinstance(val, bool)) :
            #return self._write_number(val, '?')
            return int_to_hex(val)
        elif(isinstance(val, UInt16)) :
            return self._write_number(val, 'H')
        elif(isinstance(val,UInt32)) :
            return self._write_number(val, 'I')
        elif(isinstance(val,VarUInt)) :
            # temp encoding
            return self._write_varuint(val)
        elif(isinstance(val, int) or
             isinstance(val, long)) :
            return self._write_number(val, 'l')
        elif(isinstance(val, Authorization)) :
            return val.encode()
        elif(isinstance(val, Action)) :
            return val.encode()
        elif(isinstance(val, list)) :
            buf = self._write_varuint(VarUInt(len(val))) 
            for item in val :
                e_item = self.encode(item)
                buf = '{}{}'.format(buf, e_item)
            return buf
        else :
            raise TypeError('Invalid type {} specified'.format(type(val)))
        
