AWS SFTP to S3 Automation Project
=================================

Introduction
------------

This project automates the file transfer process from a publicly accessible S3 bucket, intended for user uploads, to another S3 bucket exclusively accessible by the administrator. It also automates the monthly setup of an SFTP server, utilizing AWS services such as S3 buckets, Lambda functions, AWS Transfer Family, and DynamoDB for comprehensive and secure file management.

Table of Contents
-----------------

*   [Introduction](#introduction)
*   [Architecture Overview](#architecture-overview)
*   [Installation](#installation)
    *   [Prerequisites](#prerequisites)
    *   [Setup Steps](#setup-steps)
*   [Usage](#usage)
    *   [Uploading Files via SFTP](#uploading-files-via-sftp)
    *   [Monitoring and Managing Transfers](#monitoring-and-managing-transfers)
*   [Features](#features)
*   [Additional Efforts and Learnings](#additional-efforts-and-learnings)
*   [Configuration](#configuration)
*   [Documentation](#documentation)

Architecture Overview
---------------------

The solution architecture includes:

*   **Two S3 Buckets**: A source bucket for user uploads and a destination bucket for administrator access.
*   **Lambda Function**: Automates file copying from the source to the destination bucket.
*   **AWS Transfer Family SFTP Server**: Facilitates secure file uploads to the source S3 bucket.
*   **DynamoDB Table**: Stores user information and public SSH keys for SFTP access.
*   **Event Scheduler**: Manages the SFTP server's operational schedule to optimize costs.

Installation
------------

### Prerequisites

*   An AWS account with access to S3, Lambda, AWS Transfer Family, DynamoDB, EventBridge, and IAM.
*   AWS CLI installed and configured.
*   Basic knowledge of AWS services and SFTP protocols.

### Setup Steps

1.  **Create S3 Buckets**: Establish two S3 buckets for source and destination purposes.
2.  **Setup SFTP Server**: Deploy an SFTP server via AWS Transfer Family linked to the source S3 bucket. Schedule the server to start operations two days before each month's end.
3. **SFTP Server Deletion**: Schedule the deletion of the SFTP server at the first day of each month 10 Am.
4.  **Deploy Lambda Function**: Implement a Lambda function triggered by file uploads to the source bucket, facilitating file transfers to the destination bucket.
5.  **Prepare DynamoDB Table**: Construct a DynamoDB table for storing user details and SSH keys.
6.  **Configure SFTP Users**: Employ a Lambda function to integrate user details from the DynamoDB table into the SFTP server.
7.  **Schedule SFTP Server Management**: Utilize an event-based system for SFTP server operational scheduling.

Usage
-----

### Uploading Files via SFTP

Users, with their credentials and SSH keys, can securely upload files to the SFTP server. These files are automatically transferred to the source S3 bucket.

### Monitoring and Managing Transfers

The project uses a Lambda function to oversee new uploads and facilitate their transfer to the destination bucket. This process can be monitored via AWS CloudWatch logs and S3 event notifications.

Features
--------

*   Secure SFTP file upload.
*   Automated file transfer between S3 buckets.
*   SFTP server operational time optimization for cost management.
*   Simplified user management via DynamoDB.
*   Project deployment automation using Infrastructure as Code (IaC) with AWS CloudFormation.

Additional Efforts and Learnings
--------------------------------
In this project, my aim was not only to meet the essential requirements but also to explore and integrate practices that could enhance the robustness and security of the solution. I am continuously learning and were excited to incorporate some of my learnings into the project. Here’s a brief overview of what I've attempted to achieve:

*   **Infrastructure as Code (IaC)**:  Utilizing AWS CloudFormation, I've adhered to the principles of IaC for the entire deployment of the project. This approach enables us to automate and replicate our infrastructure setup effortlessly, ensuring consistency and reducing manual errors. The `template.yaml` file in the deployment folder outlines the configurations for all AWS services involved.
*   **Security and DevSecOps Mindset**: Security is at the core of the project design. I've ensured that all file transfers are encrypted, safeguarding the data in transit and at rest..
*   **Least Privilege Principle**:  In line with best practices for access management, I've meticulously crafted IAM policies to adhere to the least privilege principle. This means that each component of the solution, from Lambda functions to SFTP server access, is granted only the permissions necessary to perform its intended functions.(But i could do better take a look at the developer guide)

Configuration
-------------

Refer to the `template.yaml` file in the deployment folder for detailed AWS service configurations.

Documentation
-------------

For detailed configuration instructions and service overviews, please consult the official AWS documentation:

*   [AWS S3](https://docs.aws.amazon.com/s3/)
*   [AWS Lambda](https://docs.aws.amazon.com/lambda/)
*   [AWS Transfer for SFTP](https://docs.aws.amazon.com/transfer/latest/userguide/)
*   [Amazon DynamoDB](https://docs.aws.amazon.com/dynamodb/)
*   [AWS CloudFormation](https://docs.aws.amazon.com/cloudformation/)
*   [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/)
*   [AWS IAM](https://docs.aws.amazon.com/iam/)