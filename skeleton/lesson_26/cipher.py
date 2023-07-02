"""
Our implementation of an affine cipher and Atbash
"""
import string


class Cipher:
    num_alpha = {i: j for i, j in zip(range(1, 27), string.ascii_lowercase)}
    alpha_num = {i[1]: i[0] for i in num_alpha.items()}

    def encrypt(self, message: str):
        pass

    def decrypt(self, message: str):
        pass


class AtbashCipher(Cipher):
    # TODO: Implement the Atbash Cipher here with encrypt and decrypt methods
    pass


class AffineCipher(Cipher):
    # TODO: Implement the generalized affine cipher here with encrypt and decrypt methods
    pass



