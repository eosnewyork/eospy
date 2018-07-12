import base58
import hashlib
import os
import ecdsa
import re
from binascii import hexlify, unhexlify

def sha256(data):
    ''' '''
    return hashlib.sha256(data).hexdigest()

def ripemd160(data):
    ''' '''
    h = hashlib.new('ripemd160')
    h.update(data)
    return h.hexdigest()
    
def create_entropy( cpu_entropy=0 ) :
    '''    '''
    ba = bytearray(os.urandom(32))
    seed = sha256(ba)
    return ecdsa.util.PRNG(seed)

def check_encode(key_buffer, key_type=None) :
    '''    '''
    if key_type == 'sha256x2' :
        first_sha = sha256(unhexlify(key_buffer))
        chksum = sha256(unhexlify(first_sha))[:8]
        return base58.b58encode(unhexlify(key_buffer+chksum))
    else :
        check = key_buffer
        if key_type :
            check += key_type
        chksum = ripemd160(unhexlify(check))[:8]
        return base58.b58encode(unhexlify(check+chksum))
    
def check_decode(key_string, key_type=None) :
    '''    '''
    buffer = hexlify(base58.b58decode(key_string))
    chksum = buffer[-8:]
    key = buffer[:-8]
    if key_type == 'sha256x2' :
        # legacy
        first_sha = sha256(unhexlify(key))
        newChk = sha256(unhexlify(first_sha))[:8]
    else :
        check = key
        if key_type :
            check += key_type
        newChk = ripemd160(unhexlify(check))[:8]

    if chksum != newChk :
        raise ValueError('checksums do not match: {0} != {1}'.format(chksum, newChk))

    return key

class EOSKey :
    def __init__(self, private_str='') :
        ''' '''
        if private_str :
            private_key, format, key_type = self._parse_key(private_str)
            self._sk = ecdsa.SigningKey.from_string(unhexlify(private_key), curve=ecdsa.SECP256k1)
        else :
            self._sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self._vk = self._sk.get_verifying_key()
        
    def _parse_key(self, private_str) :
        ''' '''
        match = re.search('^PVT_([A-Za-z0-9]+)_([A-Za-z0-9]+)$', private_str)
        if not match :
            # legacy WIF - format            
            version_key = check_decode(private_str, 'sha256x2')
            # ensure first 2 chars == 0x80
            version = int(version_key[0:2],16)
            if not version == 0x80 :
                raise ValueError('Expected version 0x80, instead got {0}', version)
            private_key = version_key[2:]
            key_type = 'K1'
            format = 'WIF'
        else :
            key_type, key_string = match.groups()
            private_key = check_decode(key_string, key_type)
            format = 'PVT'
        return (private_key, format, key_type)

    def _compress_pubkey(self) :
        ''' '''
        order = self._sk.curve.generator.order()
        p = self._vk.pubkey.point
        x_str = ecdsa.util.number_to_string(p.x(), order)
        compressed = hexlify(bytes(chr(2 + (p.y() & 1))) + x_str)
        return compressed

    def to_public(self) :
        ''' '''
        cmp = self._compress_pubkey()
        return 'EOS' + check_encode(cmp)
        
    def to_wif(self) :
        ''' '''
        pri_key = '80' + hexlify(self._sk.to_string())
        return check_encode(pri_key, 'sha256x2')

