import boto3
import time

# Initialize the Lambda client
lambda_client = boto3.client('lambda',
                             aws_access_key_id=AWS_ACCESS_KEY,
                             aws_secret_access_key=AWS_SECRET_KEY,
                             region_name=REGION_NAME)
# Define your S3 bucket name and IAM role ARN
bucket_name = 'user-activity-data-bucket'  # Replace with your actual bucket name
role_arn = 'arn:aws:iam::014498618598:role/LambdaExecutionRole'  # Replace with your IAM role ARN

def wait_for_update(function_name):
    while True:
        response = lambda_client.get_function(FunctionName=function_name)
        status = response['Configuration']['State']
        last_update_status = response['Configuration'].get('LastUpdateStatus')

        if status == 'Active' and last_update_status != 'InProgress':
            break
        print(f"Current status: {status}, Last update status: {last_update_status}. Waiting for function update to complete...")
        time.sleep(5)
    print(f"Function update completed with status: {status}")

try:
    with open('lambda_function.zip', 'rb') as zip_file:
        # Update the Lambda function code
        response = lambda_client.update_function_code(
            FunctionName='UserActivityCollector',
            ZipFile=zip_file.read(),  # Read the zip file
        )
        print('Lambda function code updated:', response['FunctionArn'])

        # Wait for the update to complete
        wait_for_update('UserActivityCollector')

        # Update the function configuration to include environment variables
        response = lambda_client.update_function_configuration(
            FunctionName='UserActivityCollector',
            Environment={
                'Variables': {
                    'BUCKET_NAME': bucket_name,  # Set the S3 bucket name as an environment variable
                }
            }
        )
        print('Lambda function configuration updated:', response['FunctionArn'])
except lambda_client.exceptions.ResourceNotFoundException:
    # If the function does not exist, create it
    with open('lambda_function.zip', 'rb') as zip_file:
        response = lambda_client.create_function(
            FunctionName='UserActivityCollector',
            Runtime='python3.8',
            Role=role_arn,  # IAM role ARN that allows access to S3
            Handler='lambda_function.lambda_handler',
            Code={
                'ZipFile': zip_file.read(),  # Read the zip file
            },
            Environment={
                'Variables': {
                    'BUCKET_NAME': bucket_name,  # Set the S3 bucket name as an environment variable
                },
            },
            Timeout=30,  # Set a timeout for the function (in seconds)
        )
    print('Lambda function created:', response['FunctionArn'])
