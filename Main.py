#!/usr/bin/env python
import base64
import sys
import os
import getpass
try:
    from cryptography.fernet import Fernet
except ImportError:
    sys.exit("cryptography not installed install it with pip install cryptography via cmd or powershell (On Windows)")
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
encoding = "UTF-8"
print("PyLock beta v1.0.0 by ***REMOVED*** https://***REMOVED***/PyLock")
pwd = getpass.getpass("Password to use: ")
salt = os.urandom(16)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
bytes_pwd = bytes(pwd, encoding)
del pwd
key = base64.urlsafe_b64encode(kdf.derive(bytes_pwd))
del bytes_pwd
Auth = Fernet(key)
del key
loc = input("Script to use: ")
print("Can be used to overwrite your script")
sloc = input("Save as: ")
fscript = open(loc)
script = fscript.read()
fscript.close
del fscript
nc = '''#!/usr/bin/env python
#Made using PyLock by ***REMOVED*** https://***REMOVED***/PyLock
import getpass
import base64
import sys
try:
    from cryptography.fernet import Fernet
except ImportError:
    sys.exit("Error cryptography not installed install it with pip install cryptography via cmd or powershell (On Windows)")
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
pwd = bytes(getpass.getpass("Password: "), "%s")
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=%s,
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(pwd))
del pwd
Auth = Fernet(key)
del key
try:
    exec(Auth.decrypt(b"%s").decode("%s"))
except Exception as ex:
    if(type(ex).__name__ == "InvalidToken"):
        sys.exit("Wrong password (-:")
    print(ex)
del kdf
del sys
del Auth''' % (encoding, salt, Auth.encrypt(bytes(script, encoding)).decode(encoding), encoding)
del encoding
del script
del Auth
del salt
f = open(sloc,"w+")
f.write(nc)
f.close
del f
del nc
