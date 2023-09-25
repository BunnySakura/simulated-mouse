import binascii
import base64
from typing import Optional

import rsa
import os


class RsaEncrypt:
    def __init__(self):
        """初始化Encrypt对象，生成或导入RSA密钥对"""
        self.public_key, self.private_key = self.load_or_generate_keys()

    @staticmethod
    def load_or_generate_keys():
        """加载或生成RSA密钥对。

        Returns:
            返回公钥和私钥。
        """
        if not os.path.isfile("./public.pem") or not os.path.isfile("./private.pem"):
            public_key, private_key = rsa.newkeys(1024)
            with open("./public.pem", 'w') as public:
                public.write(public_key.save_pkcs1().decode())
            with open('./private.pem', 'w') as private:
                private.write(private_key.save_pkcs1().decode())
        else:
            with open("./public.pem", 'r') as public:
                public_key = rsa.PublicKey.load_pkcs1(public.read().encode())
            with open('./private.pem', 'r') as private:
                private_key = rsa.PrivateKey.load_pkcs1(private.read().encode())
        return public_key, private_key

    def rsa_encrypt(self, plain_text):
        """使用RSA加密明文

        Args:
            plain_text: 明文

        Returns:
            返回密文
        """
        return rsa.encrypt(plain_text.encode(), self.public_key)

    def rsa_decrypt(self, crypto_text) -> Optional[str]:
        """使用RSA解密密文

        Args:
            crypto_text: 密文

        Returns:
            返回明文
        """
        try:
            return rsa.decrypt(base64.b64decode(crypto_text), self.private_key).decode()
        except binascii.Error:
            return None
        except rsa.DecryptionError:
            return None

    def rsa_sign(self, text: str, hash_method: str = 'SHA-1'):
        """
        使用RSA对文本进行签名
        Args:
            text: 明文
            hash_method: 哈希方法

        Returns:
            返回签名结果
        """
        return rsa.sign(text.encode(), self.private_key, hash_method)

    def rsa_verify(self, text, signature) -> str:
        """使用公钥验证签名

        Args:
            text: 明文
            signature: 签名

        Returns:
            验证成功返回使用的hash类型名字符串；否则返回错误信息
        """
        try:
            return rsa.verify(text.encode(), signature, self.public_key)
        except rsa.VerificationError as e:
            return str(e)


if __name__ == '__main__':
    encrypt = RsaEncrypt()
    test_text = encrypt.rsa_encrypt("e94370c0-c694-5e7c-aee9-ff894cfaf63b")
    print("Key:", base64.b64encode(test_text))
    print(encrypt.rsa_decrypt(base64.b64encode(test_text)))
    print(encrypt.rsa_verify("芜湖！", encrypt.rsa_sign("芜湖！")))
    with open("./key", "wb") as key:
        key.write(base64.b64encode(test_text))
