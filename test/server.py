#!/usr/bin/env python3

import socket
from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET
import hashlib
from Crypto.Cipher import AES
import ssl

keyFile = "priv.pem"  # Provide the full path to the private key file
certFile = "cert.crt"  # Provide the full path to the certificate file

KEY = hashlib.sha256(b"senha").digest()  # Convert mnemonic string to a 32-bit encrypted object
IV = b"abcdefghijklmnop"  # Initialization vector should be 16 bytes
obj_enc = AES.new(KEY, AES.MODE_CFB, IV)  # Create an AES encryption object
obj_dec = AES.new(KEY, AES.MODE_CFB, IV)  # Create an AES decryption object

def echo_client(s):
    while True:
        message_enc = s.recv(1024)
        if not message_enc:
            break
        try:
            message = obj_dec.decrypt(message_enc).decode('utf-8')
        except UnicodeDecodeError:
            print("Error decoding received data.")
            continue
        print("Received from connection:", message)
        data = message.upper()  # Convert the received string to uppercase
        encrypted = obj_enc.encrypt(data.encode('utf-8'))
        s.send(encrypted)
    s.close()

def main():
    host = "0.0.0.0"
    port = 5011

    s = socket.socket(AF_INET, SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=certFile, keyfile=keyFile)
    s_ssl = context.wrap_socket(s, server_side=True)
    
    while True:
        try:
            c, addr = s_ssl.accept()
            print("Connected with:", addr)
            echo_client(c)
        except socket.error as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
