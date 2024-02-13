#!/bin/bash

echo "Enter Username:"
read USERNAME
echo "Enter SSH Public Key:"
read -s SSHPUBLICKEY
aws dynamodb put-item \
    --table-name SFTPUsers \
    --item "{
        \"Username\": {\"S\": \"$USERNAME\"},
        \"SSHPublicKey\": {\"S\": \"$SSHPUBLICKEY\"}
    }"

echo "Item added to database successfully."
