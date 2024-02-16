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


def delete_sftp_server(server_id):
    try:
        transfer.delete_server(ServerId=server_id)
        print(f"SFTP Server {server_id} deleted successfully.")
        return True
    except Exception as e:
        print(f"Error deleting SFTP server {server_id}: {e}")
        return False


def update_server_status_in_dynamodb(server_id):
    try:
        dynamodb.update_item(
            TableName=SERVERS_DYNAMODB_TABLE_NAME,
            Key={"serverId": {"S": server_id}},
            UpdateExpression="SET Status = :val",
            ExpressionAttributeValues={":val": {"S": "deleted"}},
        )
        print(f"SFTP Server {server_id} status updated to deleted in DynamoDB.")
    except Exception as e:
        print(f"Error updating SFTP server status in DynamoDB: {e}")
        raise e


def lambda_handler(event, context):
    try:
        response = dynamodb.scan(
            TableName=SERVERS_DYNAMODB_TABLE_NAME,
            FilterExpression="status = :status",
            ExpressionAttributeValues={":status": {"S": "online"}},
        )
        servers = response.get("Items", [])

        for server in servers:
            server_id = server["serverId"]["S"]
            if delete_sftp_server(server_id):
                update_server_status_in_dynamodb(server_id, "deleted")

        return {
            "statusCode": 200,
            "body": json.dumps("Online SFTP Servers deleted successfully!"),
        }
    except Exception as e:
        print(f"Error in Lambda execution: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps("Error processing request."),
        }
