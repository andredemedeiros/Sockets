#!/usr/bin/env python3

import socket
import hashlib
from Crypto.Cipher import AES
import ssl

KEY = hashlib.sha256(b"senha").digest()  # Convert mnemonic string to a 32-bit encrypted object
IV = b"abcdefghijklmnop"  # Initialization vector should be 16 bytes
obj_enc = AES.new(KEY, AES.MODE_CFB, IV)  # Create an AES encryption object
obj_dec = AES.new(KEY, AES.MODE_CFB, IV)  # Create an AES decryption object

def main():
    host = input("What is the server ip?")  # Replace with the server's IP address
    port = 5011

    # Create an SSL context
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE  # No client-side cert validation for simplicity

    # Create a socket and wrap it with SSL
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = context.wrap_socket(s, server_hostname=host)

    ssl_sock.connect((host, port))

    message = input("-> ")
    while message != 'q':
        message_enc = obj_enc.encrypt(message.encode('utf-8'))
        ssl_sock.send(message_enc)  # Use send() for SSL-wrapped sockets
        data = ssl_sock.recv(1024)
        try:
            print("Received data:", data.decode('utf-8'))
        except UnicodeDecodeError:
            print("Error decoding received data.")
        decrypted = obj_dec.decrypt(data)
        print("Received from server:", decrypted.decode('utf-8'))
        message = input("-> ")

    ssl_sock.close()

if __name__ == "__main__":
    main()
