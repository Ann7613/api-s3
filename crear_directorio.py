import json
import boto3
import base64

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        elif isinstance(event.get('body'), dict):
            body = event['body']
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid body format'})
            }

        bucket_name = body.get('bucket')
        directory_name = body.get('directory_name')

        if not bucket_name or not directory_name:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing bucket or directory_name'})
            }

        if not directory_name.endswith('/'):
            directory_name += '/'


        s3_client.put_object(Bucket=bucket_name, Key=directory_name)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Directory "{directory_name}" created in bucket "{bucket_name}".'})
        }

    except s3_client.exceptions.NoSuchBucket:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': f'Bucket "{bucket_name}" does not exist.'})
        }

    except Exception as e:

        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
