"""调用RSA库获取激活密钥。"""
import binascii
import os
import base64
import rsa
from rsa import DecryptionError, VerificationError


class Encrypt(object):
    def __init__(self):
        """密钥存在则读取密钥，不存在则生成密钥。"""
        # 生成密钥
        if not os.path.isfile("./private.pem"):
            public_key, private_key = rsa.newkeys(1024)
            # 保存密钥
            print("保存密钥。\n")
            with open("./public.pem", 'w') as public:
                public.write(public_key.save_pkcs1().decode())
            with open('./private.pem', 'w') as private:
                private.write(private_key.save_pkcs1().decode())

        # 导入密钥
        with open("./public.pem", 'r') as public:
            self.public_key = rsa.PublicKey.load_pkcs1(public.read().encode())
        with open('./private.pem', 'r') as private:
            self.private_key = rsa.PrivateKey.load_pkcs1(private.read().encode())

    def rsa_encrypt(self, text):
        """RSA加密。

        Args:
            text: 明文。

        Returns:
            返回密文。

        """
        crypto_text = rsa.encrypt(text.encode(), self.public_key)
        return crypto_text

    def rsa_decrypt(self, crypto_text):
        """RSA解密。

        Args:
            crypto_text: 密文。

        Returns:
            返回明文。

        """
        try:
            crypto_text = base64.b64decode(crypto_text)
        except binascii.Error:
            return -1
        try:
            text = rsa.decrypt(crypto_text, self.private_key).decode()
            return text
        except DecryptionError:
            return -1

    def rsa_sign(self, text):
        """RSA签名。

        Args:
            text: 明文。

        Returns:
            返回密文

        """
        crypto_text = rsa.sign(text.encode(), self.private_key, 'SHA-1')
        return crypto_text

    def rsa_verify(self, text, signature):
        """收到指令明文、签名，然后用公钥验证，进行身份确认。

        Args:
            text: 明文。
            signature: 签名。

        Returns:
            验证成功返回使用的hash类型名字符串；否则返回错误信息。

        """
        try:
            return rsa.verify(text.encode(), signature, self.public_key)
        except VerificationError as error:
            return str(error)


if __name__ == '__main__':
    encrypt = Encrypt()
    test_text = encrypt.rsa_encrypt("123456")
    print("Key:", base64.b64encode(test_text))
    print(encrypt.rsa_decrypt(test_text))
    # test_text = encrypt.rsa_sign("芜湖！")
    # print(encrypt.rsa_verify("芜湖！", test_text))
