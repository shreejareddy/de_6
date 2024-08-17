import boto3
import logging
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


cloudwatch = boto3.client(
    'cloudwatch',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=REGION_NAME
)

def create_cloudwatch_alarms():
    try:
        # Alarm for DataCollector Lambda function
        cloudwatch.put_metric_alarm(
            AlarmName='DataCollectorErrors',
            MetricName='Errors',
            Namespace='AWS/Lambda',
            Statistic='Sum',
            Period=60,
            Threshold=1,
            ComparisonOperator='GreaterThanOrEqualToThreshold',
            EvaluationPeriods=1,
            # No AlarmActions configured here
            Dimensions=[
                {'Name': 'FunctionName', 'Value': 'DataCollectorFunction'}
            ]
        )
        logger.info("Created CloudWatch alarm for DataCollector Lambda function.")
        
        # Alarm for DataProcessor Lambda function
        cloudwatch.put_metric_alarm(
            AlarmName='DataProcessorErrors',
            MetricName='Errors',
            Namespace='AWS/Lambda',
            Statistic='Sum',
            Period=60,
            Threshold=1,
            ComparisonOperator='GreaterThanOrEqualToThreshold',
            EvaluationPeriods=1,
            # No AlarmActions configured here
            Dimensions=[
                {'Name': 'FunctionName', 'Value': 'DataProcessorFunction'}
            ]
        )
        logger.info("Created CloudWatch alarm for DataProcessor Lambda function.")
    
    except ClientError as e:
        logger.error(f"Error creating CloudWatch alarms: {e}")
        raise e

if __name__ == "__main__":
    create_cloudwatch_alarms()
