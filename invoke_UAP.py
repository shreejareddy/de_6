import boto3
import json

# Initialize the Lambda client


# Initialize the Lambda client
lambda_client = boto3.client('lambda',
                             aws_access_key_id=AWS_ACCESS_KEY,
                             aws_secret_access_key=AWS_SECRET_KEY,
                             region_name=REGION_NAME)
# Define the Lambda function name
lambda_function_name = 'UserActivityProcessingFunction'  # Replace with your Lambda function name

# Define the payload
payload = {
    "Records": [
        {
            "s3": {
                "bucket": {
                    "name": "user-activity-data-bucket"
                },
                "object": {
                    "key": "user_activity_data.json"
                }
            }
        }
    ]
}

def invoke_lambda(payload):
    try:
        response = lambda_client.invoke(
            FunctionName=lambda_function_name,
            InvocationType='RequestResponse',  # For synchronous invocation
            Payload=json.dumps(payload)
        )
        
        # Read and print the response
        response_payload = json.loads(response['Payload'].read().decode('utf-8'))
        print("Lambda function response:", response_payload)
        
        return response_payload
        
    except Exception as e:
        print(f"Error invoking Lambda function: {e}")
        return None

if __name__ == "__main__":
    invoke_lambda(payload)
