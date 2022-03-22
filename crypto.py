from Crypto import Random
from Crypto.Cipher import AES
import base64


class PKCS7Encoder():
    class InvalidBlockSizeError(Exception):
        pass

    def __init__(self, block_size=16):
        if block_size < 2 or block_size > 255:
            raise PKCS7Encoder.InvalidBlockSizeError('The block size must be '
                                                     'between 2 and 255, inclusive')
        self.block_size = block_size

    def encode(self, text):
        text_length = len(text)
        amount_to_pad = self.block_size - (text_length % self.block_size)
        if amount_to_pad == 0:
            amount_to_pad = self.block_size
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    def decode(self, text):
        pad = ord(text[-1])
        return text[:-pad]


def encrypt_val(clear_text):
    master_key = b'1234567890123456'
    encoder = PKCS7Encoder()
    raw = encoder.encode(clear_text)
    iv = Random.new().read(16)
    cipher = AES.new(master_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw.encode("utf-8"))).decode("utf-8")


print(encrypt_val(URL))
