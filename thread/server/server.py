#!/usr/bin/env python3

import socket
from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET
import hashlib
from Crypto.Cipher import AES
import ssl
import threading

MAX_CLIENT = 4

keyFile = "../priv.pem"  # Provide the full path to the private key file
certFile = "../cert.crt"  # Provide the full path to the certificate file

KEY = hashlib.sha256(b"senha").digest()  # Convert mnemonic string to a 32-bit encrypted object
IV = b"abcdefghijklmnop"  # Initialization vector should be 16 bytes
obj_enc = AES.new(KEY, AES.MODE_CFB, IV)  # Create an AES encryption object
#obj_dec = AES.new(KEY, AES.MODE_CFB, IV)  # Create an AES decryption object


def save_data_client(s, addr):
    obj_dec = AES.new(KEY, AES.MODE_CFB, IV)  # Create an AES decryption object
    while True:
        message_enc = s.recv(5*1024)
        if not message_enc:
            break
        dec_message = obj_dec.decrypt(message_enc)
        try:
            message =dec_message.decode('ascii')
        except UnicodeDecodeError:
            print("Error decoding received data.")
            print(dec_message)
            continue
        ip, port = addr
        time, cpu, mem = message.split("\n")
        cpu = ",".join(cpu.split())
        line = f"{time},{cpu},{mem}\n"
        name = ip.replace(".", "-")+"-"+str(port)
        with open(f"data/{name}.csv", "a") as f:
            f.write(line)
    s.close()


def main():
    host = "0.0.0.0"
    port = 5011

    s = socket.socket(AF_INET, SOCK_STREAM)
    s.bind((host, port))
    s.listen(MAX_CLIENT)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=certFile, keyfile=keyFile)
    s_ssl = context.wrap_socket(s, server_side=True)

    while True:
        try:
            c, addr = s_ssl.accept()

            print("Connected with:", addr)
            client_thread = threading.Thread(target=save_data_client, args=(c, addr))
            client_thread.daemon = True
            client_thread.start()
        except socket.error as e:
            print("Error:", e)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
