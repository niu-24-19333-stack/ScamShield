# ===========================================
# ScamShield Frontend
# ===========================================

Static frontend for ScamShield web application.

## Structure

```
public/
├── assets/          # Images, icons, fonts
│   └── favicon.svg
├── css/             # Stylesheets
│   ├── style.css    # Global styles
│   ├── home.css     # Homepage styles
│   ├── pages.css    # Common page styles
│   └── dashboard.css # Dashboard styles
├── js/              # JavaScript
│   ├── main.js      # Global scripts
│   ├── auth.js      # Authentication
│   ├── api.js       # API client
│   └── dashboard.js # Dashboard logic
├── index.html       # Landing page
├── login.html       # Login page
├── signup.html      # Registration page
├── dashboard.html   # User dashboard
├── contact.html     # Contact page
├── admin.html       # Admin panel
├── 404.html         # Error page
└── 50x.html         # Server error page
```

## Development

Serve the `public` folder with any static file server:

```bash
# Python
cd public
python -m http.server 5500

# Node.js
npx serve public

# VS Code Live Server
# Right-click index.html -> Open with Live Server
```

## Building for Production

The frontend is served via Nginx in Docker. The `Dockerfile` copies the `public/` folder to nginx's html directory.

```bash
docker build -t scamshield-frontend .
docker run -p 80:80 scamshield-frontend
```

## API Configuration

The frontend expects the API at `/api/`. In development, configure a proxy or update `js/api.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000/api/v1';
```
