import json
import base64
import boto3

s3_resource = boto3.resource('s3')

def upload_base_64_to_s3(s3_bucket_name, s3_file_name, base_64_str):
    s3_resource.Object(s3_bucket_name, s3_file_name).put(Body=base64.b64decode(base_64_str))
    return (s3_bucket_name, s3_file_name)

def lambda_handler(event, context):
    try:
        body = event['body']
        if isinstance(body, str):
            body = json.loads(body)

        bucket_name = body.get('bucket')
        file_path = body.get('filepath')
        base64_content = body.get('content')
        
        if not all([bucket_name, file_path, base64_content]):
            return {'statusCode': 400, 'body': json.dumps({'error': 'Missing parameters: bucket, filepath, or content'})}

        bucket, key = upload_base_64_to_s3(bucket_name, file_path, base64_content)
        
        return {'statusCode': 200, 'body': json.dumps({'message': 'File uploaded successfully', 'location': f's3://{bucket}/{key}'})}
        
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': f'Internal Server Error: {str(e)}'})}
