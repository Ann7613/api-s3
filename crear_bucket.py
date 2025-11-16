import json
import boto3
import uuid

s3_client = boto3.client('s3')
REGION = 'us-east-1'

def lambda_handler(event, context):
    try:
        body = event['body']
        if isinstance(body, str):
            body = json.loads(body)
        
        prefix = body.get('bucket_prefix', 'mi-bucket')
        bucket_name = f"{prefix}-{uuid.uuid4().hex[:8]}"

        if REGION == 'us-east-1':
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': REGION}
            )

        return {
            'statusCode': 200,
            'body': f"Bucket {bucket_name} created successfully."
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }
