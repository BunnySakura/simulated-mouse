"""调用RSA库验证密钥。"""
import binascii
import base64
import rsa
from rsa import DecryptionError


class Encrypt(object):
    def __init__(self):
        """密钥存在则读取密钥，不存在则生成密钥。"""
        _private_key = """
-----BEGIN RSA PRIVATE KEY-----
test
-----END RSA PRIVATE KEY-----
"""
        self.private_key = rsa.PrivateKey.load_pkcs1(_private_key.encode())  # 私钥

    def rsa_decrypt(self, crypto_text) -> str:
        """RSA解密。

        Args:
            crypto_text: 密文。

        Returns:
            解密成功则返回明文；否则返回错误信息。

        """
        try:
            crypto_text = base64.b64decode(crypto_text)
        except binascii.Error as error:
            return str(error)
        try:
            text = rsa.decrypt(crypto_text, self.private_key).decode()
            return text
        except DecryptionError as error:
            return str(error)

    def rsa_sign(self, text):
        """RSA签名。

        Args:
            text: 明文。

        Returns:
            返回密文。

        """
        crypto_text = rsa.sign(text.encode(), self.private_key, 'SHA-1')
        return crypto_text


if __name__ == '__main__':
    encrypt = Encrypt()
    test_text = encrypt.rsa_sign("芜湖！")
