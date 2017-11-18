###salting password, salt per user
import random
import base64
import struct
import hashlib
def generate_salt():
    '''generate random string as salt '''
    rand_f=random.SystemRandom().random()
    mysalt=base64.b64encode(struct.pack("!d" , rand_f))
    return mysalt


def salted_password(salt, password):
    
    cat=salt + password.encode('ascii')
    return hashlib.sha256(cat).hexdigest()

