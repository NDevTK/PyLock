#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

# Function called on exit
def exitmsg(msg):
    print(msg)
    input_pylock('Press ENTER to exit the script')
    sys.exit()

# Create function for User Input
if sys.version_info < (3, 0, 0):
    def input_pylock(string):
        return raw_input(string)
else:
    def input_pylock(string):
        return input(string);

#Imports :D
import base64
import binascii
import os
import getpass
try:
    from cryptography.fernet import Fernet
except ImportError:
    exitmsg('The module cryptography is not installed please install it with pip.')
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

# Header
header = """PyLock beta v1.0.4 by NDev https://github.com/NDevTK/Python-Script-Locker/
DO NOT TRUST THIS SCRIPT TO BE SECURE!"""
print(header)

# Create salt
salt=binascii.hexlify(os.urandom(40))

# Scrypt Key derivation function
kdf = Scrypt(
    salt=salt,
    length=32,
    n=2 ** 14,
    r=8,
    p=1,
    backend=default_backend(),
    )

script_location = input_pylock('Script to use: ')
try:
    script_file = open(script_location)
except IOError:
    exitmsg('Unable to read file')
script = script_file.read()
script_file.close

# Get user input
print('Can be used to overwrite your script')
script_location = input_pylock('Save as: ')
password = getpass.getpass('Password to use: ').encode()

# Create key from password
key = Fernet(base64.urlsafe_b64encode(kdf.derive(password)));
del password; # Clean up

# New file template
new_file_contents = \
'''#!/usr/bin/env python

# Header
print("""%s""")

import sys

def exitmsg(msg):
    print(msg)
    input_pylock("Press ENTER to exit")
    sys.exit()

# Create function for User Input
if sys.version_info < (3, 0, 0):
    def input_pylock(string):
        return raw_input(string)
else:
    def input_pylock(string):
        return input(string);

#Inports
import getpass
import base64
try:
    from cryptography.fernet import Fernet
except ImportError:
    exitmsg("The module cryptography is not installed please install it with pip.")
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

# Get user input
password = getpass.getpass('Password: ').encode()

# Scrypt Key derivation function
kdf = Scrypt(salt=%s,length=32,n=2**14,r=8,p=1,backend=default_backend())

# Create key from password
key = Fernet(base64.urlsafe_b64encode(kdf.derive(password)));
del password; # Clean up

# Try to decrypt
try:
    script = key.decrypt(%s)
except Exception as ex:
    if(type(ex).__name__ == "InvalidToken"):
        exitmsg("Wrong password (-:") # :(
    print(ex)

# Exec code
del key # Clean up
exec(script); # Run script
del script # Clean up''' \
% (header, salt, key.encrypt(script.encode())) # Use template

try:
    new_file = open(script_location, 'w+')
    new_file.write(new_file_contents) # Write file contents
except IOError:
    exitmsg('Unable to write to file')

del key; # Clean up
new_file.close
exitmsg('Your file has been created') # DONE :D
