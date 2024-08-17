import boto3
import logging
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=REGION_NAME
)

RAW_DATA_BUCKET = 'user-activity-data-bucket'

def create_buckets():
    try:
        s3.create_bucket(Bucket=RAW_DATA_BUCKET, CreateBucketConfiguration={'LocationConstraint': REGION_NAME})
        logger.info(f"Created S3 buckets: {RAW_DATA_BUCKET}")
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            logger.info("Buckets already exist.")
        else:
            logger.error(f"Error creating buckets: {e}")
            raise e

if __name__ == "__main__":
    create_buckets()
