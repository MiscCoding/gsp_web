import hashlib


class EncryptEncoder:
    @staticmethod
    def sha256Encrypt(src):
        hash_object = hashlib.sha256(src.encode())
        result = hash_object.hexdigest()

        return result
