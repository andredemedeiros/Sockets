#!/usr/bin/env python3

import socket
import hashlib
from Crypto.Cipher import AES
import ssl
from time import time_ns, sleep, asctime

from data import get_mem_per, get_cpu_per

KEY = hashlib.sha256(b"senha").digest()  # Convert mnemonic string to a 32-bit encrypted object
IV = b"abcdefghijklmnop"  # Initialization vector should be 16 bytes
obj_enc = AES.new(KEY, AES.MODE_CFB, IV)  # Create an AES encryption object
obj_dec = AES.new(KEY, AES.MODE_CFB, IV)  # Create an AES decryption object

def client_socket():
    host = input("What is the ip server?")  # Replace with the server's IP address
    port = 5011

    # Create an SSL context
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE  # No client-side cert validation for simplicity

    # Create a socket and wrap it with SSL
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = context.wrap_socket(s, server_hostname=host)

    ssl_sock.connect((host, port))
    i = 0
    while i < 300:
        cpu = " ".join(str(i) for i in get_cpu_per())
        time = asctime()
        message = f"{time}\n{cpu}\n{get_mem_per()}"
        message_enc = obj_enc.encrypt(message.encode('ascii'))
        ssl_sock.send(message_enc)  # Use send() for SSL-wrapped sockets
        sleep(2)
        i += 1
    ssl_sock.close()


client_socket()
