import os

SSH_PUBLIC_KEY = os.environ["ssh_public_key"]
ADMIN_IAM_ROLE_ARN = os.environ["admin_iam_role_arn"]
EMPLOYEE_IAM_ROLE_ARN = os.environ["employee_iam_role_arn"]
ADMIN_HOME_DIRECTORY = os.environ["admin_home_directory"]
EMPLOYEE_HOME_DIRECTORY = os.environ["employee_home_directory"]
USERS_DYNAMODB_TABLE_NAME = os.environ["users_dynamodb_table_name"]
SERVERS_DYNAMODB_TABLE_NAME = os.environ["servers_dynamodb_table_name"]
OWNER_EMAIL_ADDRESS = os.environ["owner_email_address"]
