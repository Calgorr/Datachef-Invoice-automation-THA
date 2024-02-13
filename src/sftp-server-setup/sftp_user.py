import boto3
import sys

dynamodb = boto3.client("dynamodb")
transfer = boto3.client("transfer")
dynamodb_table_name = "SFTPUsers"
sftp_server_id = sys.argv[1]


def get_users_from_dynamodb():
    try:
        return dynamodb.scan(TableName=dynamodb_table_name).get("Items", [])
    except Exception as e:
        print(f"Error scanning DynamoDB table: {e}")
        return []


def create_sftp_users(users):
    for user in users:
        username = user["Username"]["S"]
        ssh_public_key = user["SSHPublicKey"]["S"]

        try:
            transfer.create_user(
                ServerId=sftp_server_id,
                UserName=username,
                Role="arn:aws:iam::212435474521:role/sftp-employee-s3-management-role",
                SshPublicKeyBody=ssh_public_key,
                HomeDirectory="/dc-tha5-source-bucket",
            )
            print(f"employee {username} created successfully.")
        except Exception as e:
            print(f"Error creating employee {username}: {e}")


def main():
    users = get_users_from_dynamodb()
    create_sftp_users(users)


if __name__ == "__main__":
    main()
