import bcrypt
from django.contrib.auth.hashers import BasePasswordHasher

class BCryptPasswordHasher(BasePasswordHasher):
    algorithm = 'bcrypt'

    def encode(self, password, salt):
        if not password:
            return password
        salt = bcrypt.gensalt()
        password = password.encode('utf-8')
        return "{0}${1}".format(self.algorithm, bcrypt.hashpw(password, salt).decode('utf-8'))

    def verify(self, password, encoded):
        return bcrypt.checkpw(password.encode('utf-8'), "$".join(encoded.split("$")[1:]).encode('utf-8'))

    def safe_summary(self, encoded):
        return {'algorithm': self.algorithm}
