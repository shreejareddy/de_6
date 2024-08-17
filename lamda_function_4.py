import boto3
import os

# Initialize the Lambda client
lambda_client = boto3.client('lambda',
                             aws_access_key_id=AWS_ACCESS_KEY,
                             aws_secret_access_key=AWS_SECRET_KEY,
                             region_name=REGION_NAME)
# Define your IAM role ARN
role_arn = 'arn:aws:iam::014498618598:role/LambdaExecutionRole'  # Use your IAM role ARN

def create_or_update_processing_lambda():
    try:
        with open('lambda_processing.zip', 'rb') as zip_file:
            # Update the Lambda function code
            response = lambda_client.update_function_code(
                FunctionName='UserActivityProcessingFunction',  # Name for your processing function
                ZipFile=zip_file.read(),
            )
            print('Processing Lambda function code updated:', response['FunctionArn'])

    except lambda_client.exceptions.ResourceNotFoundException:
        # If the function does not exist, create it
        with open('lambda_processing.zip', 'rb') as zip_file:
            response = lambda_client.create_function(
                FunctionName='UserActivityProcessingFunction',  # Name for your processing function
                Runtime='python3.8',
                Role=role_arn,
                Handler='lambda_processing.lambda_handler',
                Code={
                    'ZipFile': zip_file.read(),
                },
                Timeout=30,  # Set a timeout for the function (in seconds)
            )
        print('Processing Lambda function created:', response['FunctionArn'])

if __name__ == "__main__":
    create_or_update_processing_lambda()
