import json
import boto3
from config import DESTINATION_BUCKET_NAME
import re
from notify_slack import post_message_to_slack


class S3ClientSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = boto3.client("s3")
        return cls._instance


def lambda_handler(event, context):
    s3_client = S3ClientSingleton()
    username, source_bucket, file_key = extract_info_from_event(event)
    if not file_type_validated(file_key) or not file_name_validated(file_key):
        slack_message = f"File {file_key} is not a valid invoice file."
        post_message_to_slack(slack_message)
        return {
            "statusCode": 200,
            "body": json.dumps("Lambda function execution completed."),
        }
    try:
        s3_client.copy_object(
            {"Bucket": source_bucket, "Key": file_key},
            DESTINATION_BUCKET_NAME,
            username + "/" + file_key,
        )
        print(f"File {file_key} copied to {DESTINATION_BUCKET_NAME} successfully.")
    except Exception as e:
        print(e)
        slack_message = f"Error processing file {file_key}: {str(e)}"
        post_message_to_slack(slack_message)

    return {
        "statusCode": 200,
        "body": json.dumps("Lambda function execution completed."),
    }


def extract_info_from_event(event):
    return (
        event["Records"][0]["userIdentity"]["principalId"],
        event["Records"][0]["s3"]["bucket"]["name"],
        event["Records"][0]["s3"]["object"]["key"],
    )


def file_type_validated(file_name: str):
    return file_name.endswith(".pdf")


def file_name_validated(file_name: str):
    return bool(re.match(r"^\d{6}$", file_name))
