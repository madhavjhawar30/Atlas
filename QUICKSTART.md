# Atlas of Images - Quick Start (5 Minutes)

Get up and running in 5 minutes with this streamlined guide.

## Prerequisites

- Python 3.9+
- Node.js 18+
- 2GB free disk space (for CLIP model)

## Installation

### 1. Backend Setup (2 minutes)

```bash
# Create virtual environment
cd backend
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (this will take ~1-2 minutes)
pip install -r requirements.txt

# The first run will download CLIP model (~350MB)
# This is a one-time download
```

### 2. Frontend Setup (1 minute)

```bash
# In a new terminal
cd frontend
npm install
```

## Run

### Option A: Manual Start (Recommended for First Time)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python app.py
```

Wait until you see: `✅ All services initialized`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Option B: Quick Start Script

```bash
chmod +x start.sh
./start.sh
```

## First Use

1. Open http://localhost:5173
2. Upload 5-10 images (drag & drop)
3. Wait ~10 seconds for processing
4. Explore the 3D neural map! 🎉

## Quick Tips

### Controls
- **Drag**: Rotate the map
- **Scroll**: Zoom in/out  
- **Click node**: View details and neighbors
- **Search box**: Try "laptop", "outdoor", "food"

### Recommended Test Images
- Mix of indoor/outdoor scenes
- Different categories (food, nature, tech, people)
- At least 10 images for good visualization

### Common First-Time Issues

**Port 8000 in use?**
```bash
# Change port in backend/app.py
port = int(os.getenv("API_PORT", "8001"))  # Changed to 8001
```

**CLIP download slow?**
- Just wait, it's a one-time ~350MB download
- Or manually download: `python -c "import open_clip; open_clip.create_model_and_transforms('ViT-B-32', pretrained='openai')"`

**Need more images?**
- Upload at least 10-15 for best results
- Try free stock photos from unsplash.com

## What's Happening Behind the Scenes

1. **Upload**: Image saved to `data/images/`
2. **Embedding**: CLIP converts image → 512-D vector
3. **Projection**: UMAP reduces 512-D → 3-D coordinates
4. **Graph**: k-NN finds 8 most similar images per node
5. **Visualization**: Three.js renders the neural network

## Next Steps

- Try the **webcam mode** (requires 15+ uploaded images)
- Experiment with **search queries**
- Explore **neighbor connections** by clicking nodes
- Check out `DEMO_SCRIPT.md` for showcase ideas
- Read `SETUP.md` for AWS deployment

## Stop Servers

Press `Ctrl+C` in each terminal, or:

```bash
./stop.sh
```

## Get Help

- Check `backend.log` and `frontend.log` for errors
- Review `SETUP.md` for detailed troubleshooting
- Ensure Python 3.9+ and Node 18+ are installed

---

**Enjoy exploring visual space! 🧭**

