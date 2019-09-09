import base58
import os
import ecdsa
import re
from binascii import hexlify, unhexlify
from .utils import sha256, ripemd160, str_to_hex, hex_to_int
from .signer import Signer
import hashlib
import time
import struct
import array

def check_wif(key) :
    if isinstance(key, str) :
        try :
            EOSKey(key)
            return True
        except Exception as ex:
            pass
    return False

class EOSKey(Signer) :
    def __init__(self, private_str='') :
        ''' '''
        if private_str :
            private_key, format, key_type = self._parse_key(private_str)
            self._sk = ecdsa.SigningKey.from_string(unhexlify(private_key), curve=ecdsa.SECP256k1)
        else :
            prng = self._create_entropy()
            self._sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1, entropy=prng)
        self._vk = self._sk.get_verifying_key()

    def __str__(self) :
        return self.to_public()
        
    def _parse_key(self, private_str) :
        ''' '''
        match = re.search('^PVT_([A-Za-z0-9]+)_([A-Za-z0-9]+)$', private_str)
        if not match :
            # legacy WIF - format            
            version_key = self._check_decode(private_str, 'sha256x2')
            # ensure first 2 chars == 0x80
            version = int(version_key[0:2],16)
            if not version == 0x80 :
                raise ValueError('Expected version 0x80, instead got {0}', version)
            private_key = version_key[2:]
            key_type = 'K1'
            format = 'WIF'
        else :
            key_type, key_string = match.groups()
            private_key = self._check_decode(key_string, key_type)
            format = 'PVT'
        return (private_key, format, key_type)

    def _create_entropy(self) :
        ''' '''
        ba = bytearray(os.urandom(32))
        seed = sha256(ba)
        return ecdsa.util.PRNG(seed)

    def _check_encode(self, key_buffer, key_type=None) :
        '''    '''
        if isinstance(key_buffer, bytes) :
            key_buffer = key_buffer.decode()
        check = key_buffer
        if key_type == 'sha256x2' :
            first_sha = sha256(unhexlify(check))
            chksum = sha256(unhexlify(first_sha))[:8]
        else :
            if key_type :
                check += hexlify(bytearray(key_type,'utf-8')).decode()
            chksum = ripemd160(unhexlify(check))[:8]
        return base58.b58encode(unhexlify(key_buffer+chksum))
   
    def _check_decode(self, key_string, key_type=None) :
        '''    '''
        buffer = hexlify(base58.b58decode(key_string)).decode()
        chksum = buffer[-8:]
        key = buffer[:-8]
        if key_type == 'sha256x2' :
            # legacy
            first_sha = sha256(unhexlify(key))
            newChk = sha256(unhexlify(first_sha))[:8]
        else :
            check = key
            if key_type :
                check += hexlify(bytearray(key_type, 'utf-8')).decode()
            newChk = ripemd160(unhexlify(check))[:8]
        #print('newChk: '+newChk)
        if chksum != newChk :
            raise ValueError('checksums do not match: {0} != {1}'.format(chksum, newChk))
        return key


    def _recover_key(self, digest, signature, i) :
        ''' Recover the public key from the sig
            http://www.secg.org/sec1-v2.pdf
        '''
        curve = ecdsa.SECP256k1.curve
        G = ecdsa.SECP256k1.generator
        order = ecdsa.SECP256k1.order
        yp = (i %2)
        r, s = ecdsa.util.sigdecode_string(signature, order)
        x = r + (i // 2 ) * order
        alpha = ((x * x * x) + (curve.a() * x) + curve.b()) % curve.p()
        beta = ecdsa.numbertheory.square_root_mod_prime(alpha, curve.p())
        y = beta if (beta - yp) % 2 == 0 else curve.p() - beta
        # generate R
        R = ecdsa.ellipticcurve.Point(curve, x, y, order)
        e = ecdsa.util.string_to_number(digest)
        # compute Q
        Q = ecdsa.numbertheory.inverse_mod(r, order) * (s * R + (-e % order) * G)
        # verify message
        if not ecdsa.VerifyingKey.from_public_point(Q, curve=ecdsa.SECP256k1).verify_digest(signature, digest,
                                                                                            sigdecode=ecdsa.util.sigdecode_string) :
            return None
        return ecdsa.VerifyingKey.from_public_point(Q, curve=ecdsa.SECP256k1)
        
    def _recovery_pubkey_param(self, digest, signature) :
        ''' Use to derive a number that will allow for the easy recovery
            of the public key from the signature
        '''
        for i in range(0,4) :
            p = self._recover_key(digest, signature, i)
            if (p.to_string() == self._vk.to_string()) :
                return i

    def _compress_pubkey(self) :
        ''' '''
        order = self._sk.curve.generator.order()
        p = self._vk.pubkey.point
        x_str = ecdsa.util.number_to_string(p.x(), order)
        hex_data = bytearray(chr(2 + (p.y() & 1)), 'utf-8')
        compressed = hexlify(hex_data + x_str).decode()
        return compressed

    def _is_canonical(self, sig):
        print("sig: " + str(sig))
        t1 = (sig[1] & 0x80) == 0
        t2 = not (sig[1] == 0 and ((sig[2] & 0x80) == 0))
        t3 = (sig[33] & 0x80) == 0
        t4 = not (sig[33] == 0 and ((sig[34] & 0x80) == 0))
        return t1 and t2 and t3 and t4

    def to_public(self) :
        ''' '''
        cmp = self._compress_pubkey()
        return 'EOS' + self._check_encode(cmp).decode()
        
    def to_wif(self) :
        ''' '''
        pri_key = '80' + hexlify(self._sk.to_string()).decode()
        return self._check_encode(pri_key, 'sha256x2').decode()

    def sign_string(self, data, encoding="utf-8"):
        ''' '''
        digest = sha256(bytearray(data, encoding))
        return self.sign(digest)

    def sign(self, digest) :
        ''' '''
        cnt = 0
        # convert digest to hex string
        digest = unhexlify(digest)
        if len(digest) != 32 :
            raise ValueError("32 byte buffer required")
        while 1 :
            # get deterministic k
            if cnt:
                sha_digest = hashlib.sha256(digest + bytearray(cnt)).digest()
            else :
                sha_digest = hashlib.sha256(digest).digest()
            k = ecdsa.rfc6979.generate_k( self._sk.curve.generator.order(),
                                          self._sk.privkey.secret_multiplier,
                                          hashlib.sha256,
                                        #   hashlib.sha256(digest + struct.pack('d', time.time())).digest() # use time to randomize
                                          sha_digest
                                          )
            # sign the message
            sigder = self._sk.sign_digest(digest, sigencode=ecdsa.util.sigencode_der, k=k)

            # reformat sig
            r, s = ecdsa.util.sigdecode_der(sigder, self._sk.curve.generator.order())
            sig = ecdsa.util.sigencode_string(r, s, self._sk.curve.generator.order())

            sigder = array.array('B', sigder)
            # ensure signature is canonical
            lenR = sigder[3]
            lenS = sigder[5 + lenR]
            
            if lenR == 32 and lenS == 32:
                # derive recover parameter
                i = self._recovery_pubkey_param(digest, sig)
                # compact
                i += 27
                # compressed
                i += 4
                sigstr = struct.pack('<B', i) + sig
                break
                # if self._is_canonical(sigstr):
                #     break    
            cnt +=1 
            if not cnt % 10 :
                print('Still searching for a signature. Tried {} times.'.format(cnt))        
        # encode
        return 'SIG_K1_' + self._check_encode(hexlify(sigstr), 'K1').decode()

    def verify(self, encoded_sig, digest) :
        ''' '''
        # remove SIG_ prefix
        encoded_sig = encoded_sig[4:]
        # remove curve prefix
        curvePre = encoded_sig[:3].strip('_')
        if curvePre != 'K1' :
            raise TypeError('Unsupported curve prefix {}'.format(curvePre))

        decoded_sig = self._check_decode(encoded_sig[3:], curvePre)
        # first 2 bytes are recover param
        # recover_param = hex_to_int(decoded_sig[:2]) - 4 - 27
        # use sig
        sig = decoded_sig[2:]
        # verify sig by recovering the key and comparing to self._vk
        # p = self._recover_key(unhexlify(digest), unhexlify(sig), recover_param)
        #return self._vk.verify_digest(unhexlify(sig), unhexlify(digest), sigdecode=ecdsa.util.sigdecode_string)
        # return p.to_string() == self._vk.to_string()
        try:
            self._vk.verify_digest(unhexlify(sig), unhexlify(digest), sigdecode=ecdsa.util.sigdecode_string)
        except ecdsa.keys.BadSignatureError:
            return False
        return True
        
