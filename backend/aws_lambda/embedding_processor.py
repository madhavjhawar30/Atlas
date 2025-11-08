"""
AWS Lambda Function: Embedding Processor
Processes uploaded images to generate CLIP embeddings
Note: Requires Lambda container with PyTorch and CLIP installed
"""

import json
import boto3
import numpy as np
from PIL import Image
import io
import os

# These imports would work in a Lambda container with the right dependencies
# import torch
# import open_clip

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'atlas-embeddings')
CLIP_MODEL = os.environ.get('CLIP_MODEL', 'ViT-B-32')

# Global variables for model (loaded once per container)
model = None
preprocess = None
device = None


def load_model():
    """Load CLIP model (called once per Lambda container lifecycle)"""
    global model, preprocess, device
    
    if model is None:
        # Uncomment when deploying to Lambda with proper container
        # device = "cuda" if torch.cuda.is_available() else "cpu"
        # model, _, preprocess = open_clip.create_model_and_transforms(
        #     CLIP_MODEL, 
        #     pretrained='openai'
        # )
        # model = model.to(device).eval()
        
        # Placeholder for local testing
        device = "cpu"
        print(f"Model loaded on {device}")
    
    return model, preprocess, device


def generate_embedding(image_bytes):
    """
    Generate CLIP embedding for an image
    
    Args:
        image_bytes: Raw image bytes
        
    Returns:
        numpy array of embedding (512-d)
    """
    model, preprocess, device = load_model()
    
    # Load image
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
    # Uncomment for actual CLIP processing
    # img_tensor = preprocess(image).unsqueeze(0).to(device)
    # 
    # with torch.no_grad():
    #     image_features = model.encode_image(img_tensor)
    #     image_features = image_features / image_features.norm(dim=-1, keepdim=True)
    # 
    # embedding = image_features.squeeze(0).cpu().numpy()
    
    # Placeholder for testing
    embedding = np.random.randn(512).astype(np.float32)
    embedding = embedding / np.linalg.norm(embedding)
    
    return embedding


def lambda_handler(event, context):
    """
    Lambda handler for embedding generation
    
    Expected event format:
    {
        "bucket": "bucket-name",
        "key": "images/filename.jpg"
    }
    """
    try:
        # Parse input
        bucket = event['bucket']
        key = event['key']
        
        print(f"Processing {key} from {bucket}")
        
        # Download image from S3
        response = s3_client.get_object(Bucket=bucket, Key=key)
        image_bytes = response['Body'].read()
        
        # Generate embedding
        embedding = generate_embedding(image_bytes)
        
        # Store in DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        
        # Generate image ID from S3 key
        image_id = key.split('/')[-1].split('.')[0]
        
        table.put_item(
            Item={
                'image_id': image_id,
                's3_bucket': bucket,
                's3_key': key,
                'embedding': embedding.tolist(),
                'embedding_dim': len(embedding),
                'processed_timestamp': int(np.datetime64('now').astype(int) / 1e9)
            }
        )
        
        print(f"Embedding stored for {image_id}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Embedding generated successfully',
                'image_id': image_id,
                'embedding_dim': len(embedding)
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

