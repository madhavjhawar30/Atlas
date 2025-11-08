# Atlas of Images - Setup Guide

Complete setup instructions to get the project running locally and deploy to AWS.

## Prerequisites

### Required Software
- **Python 3.9+** - Backend ML processing
- **Node.js 18+** - Frontend development
- **Git** - Version control
- **AWS CLI** (optional) - For AWS deployment

### AWS Account (Optional for Local Development)
- AWS Account with permissions for:
  - S3 (image storage)
  - Lambda (serverless compute)
  - Bedrock (Claude AI)
  - DynamoDB (metadata storage)
  - CloudFormation (infrastructure)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Atlas
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env with your settings (optional for local dev)
# For local development without AWS, you can leave AWS settings blank
```

**Important Note on CLIP Model**: The first time you run the backend, CLIP will download the model weights (~350MB). This is a one-time download.

### 3. Frontend Setup

```bash
# Open a new terminal and navigate to frontend
cd frontend

# Install dependencies
npm install

# Create environment file (optional)
echo "VITE_API_URL=http://localhost:8000" > .env
```

### 4. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # if not already activated
python app.py
```

The backend will start on `http://localhost:8000`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

The frontend will start on `http://localhost:5173`

### 5. First Use

1. Open `http://localhost:5173` in your browser
2. Upload 5-10 images using the upload panel
3. Wait for processing (CLIP embedding + UMAP projection)
4. Explore the 3D neural map!

## Usage Guide

### Upload Images
- Drag and drop images into the upload panel
- Or click to browse and select multiple images
- Supported formats: JPG, PNG, WebP
- Recommended: Start with 10-20 images

### Explore the Map
- **Rotate**: Click and drag
- **Zoom**: Scroll or pinch
- **Select Node**: Click on any sphere
- **View Details**: Selected node info appears on the right
- **Neighbors**: See similar images automatically

### Search
- Type natural language queries: "sunset beach", "laptop and coffee", "indoor plants"
- Matching images will be highlighted in yellow
- Click search results to explore

### Live Mode (Webcam)
1. Upload several images first
2. Click "Start Webcam"
3. Allow camera access
4. Hold objects in view - your position updates every 2 seconds
5. Watch your dot move through the map!

## AWS Deployment (Optional)

### 1. Configure AWS CLI

```bash
aws configure
```

Enter your AWS credentials, region (e.g., `us-east-1`), and output format.

### 2. Enable AWS Bedrock

1. Go to AWS Console → Bedrock
2. Navigate to "Model access"
3. Request access to "Claude 3 Sonnet"
4. Wait for approval (usually instant)

### 3. Deploy Infrastructure

```bash
cd deployment
chmod +x deploy.sh
./deploy.sh dev us-east-1
```

This will:
- Create S3 bucket for images
- Set up DynamoDB table
- Deploy Lambda functions
- Configure API Gateway
- Set up IAM roles

### 4. Update Configuration

After deployment, the script will output configuration values. Update:

**backend/.env:**
```bash
AWS_ACCESS_KEY_ID=<your-key>
AWS_SECRET_ACCESS_KEY=<your-secret>
AWS_REGION=us-east-1
S3_BUCKET_NAME=<output-from-deployment>
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
```

**frontend/.env:**
```bash
VITE_API_URL=<api-endpoint-from-deployment>
VITE_S3_BUCKET_URL=https://<bucket-name>.s3.amazonaws.com
```

### 5. Deploy Frontend (AWS Amplify)

```bash
cd frontend
npm run build

# Upload dist/ folder to Amplify or S3 + CloudFront
```

## Troubleshooting

### CLIP Model Download Issues
If the CLIP model fails to download:
```bash
# Manually download and cache
python -c "import open_clip; open_clip.create_model_and_transforms('ViT-B-32', pretrained='openai')"
```

### Port Already in Use
If port 8000 or 5173 is in use:
```bash
# Backend - edit backend/app.py and change API_PORT
# Frontend - edit frontend/vite.config.js and change server.port
```

### UMAP Fitting Errors
If you get "n_samples < n_neighbors" error:
- Upload more images (minimum 15 recommended)
- Or reduce n_neighbors in backend/.env

### AWS Bedrock Access Denied
- Ensure you've requested model access in Bedrock console
- Check IAM permissions include `bedrock:InvokeModel`
- Verify correct region (Claude 3 not available in all regions)

### Webcam Not Working
- Ensure browser has camera permissions
- Use HTTPS in production (required for camera access)
- Check browser console for detailed errors

## Performance Optimization

### For Large Datasets (>1000 images)

1. **Use GPU for CLIP**:
   - Install PyTorch with CUDA support
   - Backend will automatically use GPU if available

2. **Batch Processing**:
   ```python
   # Process images in batches of 32
   for i in range(0, len(images), 32):
       batch = images[i:i+32]
       embeddings = clip_service.embed_images_batch(batch)
   ```

3. **Use OpenSearch Instead of FAISS**:
   - For >10k images, deploy Amazon OpenSearch
   - Replace `knn_service.py` with OpenSearch client

4. **Optimize UMAP**:
   ```python
   # Faster but less accurate
   umap_service = UMAPService(
       n_neighbors=5,  # reduced from 15
       min_dist=0.3,   # increased from 0.1
   )
   ```

## Project Structure Reference

```
Atlas/
├── backend/              # Python FastAPI backend
│   ├── app.py           # Main API server
│   ├── clip_service.py  # CLIP embeddings
│   ├── umap_service.py  # Dimensionality reduction
│   ├── knn_service.py   # Similarity search
│   ├── claude_service.py # AWS Bedrock integration
│   └── aws_lambda/      # Lambda functions
├── frontend/            # React + Three.js frontend
│   ├── src/
│   │   ├── components/  # UI components
│   │   ├── App.jsx     # Main app
│   │   ├── store.js    # State management
│   │   └── api.js      # Backend API client
│   └── package.json
├── data/               # Generated data (gitignored)
│   ├── images/        # Uploaded images
│   ├── coords.json    # 3D coordinates
│   ├── graph.json     # kNN graph
│   └── meta.json      # Image metadata
├── deployment/        # AWS deployment
│   ├── cloudformation.yaml
│   └── deploy.sh
└── README.md
```

## Next Steps

1. **Customize the visualization**:
   - Edit `Scene3D.jsx` to change node appearance
   - Modify colors in `tailwind.config.js`

2. **Add more features**:
   - Cluster labeling with Claude (already implemented in backend)
   - Guided tours (Claude service ready)
   - Image similarity comparison

3. **Scale to production**:
   - Set up CI/CD pipeline
   - Add authentication
   - Implement rate limiting
   - Monitor with CloudWatch

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review logs in terminal
3. Check browser console for frontend errors
4. Open an issue on GitHub

## License

MIT License - see LICENSE file for details

