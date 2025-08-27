# MechLocator Production Deployment Guide

## 🚀 Production-Ready Configuration

This guide will help you deploy MechLocator to production with proper Google Maps API configuration and security settings.

## 📋 Prerequisites

- Python 3.8+ installed
- PostgreSQL or MySQL database (recommended for production)
- Web server (Nginx/Apache)
- SSL certificate
- Google Cloud Platform account

## 🔧 Google Maps API Setup

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable billing for the project

### 2. Enable Required APIs

Enable these APIs in your Google Cloud Console:

```bash
# Maps JavaScript API
# Places API
# Geocoding API
# Distance Matrix API (optional)
```

### 3. Create API Key

1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **API Key**
3. Copy the generated API key

### 4. Restrict API Key (CRITICAL for Production)

**Never use an unrestricted API key in production!**

1. Click on your API key to edit it
2. Under **Application restrictions**, select:
   - **HTTP referrers (web sites)** for web applications
   - **IP addresses** for server-side applications
3. Add your domain(s):
   ```
   https://yourdomain.com/*
   https://www.yourdomain.com/*
   ```
4. Under **API restrictions**, select:
   - **Restrict key**
   - Select only the APIs you need:
     - Maps JavaScript API
     - Places API
     - Geocoding API

### 5. Set Usage Limits

1. Go to **APIs & Services** > **Quotas**
2. Set daily limits for each API:
   - Maps JavaScript API: 10,000 requests/day
   - Places API: 1,000 requests/day
   - Geocoding API: 2,500 requests/day

## 🔐 Environment Configuration

### 1. Create Production .env File

```bash
# Django Settings
SECRET_KEY=your-super-secret-production-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (PostgreSQL recommended)
DATABASE_URL=postgresql://user:password@localhost:5432/mechlocator

# Google Maps API
GOOGLE_MAPS_API_KEY=your-restricted-production-api-key

# Email Configuration
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=MechLocator <noreply@yourdomain.com>

# Security Settings
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

### 2. Update Settings for Production

Add these security settings to `mechlocator/settings.py`:

```python
# Production Security Settings
if not DEBUG:
    # HTTPS Settings
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # Cookie Security
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    SESSION_COOKIE_HTTPONLY = True
    
    # Security Headers
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # X-Frame-Options
    X_FRAME_OPTIONS = 'DENY'
    
    # Content Security Policy
    CSP_DEFAULT_SRC = ("'self'",)
    CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com")
    CSP_SCRIPT_SRC = ("'self'", "https://maps.googleapis.com", "https://maps.gstatic.com")
    CSP_IMG_SRC = ("'self'", "data:", "https://maps.googleapis.com", "https://maps.gstatic.com")
    CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com")
```

## 🗄️ Database Setup

### PostgreSQL (Recommended)

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE mechlocator;
CREATE USER mechlocator_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE mechlocator TO mechlocator_user;
\q

# Install psycopg2
pip install psycopg2-binary
```

Update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mechlocator',
        'USER': 'mechlocator_user',
        'PASSWORD': 'your_secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🚀 Deployment Steps

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install python3 python3-pip python3-venv nginx postgresql

# Create application directory
sudo mkdir -p /var/www/mechlocator
sudo chown $USER:$USER /var/www/mechlocator
```

### 2. Application Deployment

```bash
# Clone repository
cd /var/www/mechlocator
git clone https://github.com/yourusername/mechlocator.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with production values

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser
```

### 3. Gunicorn Setup

```bash
# Install Gunicorn
pip install gunicorn

# Create systemd service
sudo nano /etc/systemd/system/mechlocator.service
```

Add this content:

```ini
[Unit]
Description=MechLocator Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/mechlocator
ExecStart=/var/www/mechlocator/venv/bin/gunicorn --workers 3 --bind unix:/var/www/mechlocator/mechlocator.sock mechlocator.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

### 4. Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/mechlocator
```

Add this configuration:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;
    
    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Static files
    location /static/ {
        alias /var/www/mechlocator/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /var/www/mechlocator/media/;
        expires 1y;
        add_header Cache-Control "public";
    }

    # Proxy to Gunicorn
    location / {
        proxy_pass http://unix:/var/www/mechlocator/mechlocator.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 5. Enable Services

```bash
# Enable and start services
sudo systemctl enable mechlocator
sudo systemctl start mechlocator
sudo ln -s /etc/nginx/sites-available/mechlocator /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

## 🔍 Monitoring & Maintenance

### 1. Log Monitoring

```bash
# View application logs
sudo journalctl -u mechlocator -f

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 2. Database Backups

```bash
# Create backup script
sudo nano /usr/local/bin/backup_mechlocator.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/mechlocator"
mkdir -p $BACKUP_DIR

# Database backup
pg_dump mechlocator > $BACKUP_DIR/db_backup_$DATE.sql

# Media files backup
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz /var/www/mechlocator/media/

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

### 3. SSL Certificate Renewal

If using Let's Encrypt:

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Set up auto-renewal
sudo crontab -e
# Add this line:
0 12 * * * /usr/bin/certbot renew --quiet
```

## 🛡️ Security Checklist

- [ ] API key is restricted to your domain
- [ ] HTTPS is enabled and redirecting HTTP
- [ ] DEBUG is set to False
- [ ] Secret key is changed from default
- [ ] Database uses strong password
- [ ] Static files are served securely
- [ ] Security headers are configured
- [ ] Regular backups are scheduled
- [ ] SSL certificate is valid and auto-renewing
- [ ] Firewall is configured
- [ ] Server is updated regularly

## 📊 Performance Optimization

### 1. Database Optimization

```python
# Add to settings.py
DATABASES = {
    'default': {
        # ... existing config ...
        'OPTIONS': {
            'MAX_CONNS': 20,
            'CONN_MAX_AGE': 600,
        }
    }
}
```

### 2. Caching

```python
# Add Redis caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### 3. CDN for Static Files

Consider using a CDN like Cloudflare or AWS CloudFront for static files.

## 🚨 Troubleshooting

### Common Issues

1. **Google Maps not loading**: Check API key restrictions and billing
2. **500 errors**: Check application logs and database connectivity
3. **Static files not loading**: Verify collectstatic was run and Nginx configuration
4. **SSL errors**: Verify certificate paths and permissions

### Useful Commands

```bash
# Check service status
sudo systemctl status mechlocator

# Restart services
sudo systemctl restart mechlocator
sudo systemctl restart nginx

# Check Nginx configuration
sudo nginx -t

# View real-time logs
sudo tail -f /var/log/nginx/error.log
```

## 📞 Support

For issues related to:
- **Google Maps API**: Check [Google Cloud Console](https://console.cloud.google.com/)
- **Django**: Check [Django Documentation](https://docs.djangoproject.com/)
- **Deployment**: Check server logs and this guide

---

**Remember**: Always test your deployment in a staging environment first!
