# BlogHive Frontend

This directory contains the static HTML/JS frontend for the BlogHive platform.

## How to Run

### 1. Start the Backend
The frontend relies on the Django backend to be running.
```powershell
# In the root directory
python manage.py runserver
```
The backend will be available at `http://127.0.0.1:8000`.

### 2. Start the Frontend
You can now run the frontend using npm:
```powershell
# In the blog_frontend directory
npm run dev
```
Alternatively, you can still use the Python server:
```powershell
python -m http.server 5500
```
The frontend will be accessible at `http://127.0.0.1:5500`.

### 3. Open in Browser
Visit [http://127.0.0.1:5500](http://127.0.0.1:5500) to view the application.

## Troubleshooting
- **CORS Errors**: Ensure that the Django backend has `django-cors-headers` installed and configured to allow requests from `http://127.0.0.1:5500`.
- **API URL**: If the backend is running on a different port, update the `API_BASE_URL` in `js/main.js`.
