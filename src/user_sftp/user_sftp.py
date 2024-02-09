import argparse
from config import PUBLIC_SFTP_SERVER_ID, ADMIN_PUBLIC_KEY, SOURCE_BUCKET_NAME
import boto3


class TransferClientSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = boto3.client("transfer")
        return cls._instance


def create_user(username, role_arn):
    transfer_client = TransferClientSingleton()
    try:
        response = transfer_client.create_user(
            ServerId=PUBLIC_SFTP_SERVER_ID,
            UserName=username,
            SshPublicKeyBody=ADMIN_PUBLIC_KEY,
            Role=role_arn,
            HomeDirectory="/" + SOURCE_BUCKET_NAME,
        )
        print(f"User {username} created successfully.")
        return response
    except Exception as e:
        print(f"Error creating user {username}: {str(e)}")
        return None


def delete_user(username):
    transfer_client = TransferClientSingleton()
    try:
        response = transfer_client.delete_user(
            ServerId=PUBLIC_SFTP_SERVER_ID, UserName=username
        )
        print(f"User {username} deleted successfully.")
        return response
    except Exception as e:
        print(f"Error deleting user {username}: {str(e)}")
        return None


def list_users():
    transfer_client = TransferClientSingleton()
    """
    List all users for the sftp server.
    :return: List of users.
    """
    try:
        response = transfer_client.list_users(ServerId=PUBLIC_SFTP_SERVER_ID)
        users = response["Users"]
        for user in users:
            print(f"- {user['UserName']}")
        return users
    except Exception as e:
        print(f"Error listing users: {str(e)}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Manage AWS SFTP Users")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    create_parser = subparsers.add_parser("create", help="Create a new user")
    create_parser.add_argument("username", help="Username for the new user")
    create_parser.add_argument("role_arn", help="ARN of the IAM role for the user")

    delete_parser = subparsers.add_parser("delete", help="Delete a user")
    delete_parser.add_argument("username", help="Username of the user to delete")

    list_parser = subparsers.add_parser("list", help="List all users")

    args = parser.parse_args()

    if args.command == "create":
        create_user(
            args.username,
            args.role_arn,
        )
    elif args.command == "delete":
        delete_user(args.username)
    elif args.command == "list":
        list_users()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
