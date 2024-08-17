import json
import boto3
import os

# Initialize the Lambda client
lambda_client = boto3.client('lambda',
                             aws_access_key_id=AWS_ACCESS_KEY,
                             aws_secret_access_key=AWS_SECRET_KEY,
                             region_name=REGION_NAME)

def invoke_lambda_function(function_name, payload):
    try:
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )

        response_payload = response['Payload'].read()
        response_data = json.loads(response_payload)

        return response_data

    except Exception as e:
        print(f"Error occurred while invoking Lambda function: {str(e)}")
        return None

if __name__ == "__main__":
    function_name = 'UserActivityCollector'  # Name of your Lambda function
    
    # Read the local JSON file
    with open('user_activity_data.json', 'r') as file:
        data = json.load(file)

    # Prepare the payload with data to send to Lambda
    payload = {
        'data': data  # Include the data in the payload
    }

    response = invoke_lambda_function(function_name, payload)
    print('Lambda function response:', response)
