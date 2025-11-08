#!/bin/bash

# Atlas of Images - Deployment Script
# Deploys infrastructure and Lambda functions to AWS

set -e

PROJECT_NAME="atlas-images"
ENVIRONMENT="${1:-dev}"
AWS_REGION="${2:-us-east-1}"

echo "🚀 Deploying Atlas of Images to AWS"
echo "   Environment: $ENVIRONMENT"
echo "   Region: $AWS_REGION"
echo ""

# Deploy CloudFormation stack
echo "📦 Deploying CloudFormation stack..."
aws cloudformation deploy \
  --template-file cloudformation.yaml \
  --stack-name "${PROJECT_NAME}-${ENVIRONMENT}" \
  --parameter-overrides \
    ProjectName=$PROJECT_NAME \
    Environment=$ENVIRONMENT \
  --capabilities CAPABILITY_NAMED_IAM \
  --region $AWS_REGION

echo "✅ CloudFormation stack deployed"

# Get stack outputs
BUCKET_NAME=$(aws cloudformation describe-stacks \
  --stack-name "${PROJECT_NAME}-${ENVIRONMENT}" \
  --query "Stacks[0].Outputs[?OutputKey=='ImageBucketName'].OutputValue" \
  --output text \
  --region $AWS_REGION)

TABLE_NAME=$(aws cloudformation describe-stacks \
  --stack-name "${PROJECT_NAME}-${ENVIRONMENT}" \
  --query "Stacks[0].Outputs[?OutputKey=='EmbeddingsTableName'].OutputValue" \
  --output text \
  --region $AWS_REGION)

API_ENDPOINT=$(aws cloudformation describe-stacks \
  --stack-name "${PROJECT_NAME}-${ENVIRONMENT}" \
  --query "Stacks[0].Outputs[?OutputKey=='ApiEndpoint'].OutputValue" \
  --output text \
  --region $AWS_REGION)

echo ""
echo "📊 Stack Outputs:"
echo "   Bucket: $BUCKET_NAME"
echo "   Table: $TABLE_NAME"
echo "   API: $API_ENDPOINT"
echo ""

# Package and deploy Lambda functions
echo "📦 Packaging Lambda functions..."

cd ../backend/aws_lambda

# Create deployment package
if [ -d "package" ]; then
  rm -rf package
fi
mkdir package

pip install -r requirements.txt -t package/
cp *.py package/

cd package
zip -r ../lambda-deployment.zip .
cd ..

echo "✅ Lambda package created"

# Deploy upload handler
echo "🚀 Deploying upload handler..."
aws lambda create-function \
  --function-name "${PROJECT_NAME}-upload-${ENVIRONMENT}" \
  --runtime python3.11 \
  --role $(aws cloudformation describe-stacks \
    --stack-name "${PROJECT_NAME}-${ENVIRONMENT}" \
    --query "Stacks[0].Outputs[?OutputKey=='LambdaRoleArn'].OutputValue" \
    --output text \
    --region $AWS_REGION) \
  --handler upload_handler.lambda_handler \
  --zip-file fileb://lambda-deployment.zip \
  --timeout 30 \
  --memory-size 256 \
  --environment Variables="{S3_BUCKET_NAME=$BUCKET_NAME}" \
  --region $AWS_REGION \
  || aws lambda update-function-code \
    --function-name "${PROJECT_NAME}-upload-${ENVIRONMENT}" \
    --zip-file fileb://lambda-deployment.zip \
    --region $AWS_REGION

echo "✅ Lambda functions deployed"

# Clean up
rm -rf package lambda-deployment.zip

echo ""
echo "✨ Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Update backend/.env with:"
echo "   S3_BUCKET_NAME=$BUCKET_NAME"
echo "   AWS_REGION=$AWS_REGION"
echo ""
echo "2. Update frontend/.env with:"
echo "   VITE_API_URL=$API_ENDPOINT"
echo "   VITE_S3_BUCKET_URL=https://$BUCKET_NAME.s3.amazonaws.com"
echo ""
echo "3. Start the backend: cd backend && python app.py"
echo "4. Start the frontend: cd frontend && npm run dev"

