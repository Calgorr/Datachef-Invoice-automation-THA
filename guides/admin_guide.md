# Admin Guide

## Configure AWS CLI

1. Install the AWS CLI following the official AWS documentation.
2. Configure it using `aws configure`, entering your AWS Access Key, Secret Key, region (`eu-west-1`), and output format (e.g., `json`).

## User Management Commands

Ensure all user management tasks are completed before the scheduled cron job: `0 22 28 * ? *`.

### Creating a User in DynamoDB

- To add a user, use the command:
  ```bash
  aws dynamodb put-item --table-name SFTPUsers --item '{"username": {"S": "employee_username"}, "publicKey": {"S": "employee_public_key"}}'
### Listing a User
- To list users, execute:
  ```bash
  aws dynamodb scan --table-name SFTPUsers
### Deleting a User
- To delete a user:
  ```bash
  aws dynamodb delete-item --table-name SFTPUsers --key '{"username": {"S": "employee_username"}}'
### Access Invoices and S3 Bucket Administration
- Admins can access both S3 buckets(with administrative permissions) using an SFTP client with the admin username and private key. For configuration details, refer to the User Guide.
