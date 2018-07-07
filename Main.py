#!/usr/bin/env python
import sys
def exitmsg(msg):
    print(msg)
    input("Press ENTER to exit the script")
    sys.exit()
if sys.version_info<(3,0,0):
    def input(string):
         return raw_input(string)
import base64
import binascii
import os
import getpass
try:
    from cryptography.fernet import Fernet
except ImportError:
    exitmsg("The module cryptography is not installed please install it with pip install cryptography via the command line")
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
print("PyLock beta v1.0.3 by ***REMOVED*** https://github.com/NDevTK/Python-Script-Locker")
kdf = Scrypt(salt=binascii.hexlify(os.urandom(40)),length=32,n=2**14,r=8,p=1,backend=default_backend())
loc = input("Script to use: ")
try:
    fscript = open(loc)
except IOError:
    exitmsg("Unable to read file")
script = fscript.read()
fscript.close
print("Can be used to overwrite your script")
sloc = input("Save as: ")
nc = '''#!/usr/bin/env python
#Made using PyLock by ***REMOVED*** https://github.com/NDevTK/Python-Script-Locker
import sys
def exitmsg(msg):
    print(msg)
    input("Press ENTER to exit")
    sys.exit()
if sys.version_info<(3,0,0):
    def input(string):
         return raw_input(string)
import getpass
import base64
try:
    from cryptography.fernet import Fernet
except ImportError:
    exitmsg("The module cryptography is not installed please install it with pip install cryptography via the command line")
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
kdf = Scrypt(salt=%s,length=32,n=2**14,r=8,p=1,backend=default_backend())
try:
    exec(Fernet(base64.urlsafe_b64encode(kdf.derive(getpass.getpass("Password to use: ").encode()))).decrypt(%s))
except Exception as ex:
    if(type(ex).__name__ == "InvalidToken"):
        exitmsg("Wrong password (-:")
    print(ex)''' % (salt, Fernet(base64.urlsafe_b64encode(kdf.derive(getpass.getpass("Password to use: ").encode()))).encrypt(script.encode()))
try:
    f = open(sloc,"w+")
    f.write(nc)
except IOError:
    exitmsg("Unable to write to file")
f.close
exitmsg("Your file has been created")
