Developer Guide
===============

System Architecture
-------------------

The system integrates AWS Transfer Family's SFTP service with AWS S3, using Lambda functions and DynamoDB for automation and data management. When a file is uploaded to an S3 source bucket, a Lambda function named (s3-bucket-invoice-copy) is triggered to move the file to a designated destination bucket. DynamoDB holds employee data, which is utilized to dynamically create SFTP users on the 28th of each month. This setup is orchestrated with an event scheduler that ensures timely execution of the Lambda function named (sftp-server-setup) for user creation.

Proposed Improvements
---------------------

1.  **SFTP Server ID Storage**: Store the SFTP server ID in a DynamoDB table for precise policy Resource Defining, avoiding the use of `Resource = *`(least privilege principle).
2.  **Scheduled SFTP Server Management**: Implement a system to fetch the last SFTP server ID and schedule server deletion for the first day of each month, allowing a maximum lifespan of 2 days post-creation if not manually terminated by the admin.
3.  **Lambda Function for User Addition**: Create a Lambda function to automatically add users stored in the DynamoDB table to the SFTP server upon its activation, using the server ID from the database.
4.  **Lambda Function to delete the sftp server based on the number of uploads**: after each upload in a month a counter is incremented by one after the counter reaches the number of employee's existing in the SFTPUsers table the sftp server is deleted

### Additional Suggestion

*   **Monitoring and Alerts**: Implement CloudWatch to monitor system activities and trigger alerts for any anomalies or system failures, ensuring timely response to issues.

This guide aims to offer a foundational understanding of the system's workings and areas for potential enhancements to ensure its scalability, security, and efficiency.