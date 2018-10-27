#!/usr/bin/env bash

# Setup your own PKI
#
# Usage: ./gencerts.sh
#
# Generates the following certificate files
#
# root_ca.csr – The root ca certificate sign request, which doesn’t make sense for the root ca, and therefore will never be used. As the root CA is self signed.
# root_ca.pem – The Root CA certificate. This is the file you distribute as much as possible.
# root_ca.key – This is the root CA Key. Keep this file safe and secured, as if your life depends on it. For a public Root CA this is actually truth.
#
# intermediate_ca.csr – The Intermediate CA certificate sign request.
# intermediate_ca.pem – The Intermediate CA certificate, signed by the Root CA. Make sure you distribute this file.
# intermediate_ca.key – This is the Intermediate CA Key. Keep this file safe and secured.
#
# server.key – The all important server private key
# server.pem – The server certificate
#
# client.key – The all important client private key
# client.pem – The client certificate
#

set -e

rm -f certs/*.pem
rm -f certs/*.csr

mkdir -p certs

# create the root CA
cfssl gencert -initca config/ca_root.json | cfssljson -bare certs/root_ca

# create the intermediate CA
cfssl gencert -initca config/intermediate_ca.json | cfssljson -bare certs/intermediate_ca

# sign the intermediate ca with the root ca
cfssl sign -ca certs/root_ca.pem -ca-key certs/root_ca-key.pem -config config/root_to_intermediate_ca.json certs/intermediate_ca.csr | cfssljson -bare certs/intermediate_ca

# generate end device certificates
cfssl gencert -ca certs/intermediate_ca.pem -ca-key certs/intermediate_ca-key.pem -config config/intermediate_to_client_cert.json config/csr_end_device.json | cfssljson -bare certs/server
cfssl gencert -ca certs/intermediate_ca.pem -ca-key certs/intermediate_ca-key.pem -config config/intermediate_to_client_cert.json config/csr_end_device.json | cfssljson -bare certs/client
