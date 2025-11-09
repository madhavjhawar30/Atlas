# Quick Fix: HTTPS Setup for Backend

## Current Issue
- Frontend: `https://goatlas.tech/` (HTTPS) ✅
- Backend: `http://your_vultr_ip:8001` (HTTP) ❌
- **Browsers block HTTP requests from HTTPS pages** (Mixed Content Error)

## Solution Options

### Option 1: Set Up HTTPS Backend (Recommended - 15 minutes)

**You need to:**
1. Set up Nginx as reverse proxy on your Vultr server
2. Get SSL certificate with Let's Encrypt
3. Use `https://api.goatlas.tech` as your backend URL

**Follow the guide in `VULTR_HTTPS_SETUP.md`**

---

### Option 2: Quick Test (Development Only)

If you just want to test locally, you can run the frontend locally over HTTP:

```bash
cd frontend
npm run dev
```

Then access it at `http://localhost:5173` (not HTTPS)

**Note:** This won't work for production since your site is on HTTPS.

---

## Immediate Steps

### 1. Set Up HTTPS Backend (Do This Now)

**On your Vultr server:**

1. **Install Nginx:**
   ```bash
   sudo apt update
   sudo apt install nginx certbot python3-certbot-nginx -y
   ```

2. **Configure Nginx:**
   ```bash
   sudo nano /etc/nginx/sites-available/api.goatlas.tech
   ```
   
   Add:
   ```nginx
   server {
       listen 80;
       server_name api.goatlas.tech;
       
       location / {
           proxy_pass http://localhost:8001;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

3. **Enable site:**
   ```bash
   sudo ln -s /etc/nginx/sites-available/api.goatlas.tech /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **Add DNS A record:**
   - Go to your domain registrar (where you manage goatlas.tech)
   - Add A record: `api` → Your Vultr server IP
   - Wait 5-10 minutes for DNS propagation

5. **Get SSL certificate:**
   ```bash
   sudo certbot --nginx -d api.goatlas.tech
   ```

6. **Update firewall:**
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   ```

### 2. Update Frontend

After HTTPS is set up:

1. **Edit `frontend/.env.production`:**
   ```
   VITE_API_URL=https://api.goatlas.tech
   ```

2. **Rebuild frontend:**
   ```bash
   cd frontend
   npm run build
   ```

3. **Copy to docs:**
   ```bash
   cp -r frontend/dist/* docs/
   ```

4. **Commit and push:**
   ```bash
   git add docs/
   git commit -m "Update frontend to use HTTPS backend"
   git push
   ```

---

## Verify It Works

1. **Test backend HTTPS:**
   ```bash
   curl https://api.goatlas.tech/health
   ```
   Should return: `{"status": "ok", "message": "Backend is running"}`

2. **Test from browser:**
   - Go to `https://goatlas.tech`
   - Open DevTools (F12) → Console
   - Should see no mixed content errors
   - Try uploading an image

---

## What's Your Vultr Server IP?

To help you set this up, I need to know:
- Your Vultr server IP address
- Or if you've already set up a domain for it

Once you provide this, I can help you configure everything correctly.

