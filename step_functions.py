import boto3
import json
import logging
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
ROLE_ARN = 'arn:aws:iam::014498618598:role/StepFunctionsExecutionRole'

sfn = boto3.client(
    'stepfunctions',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=REGION_NAME
)

def create_step_function():
    definition = {
        "Comment": "A simple example of a Step Functions state machine",
        "StartAt": "DataCollector",
        "States": {
            "DataCollector": {
                "Type": "Task",
                "Resource": "arn:aws:lambda:us-east-2:014498618598:function:DataCollectorFunction",
                "Next": "DataProcessor"
            },
            "DataProcessor": {
                "Type": "Task",
                "Resource": "arn:aws:lambda:us-east-2:014498618598:function:DataProcessorFunction",
                "End": True
            }
        }
    }

    try:
        sfn.create_state_machine(
            name='UserActivityPipeline',
            definition=json.dumps(definition),
            roleArn=ROLE_ARN
        )
        logger.info("Created Step Functions state machine.")
    except ClientError as e:
        logger.error(f"Error creating Step Functions state machine: {e}")
        raise e

if __name__ == "__main__":
    create_step_function()
