#!/bin/bash
echo "Enter Username to delete:"
read USERNAME
aws dynamodb delete-item \
    --table-name SFTPUsers \
    --key "{
        \"Username\": {\"S\": \"$USERNAME\"}
    }"

echo "Item with Username $USERNAME deleted from database successfully."
