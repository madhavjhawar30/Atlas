"""
AWS Lambda Function: Upload Handler
Handles image upload to S3 and triggers embedding processing
"""

import json
import boto3
import base64
from datetime import datetime
import os

s3_client = boto3.client('s3')
lambda_client = boto3.client('lambda')

BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'atlas-images')
EMBEDDING_FUNCTION = os.environ.get('EMBEDDING_FUNCTION_NAME', 'atlas-embedding-processor')


def lambda_handler(event, context):
    """
    Lambda handler for image upload
    
    Expected event format:
    {
        "body": base64-encoded image data,
        "filename": original filename,
        "contentType": image MIME type
    }
    """
    try:
        # Parse input
        if 'body' not in event:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing image data'})
            }
        
        # Decode image
        image_data = base64.b64decode(event['body'])
        filename = event.get('filename', f'image_{datetime.now().timestamp()}.jpg')
        content_type = event.get('contentType', 'image/jpeg')
        
        # Generate S3 key
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        s3_key = f'images/{timestamp}_{filename}'
        
        # Upload to S3
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=image_data,
            ContentType=content_type,
            Metadata={
                'upload_timestamp': timestamp,
                'original_filename': filename
            }
        )
        
        # Generate public URL
        image_url = f'https://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}'
        
        # Trigger embedding processing (async)
        try:
            lambda_client.invoke(
                FunctionName=EMBEDDING_FUNCTION,
                InvocationType='Event',  # Async invocation
                Payload=json.dumps({
                    'bucket': BUCKET_NAME,
                    'key': s3_key
                })
            )
        except Exception as e:
            print(f"Warning: Could not trigger embedding function: {e}")
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Image uploaded successfully',
                'imageUrl': image_url,
                's3Key': s3_key,
                'bucket': BUCKET_NAME
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

