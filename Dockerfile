# Use nginx to serve static files
FROM nginx:alpine

# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy website files
COPY . /usr/share/nginx/html/

# Custom nginx config with gzip compression and SPA routing
RUN cat > /etc/nginx/conf.d/default.conf << 'NGINX_CONF'
server {
    listen 8080;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;
    charset utf-8;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_min_length 256;
    gzip_types
        text/plain
        text/css
        text/javascript
        text/xml
        application/json
        application/javascript
        application/xml
        application/xml+rss
        application/xhtml+xml
        image/svg+xml
        font/woff
        font/woff2
        application/font-woff
        application/font-woff2;

    location / {
        try_files $uri $uri.html $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2|webp)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
NGINX_CONF

# Expose port 8080 (Cloud Run requirement)
EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
