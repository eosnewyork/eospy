from abc import ABC, abstractmethod

class Signer(ABC):
    def __init__(self, private_str=''):
        super().__init__()
    
    @abstractmethod
    def to_public(self):
        pass

    @abstractmethod
    def to_wif(self):
        pass

    @abstractmethod
    def sign(self, digest):
        pass
    
    @abstractmethod
    def verify(self, encoded_sig, digest):
        pass