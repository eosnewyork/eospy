# serializaion library that mimics fcbuffer in https://github.com/EOS-Mainnet/eosjs-fcbuffer

import binascii
import struct
from .utils import string_to_name, int_to_hex
from .types import Name, AccountName, PermissionName, ActionName, TableName, ScopeName, Byte, UInt16, UInt32, VarUInt, Authorization, Action

def convert_little_endian(buf, format='q') :
    ''' '''
    return struct.pack('<{}'.format(format), buf)

def convert_big_endian(buf) :
    ''' '''
    return struct.pack('>{}'.format(format), buf)

class EOSBuffer :
    def __init__(self, v) :
        self._value = v
        self._count = 0
    
    def _write_number(self, val, format='q') :
        ''' '''
        le = convert_little_endian(val, format)
        return binascii.hexlify(le)

    def _write_name(self, w_str) :
        ''' '''
        val = string_to_name(w_str)
        le = convert_little_endian(val, 'Q')
        return binascii.hexlify(le)

    def _write_str(self, w_str) :
        return binascii.hexlify(chr(len(w_str)) +w_str)

    def _write_varuint(self, vuint) :
        buf = vuint.encode()
        return binascii.hexlify(buf)
        
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
        
