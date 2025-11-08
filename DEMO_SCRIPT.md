# Atlas of Images - Demo Script

**Duration**: 2-3 minutes  
**Goal**: Showcase the key features and wow the judges

---

## Pre-Demo Setup (Do Before Presenting)

1. Have 20-30 diverse images ready:
   - Landscapes
   - Food
   - Indoor scenes (desks, plants)
   - Outdoor activities
   - Vehicles
   - Animals

2. Upload 15 images before the demo starts
3. Ensure projection and graph are built
4. Have the map already visible and rotating

---

## Demo Flow

### 1. Introduction (15 seconds)

> "This is **Atlas of Images** - a live 3D neural network visualization of visual space. 
> Each glowing node is an image. Proximity means semantic similarity. 
> Watch how we can explore, search, and navigate through thousands of images in real-time."

**Action**: Slowly rotate and zoom through the existing map, showing the neural network aesthetic.

---

### 2. Upload & Watch It Grow (30 seconds)

> "Let me add some new images. As I upload, watch the map expand and new connections form."

**Action**: 
- Drag and drop 5 new images
- Wait for processing animation
- Show new nodes appearing and edges connecting

> "Behind the scenes, we're using CLIP to generate 512-dimensional semantic embeddings, 
> then projecting to 3D with UMAP. Each edge represents similarity in that high-dimensional space."

---

### 3. Natural Language Search (30 seconds)

> "Now let's search using natural language. Say I'm looking for 'cozy desk with a laptop'..."

**Action**:
- Type query: "cozy desk with laptop"
- Click search
- Watch matching nodes highlight in yellow

> "Notice how it found semantically similar images, even if they don't match exactly. 
> This is the power of CLIP - it understands concepts, not just pixels."

**Action**: Click on a highlighted node to see neighbors

---

### 4. Live Webcam Mode (45 seconds) ⭐ **WOW MOMENT**

> "Here's where it gets interesting. Let me turn on the webcam."

**Action**: Click "Start Webcam"

> "Watch this dot - that's me, in real-time, positioned based on what the camera sees."

**Action**: 
- Hold up your laptop → "See it moving toward the desk cluster?"
- Hold up a coffee mug → "Now it's near the kitchen items"
- Show your face → "And when I show my face, it moves to the people region"
- Point at a plant → "Plants cluster over here..."

> "The map updates every 2 seconds, constantly embedding my webcam feed 
> and finding where I belong in this visual universe."

---

### 5. Claude Integration (30 seconds)

> "And here's where AWS Bedrock and Claude come in."

**Action**: 
- Click on a dense cluster
- Show the detail panel

> "Claude automatically names and explains these clusters. 
> For example, this one is called 'Modern Workspaces' - 
> Claude analyzed the common objects, colors, and themes to generate that label."

*(If you have time, show the cluster explanation feature)*

---

### 6. Technical Stack (15 seconds)

> "Quick tech overview: 
> - **AWS Bedrock** powers Claude for cluster labeling and explanations
> - **CLIP** for state-of-the-art image embeddings
> - **UMAP** for dimensionality reduction
> - **Three.js** for the 3D visualization
> - **FastAPI** backend on AWS Lambda
> - **S3** for storage, all serverless"

---

### 7. Use Cases & Closing (15 seconds)

> "Imagine using this for:
> - **E-commerce**: Visual product discovery at scale
> - **Content moderation**: Instantly find similar flagged content
> - **Medical imaging**: Group similar scans for diagnosis
> - **Creative tools**: Explore your photo library in a completely new way
>
> Atlas of Images - making visual search intuitive and explorable."

---

## Backup Demos (If Time Permits)

### Image-Based Search
- Upload a query image
- Show similar results instantly

### Neighbor Exploration
- Click through connected nodes
- Show similarity percentages

### Guided Tour
- If implemented, show Claude's generated tour

---

## Troubleshooting During Demo

**Map not loading?**
- Refresh and show sample data
- Explain it's fast for <1000 images, scales with OpenSearch

**Webcam not working?**
- Skip and focus on search/exploration
- Say "WebRTC/HTTPS required in production"

**Search not finding anything?**
- Try broader terms: "outdoor", "indoor", "food"
- Show manual exploration instead

---

## Key Talking Points

✅ **Real-time** - Live webcam positioning  
✅ **AI-Powered** - CLIP embeddings + Claude labeling  
✅ **Scalable** - Built on AWS serverless  
✅ **Beautiful UX** - Neural network aesthetic  
✅ **Novel** - No one else is doing visual space exploration like this  

---

## Judging Criteria Alignment

| Criterion | How We Address |
|-----------|----------------|
| **Technical Complexity** | CLIP, UMAP, 3D rendering, real-time processing |
| **AWS Usage** | Bedrock (Claude), Lambda, S3, API Gateway |
| **Claude Integration** | Cluster naming, explanations, search assistance |
| **Innovation** | Live webcam positioning in embedding space |
| **User Experience** | Intuitive, beautiful, interactive |
| **Completeness** | Fully functional end-to-end demo |

---

## Post-Demo Q&A Prep

**Q: How fast does it scale?**  
A: CLIP inference ~50ms per image on GPU. For >10k images, we'd use OpenSearch k-NN for sub-10ms queries.

**Q: What about privacy/security?**  
A: Images never leave your infrastructure - everything runs on your AWS account. No third-party APIs except Bedrock.

**Q: Can it work with text + images?**  
A: Yes! CLIP's text encoder puts text and images in the same space. You could search "red sports car" and it finds matching images.

**Q: Production-ready?**  
A: MVP is working. For production: add auth, rate limiting, CDN for images, OpenSearch for scale, and better caching.

---

Good luck! 🧭✨

