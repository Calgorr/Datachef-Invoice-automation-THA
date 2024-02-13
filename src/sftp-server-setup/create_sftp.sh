#!/bin/bash
server_id=$(aws transfer create-server --protocols "SFTP" --identity-provider-type SERVICE_MANAGED --query "ServerId" --output text)
echo "Enter the SSH public key:"
read -s SSH_PUBLIC_KEY
IAM_ROLE_ARN="arn:aws:iam::212435474521:role/sftp-admin-role"
HOME_DIRECTORY="/dc-tha5-destination-bucket"
aws transfer create-user \
    --server-id $server_id \
    --user-name admin-sftp \
    --role $IAM_ROLE_ARN \
    --ssh-public-key-body "$SSH_PUBLIC_KEY" \
    --home-directory $HOME_DIRECTORY

python ./sftp_user.py $server_id
