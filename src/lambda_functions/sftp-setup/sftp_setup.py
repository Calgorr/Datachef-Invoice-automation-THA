import boto3
import json
from config.sftp_config import *


class TransferClientSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = boto3.client("transfer")
        return cls._instance


class DynamoDBClientSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = boto3.client("dynamodb")
        return cls._instance


transfer = TransferClientSingleton()
dynamodb = DynamoDBClientSingleton()


def create_sftp_server():
    try:
        response = transfer.create_server(
            Protocols=["SFTP"],
            Tags=[{"Key": "owner", "Value": OWNER_EMAIL_ADDRESS}],
            IdentityProviderType="SERVICE_MANAGED",
        )
        return response["ServerId"]
    except Exception as e:
        print(f"Error creating SFTP server: {e}")
        raise e


def store_server_in_dynamodb(server_id):
    try:
        dynamodb.put_item(
            TableName=SERVERS_DYNAMODB_TABLE_NAME,
            Item={
                "serverId": {"S": server_id},
                "status": {"S": "online"},
            },
        )
    except Exception as e:
        print(f"Error storing SFTP server info in DynamoDB: {e}")
        raise e


def create_sftp_user(server_id):
    try:
        transfer.create_user(
            ServerId=server_id,
            UserName="admin-sftp",
            Role=ADMIN_IAM_ROLE_ARN,
            SshPublicKeyBody=SSH_PUBLIC_KEY,
            HomeDirectory=ADMIN_HOME_DIRECTORY,
        )
    except Exception as e:
        print(f"Error creating SFTP user: {e}")
        raise e


def get_users_from_dynamodb():
    try:
        return dynamodb.scan(TableName=USERS_DYNAMODB_TABLE_NAME).get("Items", [])
    except Exception as e:
        print(f"Error scanning DynamoDB table: {e}")
        raise e


def create_sftp_users(users, server_id):
    for user in users:
        username = user["Username"]["S"]
        ssh_public_key = user["SSHPublicKey"]["S"]
        try:
            transfer.create_user(
                ServerId=server_id,
                UserName=username,
                Role=EMPLOYEE_IAM_ROLE_ARN,
                SshPublicKeyBody=ssh_public_key,
                HomeDirectory=EMPLOYEE_HOME_DIRECTORY,
            )
            print(f"SFTP user {username} created successfully.")
        except Exception as e:
            print(f"Error creating SFTP user {username}: {e}")
            continue


def lambda_handler(event, context):
    server_id = create_sftp_server()
    store_server_in_dynamodb(server_id)
    create_sftp_user(server_id)
    users = get_users_from_dynamodb()
    create_sftp_users(users, server_id)

    return {
        "statusCode": 200,
        "body": json.dumps("SFTP Server and users created successfully!"),
    }
