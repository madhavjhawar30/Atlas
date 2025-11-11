# Fix 413 Request Entity Too Large Error

## Problem
When uploading images, you get this error:
```
POST https://api.goatlas.tech/embed/batch net::ERR_FAILED 413 (Request Entity Too Large)
```

This happens because Nginx has a default limit of 1MB for file uploads, which is too small for images.

## Quick Fix (5 minutes)

**SSH into your Vultr server and run these commands:**

### 1. Edit Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/api.goatlas.tech
```

### 2. Add `client_max_body_size` to the server block

Find the `server {` block and add this line right after `server_name api.goatlas.tech;`:

```nginx
server {
    listen 80;
    server_name api.goatlas.tech;
    
    # ADD THIS LINE - Increase upload size limit to 100MB
    client_max_body_size 100M;
    
    location / {
        proxy_pass http://localhost:8001;
        # ... rest of config
    }
}
```

If you're using HTTPS (after running certbot), you'll have two server blocks (one for port 80, one for port 443). Add `client_max_body_size 100M;` to **both** server blocks.

### 3. Also add timeout settings (optional but recommended)

Inside the `location / {` block, add these timeout settings:

```nginx
location / {
    proxy_pass http://localhost:8001;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    
    # ADD THESE LINES - Increase timeouts for large uploads
    proxy_read_timeout 300s;
    proxy_connect_timeout 300s;
    proxy_send_timeout 300s;
}
```

### 4. Test and Reload Nginx

```bash
# Test the configuration
sudo nginx -t

# If test passes, reload Nginx
sudo systemctl reload nginx
```

### 5. Verify it works

Try uploading images again from your frontend. The 413 error should be gone.

---

## Full Example Configuration

Here's what your complete Nginx config should look like (for HTTPS):

```nginx
server {
    listen 80;
    server_name api.goatlas.tech;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.goatlas.tech;

    # SSL certificates (added by certbot)
    ssl_certificate /etc/letsencrypt/live/api.goatlas.tech/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.goatlas.tech/privkey.pem;

    # Increase upload size limit for image uploads
    client_max_body_size 100M;

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
        
        # Increase timeouts for large file uploads
        proxy_read_timeout 300s;
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
    }
}
```

---

## Troubleshooting

### Still getting 413 error?
- Make sure you added `client_max_body_size` to **all** server blocks (port 80 and 443)
- Verify the config is correct: `sudo nginx -t`
- Check Nginx error logs: `sudo tail -f /var/log/nginx/error.log`
- Make sure you reloaded Nginx: `sudo systemctl reload nginx`

### Uploads timing out?
- Increase the timeout values (300s = 5 minutes)
- Check backend logs to see if it's processing: `sudo journalctl -u atlas-backend -f`

### Need larger file size?
- Change `100M` to `200M` or `500M` as needed
- Keep in mind server disk space and memory limits

