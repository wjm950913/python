import jwt
import time
from django.conf import settings


def make_token(username, exp=3600 * 24):
    now = time.time()
    payload = {'uname': username, 'exp': now + exp}
    return jwt.encode(payload, settings.JWT_TOKEN_KEY, algorithm='HS256')


# print(make_token('tom'))
def de_token(token):
    uname = jwt.decode(token, settings.JWT_TOKEN_KEY, algorithm='HS256')
    return uname
