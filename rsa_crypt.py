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
MIICYgIBAAKBgQCX2QEc7aFKIhnsVeSSJhwnc9sR+6jKBvF6m3X5B9BgvJQdjVns
Z3Ep3W/2P48ui1CpvJPVQc5uagVAJ/LHFf+UEhjHqDjpsM0hYhZ7OsCvPB8O7huC
Gd6+RWv4ozOP2B8X68y0FD9jUMp/IKixpX6hHRMbFhxT+l2nkzA+5tlA8wIDAQAB
AoGBAIARjDjDyublgAuuHcuNzO0Rb9Do+eD6niwUdhmFF6CfLCUIlLEoRW9TzhxY
WwCci3m9DMouaFcDoE4N4qy3/KqoYbXCBkEJTGJ/qAVDeCoZ4vv7Yv89Uc8ltiti
bD2s+6aNrMFn/1UN+MmeyIPuQdG77/MQX0hkE3+W6sW3uJyRAkUAzuj5WciMHLeT
/zHfIeGd4rDbU1yOIvO/LXNH/r5ealA5axUf0ioRGeHpEptJj5zi+Oe+28vyJEF7
d9EneouwzZwyHq0CPQC737mfVCyaGtyDyPZ35NgCVpgwe6tgSZl/Zl2P0EmH4d6r
u7e++w7wLf9Le9qHCYWO6gV1CSlHMevo8h8CRQCc10DcbAa5ZfbLhPRM7IcP5Vv7
zrb3i6ipPS+fzJIpKHK91x9t4fFgmzxfnFKgiB4M6y5j0i7UiMacxnCUlfsJgJMF
aQI9AIDpdav/DQ+9CLygo4YHD7UjCBCUezZ5qgrCCccJi7riYHEEQIOaL1jcpwV7
eaoY/Xzf1VjGLX29ontXzwJEMYMsxyNapePGcWt30WL+qjeow22lvnOGkXBX2MM8
VA3lyk2nGgE0G4MJKYe3Ncr994mY6qXqzne0aIySs6zbxbKOPa0=
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
