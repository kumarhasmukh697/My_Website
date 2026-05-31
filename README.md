# Hasmukh Portfolio Website

**Project**
- **Name**: Hasmukh Portfolio Website
- **Description**: A personal portfolio site built with Django to showcase projects, skills, resume, and provide a contact form. Projects and their image galleries are stored in the `mywebsite` app and served from the `media/` directory.

**Demo / Local Preview**
- Runs locally with Django's development server: `python manage.py runserver`

**Features**
- **Projects**: List of projects with images and short descriptions (model: `Project`).
- **Project details**: Detail page with an image gallery (model: `ImageGallary`).
- **Contact form**: Sends email via configured SMTP settings.
- **Static assets**: Uses Bootstrap, AOS, Glightbox, Swiper and other static libraries included in `static/assets`.
- **Resume & Skills**: Static sections listing education, experience and technical skills.

**Tech Stack**
- **Backend**: Django 6.0.4
- **Python**: 3.12 (recommended)
- **Database**: SQLite (default), configurable via env vars
- **Image handling**: Pillow
- **Env management**: python-dotenv

**Quick Start (Local)**

1. Create a virtual environment and activate it

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create `.env` based on the sample in the repo and fill values (see "Environment variables" below).

4. Run migrations and create a superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

5. (Optional) Collect static files

```bash
python manage.py collectstatic --noinput
```

6. Start the development server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ to view the site.

**Environment variables (.env)**
- `DJANGO_SECRET_KEY` — Django secret key (REQUIRED in production)
- `DJANGO_DEBUG` — `True` or `False` (use `False` in production)
- `DJANGO_ALLOWED_HOSTS` — comma-separated hosts (e.g. `localhost,127.0.0.1`)
- `DJANGO_DB_ENGINE` — Django DB engine (default `django.db.backends.sqlite3`)
- `DB_NAME` — DB name or sqlite filename (default `db.sqlite3`)
- `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` — DB credentials for non-sqlite setups
- `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` — email/smtp configuration for contact form

The repository already contains a `.env` example with placeholders. Keep that file out of version control.

**Media & Static**
- Uploaded project images are stored in `media/project_images/`.
- Static assets (CSS, JS, images) live under `static/assets/` and are served by Django in development.

**Database**
- Default: SQLite (file `db.sqlite3`). For production, change `DJANGO_DB_ENGINE` to a production-ready engine (e.g. PostgreSQL) and set `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`.

**Deployment Notes**
- Set `DJANGO_DEBUG=False` and configure `DJANGO_SECRET_KEY` and `DJANGO_ALLOWED_HOSTS` for your domain.
- Use a WSGI server like Gunicorn or an ASGI server behind a reverse proxy.
- Serve static files via a CDN or web server (e.g., nginx) after running `collectstatic`.
- Configure media file storage (S3 or equivalent) if you expect user uploads in production.

**Contributing**
- Feel free to open issues or PRs. For local changes, follow the Quick Start steps, add tests, and submit a PR.

**License**
- MIT License — feel free to change this to another license if you prefer.

**Contact**
- Owner: Hasmukh Kumar
- Email: Kumarhasmukh697@gmail.com


---


