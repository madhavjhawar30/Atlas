# Setting Up HTTPS for Vultr Backend

## Problem
Your frontend is served over HTTPS (`https://goatlas.tech/`), but your backend is HTTP. Browsers block mixed content (HTTP requests from HTTPS pages) for security reasons.

## Solution: Set up HTTPS with Nginx + Let's Encrypt

### Option 1: Use a Subdomain (Recommended)
Set up `api.goatlas.tech` as your backend URL.

### Option 2: Use IP with Self-Signed Certificate (Not Recommended)
Works but browsers will show security warnings.

---

## Step-by-Step: HTTPS with Nginx + Let's Encrypt

### Prerequisites
- Vultr server with Ubuntu/Debian
- Domain `goatlas.tech` (you already have this)
- Backend running on port 8001
- SSH access to your Vultr server

### 1. Install Nginx
```bash
sudo apt update
sudo apt install nginx -y
```

### 2. Install Certbot (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 3. Configure DNS
Add an A record for your subdomain:
- **Type**: A
- **Name**: `api` (or `backend`)
- **Value**: Your Vultr server IP address
- **TTL**: 3600 (or default)

Wait a few minutes for DNS to propagate (you can check with `dig api.goatlas.tech`).

### 4. Configure Nginx as Reverse Proxy

Create/edit Nginx configuration:
```bash
sudo nano /etc/nginx/sites-available/api.goatlas.tech
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name api.goatlas.tech;

    location / {
        proxy_pass http://localhost:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/api.goatlas.tech /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl reload nginx
```

### 5. Obtain SSL Certificate
```bash
sudo certbot --nginx -d api.goatlas.tech
```

Follow the prompts:
- Enter your email
- Agree to terms
- Choose whether to redirect HTTP to HTTPS (recommended: Yes)

Certbot will automatically:
- Obtain the SSL certificate
- Configure Nginx to use HTTPS
- Set up auto-renewal

### 6. Verify HTTPS Works
```bash
curl https://api.goatlas.tech/health
```

You should see a JSON response like:
```json
{"status": "ok", "message": "Backend is running"}
```

### 7. Update Frontend

Edit `frontend/.env.production`:
```
VITE_API_URL=https://api.goatlas.tech
```

Rebuild and deploy:
```bash
cd frontend
npm run build
# Copy dist/* to docs/
```

### 8. Update CORS (if needed)

Your backend already allows `https://goatlas.tech`, but if you want to be more specific, you can update `app.py`:
```python
allow_origins=[
    "https://goatlas.tech",
    "https://api.goatlas.tech",  # Add this if needed
    # ... other origins
]
```

### 9. Verify Auto-Renewal
Certbot sets up auto-renewal automatically. Test it:
```bash
sudo certbot renew --dry-run
```

---

## Alternative: Use Same Domain with Path (No Subdomain)

If you don't want to use a subdomain, you can serve the API at `https://goatlas.tech/api/`:

1. Configure Nginx to proxy `/api/*` to `localhost:8001`
2. Update your frontend to use `https://goatlas.tech/api`
3. Update your backend routes (or use a path prefix in FastAPI)

However, this is more complex and the subdomain approach is cleaner.

---

## Troubleshooting

### DNS not resolving?
- Wait a few minutes for DNS propagation
- Check with `dig api.goatlas.tech` or `nslookup api.goatlas.tech`
- Verify the A record is correct in your DNS settings

### Certificate not working?
- Make sure port 80 and 443 are open in your firewall
- Check Nginx configuration: `sudo nginx -t`
- Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`

### Backend not accessible?
- Verify backend is running: `sudo systemctl status atlas.service`
- Check backend is listening on `0.0.0.0:8001` (not just `127.0.0.1`)
- Test locally: `curl http://localhost:8001/health`

### CORS errors?
- Backend already allows all origins with `"*"`
- If issues persist, check browser console for specific error
- Verify `https://goatlas.tech` is in the CORS allowed origins

---

## Firewall Configuration

Make sure ports 80 and 443 are open:
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw status
```

---

## Security Notes

- Let's Encrypt certificates expire every 90 days, but auto-renewal handles this
- Keep Nginx and Certbot updated: `sudo apt update && sudo apt upgrade`
- Consider restricting CORS origins in production (remove `"*"`)

