# Atlas of Images 🧭

A live, explorable visual map that transforms images into an interactive 3D neural network visualization.

## Concept

Drop in images or turn on your webcam. Each image is converted into a CLIP embedding (512-D vector), projected into 3D space using UMAP, and rendered as nodes in a neural network-like visualization. Search in natural language, explore clusters, and watch your live camera move around the map. Claude (via AWS Bedrock) names clusters and explains what you're seeing.

## Features

- **3D Neural Map**: Interactive Three.js visualization with nodes (images) and edges (similarity connections)
- **CLIP Embeddings**: Semantic image understanding using OpenAI's CLIP model
- **Live Mode**: Real-time webcam embedding with position updates
- **Natural Language Search**: Text queries converted to embeddings to find similar images
- **Claude Integration**: AI-powered cluster naming and explanations via AWS Bedrock
- **AWS Infrastructure**: S3 storage, Lambda processing, and Bedrock AI

## Architecture

```
[Images/Webcam]
      ↓
[CLIP Embeddings] (512-D vectors)
      ↓
[UMAP Projection] (3D coordinates)
      ↓
[kNN Graph] (similarity edges)
      ↓
[Three.js Visualization] + [Claude Cluster Names]
```

## Tech Stack

### Backend
- **Python**: CLIP embeddings, UMAP projection, kNN graph
- **FastAPI**: REST API for embedding and processing
- **AWS Lambda**: Serverless image processing
- **AWS S3**: Image storage
- **AWS Bedrock**: Claude integration

### Frontend
- **React + Vite**: Modern web framework
- **Three.js / React Three Fiber**: 3D visualization
- **TailwindCSS**: Styling

### ML/AI
- **CLIP** (open-clip-torch): Image embeddings
- **UMAP**: Dimensionality reduction
- **FAISS**: Fast k-nearest neighbors search
- **Claude 3**: Cluster naming and explanations

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- AWS Account (for production deployment)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Environment Variables

Create `.env` files in both `backend/` and `frontend/`:

**backend/.env**:
```
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
S3_BUCKET_NAME=atlas-images
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
```

**frontend/.env**:
```
VITE_API_URL=http://localhost:8000
VITE_S3_BUCKET_URL=https://your-bucket.s3.amazonaws.com
```

## Project Structure

```
Atlas/
├── backend/
│   ├── app.py                 # FastAPI main application
│   ├── clip_service.py        # CLIP embedding service
│   ├── umap_service.py        # UMAP projection service
│   ├── knn_service.py         # k-NN graph builder
│   ├── claude_service.py      # AWS Bedrock Claude integration
│   ├── aws_lambda/            # Lambda function handlers
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Scene3D.jsx    # Three.js neural map
│   │   │   ├── NodeTooltip.jsx
│   │   │   ├── SearchBar.jsx
│   │   │   ├── WebcamMode.jsx
│   │   │   └── ClusterPanel.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── data/                      # Generated data files
│   ├── coords.json           # 3D coordinates
│   ├── graph.json            # kNN edges
│   ├── meta.json             # Image metadata
│   └── clusters.json         # Claude-labeled clusters
└── README.md
```

## Usage

1. **Upload Images**: Drag and drop images or click to upload
2. **View Map**: Explore the 3D neural network visualization
3. **Hover**: See image thumbnails and detected labels
4. **Click**: View full image and nearest neighbors
5. **Search**: Type natural language queries (e.g., "cozy desk with coffee")
6. **Live Mode**: Turn on webcam to see your position on the map in real-time
7. **Clusters**: View Claude-generated cluster names and explanations

## AWS Deployment

See `deployment/` directory for:
- CloudFormation templates
- Lambda deployment scripts
- S3 bucket configuration
- API Gateway setup

## Demo Script

1. Show initial map with sample images
2. Upload new images → watch dots appear
3. Turn on webcam → dot moves with scene changes
4. Search "laptop and coffee" → highlights relevant cluster
5. Click cluster → Claude explains why images are grouped
6. Show guided tour feature

## Performance Notes

- CLIP inference: ~50ms per image (GPU) / ~200ms (CPU)
- UMAP projection: One-time fit, then transform in ~10ms
- kNN search: <5ms with FAISS for 10k images
- Frontend: Smooth 60fps with instanced rendering

## License

MIT

## Acknowledgments

- OpenAI CLIP
- UMAP-learn
- Three.js community
- AWS for infrastructure
- Anthropic Claude for AI features

