import json
import boto3
from botocore.exceptions import ClientError


dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=REGION_NAME
)
table_name = 'UserActivity'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))

        for record in event['Records']:
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            print(f"Bucket: {bucket}, Key: {key}")

            s3_client = boto3.client('s3')
            response = s3_client.get_object(Bucket=bucket, Key=key)
            json_data = response['Body'].read().decode('utf-8')
            user_activities = json.loads(json_data)

            for activity in user_activities:
                # Check if all required keys are present
                required_keys = ['user_id', 'session_id', 'timestamp', 'page_url', 'product_id', 'action_type', 'referrer', 'device_type', 'location']
                if all(key in activity for key in required_keys):
                    table.put_item(
                        Item={
                            'userId': activity['user_id'],            # Partition key in DynamoDB
                            'sessionId': activity['session_id'],      # Assuming this is your sort key
                            'timestamp': activity['timestamp'],
                            'pageUrl': activity['page_url'],
                            'productId': activity['product_id'],
                            'actionType': activity['action_type'],
                            'referrer': activity['referrer'],
                            'deviceType': activity['device_type'],
                            'location': activity['location']
                        }
                    )
                else:
                    print(f"Error: Missing one or more required keys in activity: {activity}")
                    missing_keys = [key for key in required_keys if key not in activity]
                    print(f"Missing keys: {missing_keys}")

        return {
            'statusCode': 200,
            'body': json.dumps('User activities successfully stored in DynamoDB')
        }
    except ClientError as e:
        print(f"ClientError: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to store user activities in DynamoDB')
        }
    except Exception as e:
        print(f"Exception: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('An error occurred')
        }
