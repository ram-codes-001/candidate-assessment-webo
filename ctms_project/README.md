# CTMS — Clinical Trial Management System

A QA Assessment Platform built with Django 4.2. This application simulates a real-world Clinical Trial Management System and contains intentional bugs across multiple categories for QA evaluation purposes.

> **For assessment use only — not for production clinical data**

---

## Tech Stack

- **Backend**: Django 4.2.13, Python 3.11
- **Auth**: Django built-in auth with custom `CTMSUser` model (roles: Admin, Coordinator)
- **Database**: SQLite (default) — configurable via `DATABASE_URL`
- **Static files**: WhiteNoise 6.6.0
- **Server**: Gunicorn 21.2.0
- **Frontend**: AdminLTE 3, Bootstrap 5, DataTables, Flatpickr, SweetAlert2, Select2, Toastr
- **Config**: python-decouple 3.8
- **File uploads**: Pillow 10.3.0

---

## Login Credentials

| Role        | Email                      | Password   |
|-------------|----------------------------|------------|
| Admin       | admin@ctms.com             | Admin@123  |
| Coordinator | coordinator1@ctms.com      | Coord@123  |
| Coordinator | coordinator2@ctms.com      | Coord@123  |

---

## Quick Start

```bash
git clone <repo-url>
cd ctms_project
cp .env.example .env
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_users
python manage.py seed_data
python manage.py runserver
```

Then open [http://localhost:8000](http://localhost:8000).

---

## Deployment Options

### Option 1 — Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env as needed

# Run migrations and seed
python manage.py migrate
python manage.py seed_users
python manage.py seed_data

# Collect static files (optional for dev)
python manage.py collectstatic --noinput

# Start the dev server
python manage.py runserver
```

### Option 2 — Railway / Render

1. Push the `ctms_project/` directory to a GitHub repository.
2. Create a new project on [Railway](https://railway.app) or [Render](https://render.com) and connect the repo.
3. Set the following environment variables in the platform dashboard:

   ```
   SECRET_KEY=<generate a strong random key>
   DEBUG=False
   ALLOWED_HOSTS=<your-app-domain>
   DATABASE_URL=sqlite:///db.sqlite3
   ```

4. Set the **start command** to:

   ```
   gunicorn ctms.wsgi --log-file -
   ```

5. Add a **build command** (run once on deploy):

   ```
   python manage.py migrate --noinput && python manage.py seed_users && python manage.py seed_data && python manage.py collectstatic --noinput
   ```

6. Deploy — the platform will install `requirements.txt` automatically.

### Option 3 — Docker

```bash
# Build the image (runs migrate, seed, collectstatic at build time)
docker build -t ctms-app .

# Run the container
docker run -p 8000:8000 \
  -e SECRET_KEY=your-secret-key-here \
  -e DEBUG=False \
  -e ALLOWED_HOSTS=localhost \
  ctms-app
```

Then open [http://localhost:8000](http://localhost:8000).

To persist the SQLite database across container restarts, mount a volume:

```bash
docker run -p 8000:8000 \
  -e SECRET_KEY=your-secret-key-here \
  -e DEBUG=False \
  -e ALLOWED_HOSTS=localhost \
  -v $(pwd)/data:/app/data \
  ctms-app
```

---

## Project Structure

```
ctms_project/
├── ctms/               # Django project settings, URLs, WSGI
├── accounts/           # Custom user model, login/logout
├── patients/           # Patient CRUD + seed management commands
├── visits/             # Visit log CRUD
├── labs/               # Lab results CRUD
├── adverse_events/     # Adverse event CRUD
├── reports/            # Patient listing + CSV exports
├── audit/              # Audit trail log
├── templates/          # Global base, navbar, sidebar, dashboard
├── static/             # CSS and JS assets
├── requirements.txt
├── Procfile
├── Dockerfile
└── .env.example
```

---

> For assessment use only — not for production clinical data
