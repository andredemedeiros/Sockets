#!/bin/sh

# Generate a private key
openssl genrsa -aes256 -out priv.pem 4096

# Display the private key
cat priv.pem

# Display the private key details
openssl rsa -text -in priv.pem

# Generate the public key
openssl rsa -in priv.pem -pubout -out pub.pem

# Generate a Certificate Signing Request (CSR)
openssl req -new -key priv.pem -out cert.csr

# Display the CSR details
openssl req -text -in cert.csr -noout

# Self-sign the CSR to create the certificate
openssl x509 -req -days 365 -in cert.csr -signkey priv.pem -out cert.crt
