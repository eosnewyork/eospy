import sys

sys.path.append('../eospy')

from eospy.cleos import EOSKey
import hashlib


class TestSig:
    payload = "some important data"
    digest = hashlib.sha256(payload.encode('utf-8').rstrip()).hexdigest()

    legacy = ("EOS6JWAwA6goJmmAGwQEwbFne8zNxhuVTjgk1aLqVW9efHWhGfvwU",
              "5JU8RktQ72qFtJyiW3DJ54B2ZY6Ad83HdoGg78Nk8kUNMJEmCUg")

    r1 = ("PUB_R1_65vcmkCEJuxQ2rvYxBZSiUGP9FJPaqMfrLyakHduxEULWcBUxW",
          "PVT_R1_2sTZXHRWPfgWfn4gTD4bXjVsKRTSYBCekebBgJq1P9SW7ckoXk")

    k1 = ("PUB_K1_6ctHgq55Tt4u3ksvDw1jadhC5tytemHs8fHM4YfFVqMe4F8XWU",
          "PVT_K1_r9seSVdS9yTRmSXtLrpELLZ5dhbEqr12jLCRg5NJAWr5q8U9o")

    def test_legacy(self):
        key = EOSKey(self.legacy[1])
        sig = key.sign(self.digest)
        assert key.verify(sig, self.digest)

    def test_r1(self):
        key = EOSKey(self.r1[1])
        sig = key.sign(self.digest)
        assert key.verify(sig, self.digest)

    def test_k1(self):
        key = EOSKey(self.k1[1])
        sig = key.sign(self.digest)
        assert key.verify(sig, self.digest)
