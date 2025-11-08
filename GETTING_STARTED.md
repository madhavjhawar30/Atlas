# Getting Started with Atlas of Images

Welcome! This guide will help you get Atlas running in under 10 minutes.

## What You're Building

A **3D neural network visualization** where:
- Each glowing node = an image
- Proximity = semantic similarity
- You can search, explore, and even position yourself via webcam
- Powered by CLIP embeddings, UMAP projection, and Claude AI

## Prerequisites Check

Run these commands to verify:

```bash
python --version   # Need 3.9+
node --version     # Need 18+
git --version      # Should have git
```

Don't have them? Install:
- Python: https://www.python.org/downloads/
- Node: https://nodejs.org/
- Git: https://git-scm.com/

## Step-by-Step Setup

### 1. Get the Code

You already have it! You're in the `/Users/madhavjhawar/Atlas` directory.

### 2. Backend Setup (Python)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate
# On Windows: venv\Scripts\activate

# Install everything (takes 2-3 minutes)
pip install -r requirements.txt
```

**Note**: The first time you run the backend, it will download the CLIP model (~350MB). This is normal and only happens once.

### 3. Frontend Setup (Node.js)

Open a **new terminal** (keep the backend terminal open):

```bash
cd frontend

# Install dependencies (takes 1-2 minutes)
npm install
```

### 4. Start Everything

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate  # if not already activated
python app.py
```

Wait for: `✅ All services initialized`

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

Wait for: `Local: http://localhost:5173`

### 5. Open in Browser

Go to: **http://localhost:5173**

You should see the Atlas interface!

## First Test

1. **Upload Images**:
   - Drag 10-15 images into the upload panel
   - Or click to browse and select them
   - Mix categories: landscapes, food, indoor scenes, etc.

2. **Wait for Processing**:
   - You'll see "Uploading images..."
   - Then "Projecting to 3D space..."
   - Then "Building similarity graph..."
   - Takes ~10-20 seconds total

3. **Explore**:
   - Drag to rotate the 3D map
   - Scroll to zoom
   - Click a node (sphere) to see details
   - Notice similar images are connected!

4. **Search**:
   - Type in the search box: "laptop" or "outdoor" or "food"
   - Click Search
   - Watch matching nodes light up in yellow!

5. **Live Mode** (Optional):
   - Click "Start Webcam" in the Live Mode panel
   - Allow camera access
   - Hold objects up to the camera
   - Watch your position update on the map!

## Project Structure Overview

```
Atlas/
├── backend/          ← Python API server
├── frontend/         ← React + Three.js app
├── data/            ← Your uploaded images (created automatically)
├── README.md        ← Full documentation
├── QUICKSTART.md    ← 5-minute guide
└── DEMO_SCRIPT.md   ← For presentations
```

## What's Next?

### Learn More
- Read `README.md` for complete documentation
- Check `SETUP.md` for troubleshooting
- See `PROJECT_SUMMARY.md` for technical details

### Deploy to AWS
- Follow `deployment/deploy.sh`
- Enables Claude cluster labeling
- Scales to thousands of images

### Customize
- Edit `frontend/src/components/Scene3D.jsx` for visuals
- Modify `tailwind.config.js` for colors
- Tweak UMAP parameters in `backend/.env`

## Common Issues

### "Port 8000 already in use"
Another app is using that port. Either:
- Stop the other app
- Or change the port in `backend/app.py`: `port = 8001`

### "Module not found: open_clip"
Your virtual environment isn't activated:
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### "Cannot access camera"
- Browser needs camera permission (check browser settings)
- Must upload images first before webcam mode works
- Chrome/Firefox work best

### "UMAP error: n_samples < n_neighbors"
- Upload more images (need at least 10-15)
- Or lower n_neighbors in code

### Nothing shows up on the map
- Check backend terminal for errors
- Check browser console (F12) for errors
- Make sure you waited for "projection complete"

## Get Help

1. Check the error message in terminal
2. Look for logs in `backend.log` and `frontend.log`
3. Read `SETUP.md` troubleshooting section
4. Check that Python 3.9+ and Node 18+ are installed

## Stop the Servers

Press `Ctrl+C` in each terminal window.

Or use the stop script:
```bash
./stop.sh
```

---

## Quick Reference

### Start
```bash
./start.sh           # Starts both servers
```

### Stop
```bash
./stop.sh            # Stops both servers
```

### View Logs
```bash
tail -f backend.log  # Backend logs
tail -f frontend.log # Frontend logs
```

### Reset Data
```bash
rm -rf data/         # Deletes all uploaded images and generated files
```

---

**You're ready to explore visual space! 🧭✨**

Open http://localhost:5173 and start uploading images!

