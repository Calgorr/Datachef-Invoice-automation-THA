Developer Guide
===============

System Architecture
-------------------

The system integrates AWS Transfer Family's SFTP service with AWS S3, using Lambda functions and DynamoDB for automation and data management. When a file is uploaded to an S3 source bucket, a Lambda function named (s3-bucket-invoice-copy) is triggered to move the file to a designated destination bucket. DynamoDB holds employee data, which is utilized to dynamically create SFTP users on the 28th of each month. This setup is orchestrated with an event scheduler that ensures timely execution of the Lambda function named (sftp-server-setup) for user creation.
### System Architecture - Choice of AWS Services Explained

**AWS Transfer Family's SFTP Service:** Chosen for its fully managed support for Secure File Transfer Protocol (SFTP), enabling secure file exchanges with external partners. This service is directly integrated with AWS S3, eliminating the need for managing underlying infrastructure while ensuring compliance and security standards.

**AWS S3 (Simple Storage Service):** Selected for its highly durable and scalable object storage, S3 serves as the backbone for storing files transferred via SFTP. It provides cost-effective storage and is seamlessly integrated with other AWS services, making it ideal for the source and destination buckets in this architecture.

**AWS Lambda:** Lambda functions are utilized for their serverless execution model, which allows for running code in response to triggers (such as S3 events or schedules) without provisioning or managing servers. This choice supports automation, such as moving files between buckets and creating SFTP users, aligning with the system's need for scalability and operational efficiency.

**Amazon DynamoDB:** A fully managed NoSQL database service chosen for its low latency and scalability. DynamoDB stores employee data, enabling dynamic creation of SFTP users without the operational burden of traditional database management. Its integration with Lambda allows for seamless automation within the AWS ecosystem.

**AWS EventBridge (formerly CloudWatch Events):** Utilized for scheduling tasks, such as the monthly execution of the Lambda function for SFTP user setup. EventBridge offers a flexible event-driven approach to automate operational procedures and workflows, enhancing the system's reliability and efficiency.

Proposed Improvements
---------------------

1.  **SFTP Server ID Storage**: Store the SFTP server ID in a DynamoDB table for precise policy Resource Defining, avoiding the use of `Resource = *`(least privilege principle).
2.  **Scheduled SFTP Server Management**: Implement a system to fetch the last SFTP server ID and schedule server deletion for the first day of each month, allowing a maximum lifespan of 2 days post-creation if not manually terminated by the admin.
3.  **Lambda Function for User Addition**: Create a Lambda function to automatically add users stored in the DynamoDB table to the SFTP server upon its activation, using the server ID from the database.
4.  **Lambda Function to delete the sftp server based on the number of uploads**: after each upload in a month a counter is incremented by one after the counter reaches the number of employee's existing in the SFTPUsers table the sftp server is deleted

### Additional Suggestion

*   **Monitoring and Alerts**: Implement CloudWatch to monitor system activities and trigger alerts for any anomalies or system failures, ensuring timely response to issues.

This guide aims to offer a foundational understanding of the system's workings and areas for potential enhancements to ensure its scalability, security, and efficiency.