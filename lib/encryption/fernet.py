import os
from cryptography.fernet import Fernet

import config.filepaths as paths
key_path = paths.fernet128_keys + 'secret.key'


class FernetCipher():

    def __init__(self, path=key_path):
        self.enc_dict = {}
        self.key_path = path
        self._check_path(self.key_path)
        try:
            self.key = self.load_key()
        except:
            self.generate_key()
            self.key = self.load_key()

        self.f = Fernet(self.key)

    def generate_key(self):
        _key = Fernet.generate_key()
        with open(self.key_path, 'wb') as key_file:
            key_file.write(_key)

    def load_key(self):
        return open(self.key_path, 'rb').read()

    def write_key(self, key):
        with open(self.key_path, 'wb') as key_file:
            key_file.write(key)

    def load_key_for_xport(self):
        return open(self.key_path, 'rb').read().decode()

    def encrypt(self, msg):
        msg = msg.encode()  # byte encode
        enc_msg = self.f.encrypt(msg)
        return enc_msg

    def decrypt(self, data: bytes):
        data = data["cipher_text"].encode()
        try:
            dec_msg = self.f.decrypt(data)
        except Exception as e:
            dec_msg = data
        return dec_msg

    def split(self, raw_msg):
        """Separates message from raw_msg from server.

        Returns:
            handle: (str) user name
            cipher_msg: (bytes)
        """

        SEPARATOR = ': '
        _msg = raw_msg.decode()  # to str
        _split = _msg.split(SEPARATOR)
        handle = _split[0]
        cipher_msg = _split[1].encode()  # to bytes
        return handle, cipher_msg

    def _check_path(self, path):
        folders = os.path.dirname(path)
        if not os.path.exists(folders):
            os.makedirs(folders)
