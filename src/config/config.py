import os

from dotenv import load_dotenv

load_dotenv()

DESTINATION_BUCKET_NAME = os.getenv("destination_bucket_name")
SOURCE_BUCKET_NAME = os.getenv("source_bucket_name")
SLACK_WEBHOOK_URL = os.getenv("slack_webhook_url")
ADMIN_PUBLIC_KEY = os.getenv("admin_public_key")
PUBLIC_SFTP_SERVER_ID = os.getenv("public_sftp_server_id")
