# PythonAnywhere Deployment Guide

## Goal

Deploy BookScope API to a public PythonAnywhere URL so the coursework includes an external deployment.

Expected final URL:

- `https://YOUR_PYTHONANYWHERE_USERNAME.pythonanywhere.com/`

## 1. Create the web app

On PythonAnywhere:

1. Open the `Web` tab.
2. Click `Add a new web app`.
3. Choose `Manual configuration`.
4. Choose the Python version that matches the virtualenv you will create.

PythonAnywhere's official Django deployment guide says to use a manual web app, configure a virtualenv, and edit the platform WSGI file from the Web tab rather than your project's own `bookscope/wsgi.py`.

## 2. Clone the repository

In a PythonAnywhere Bash console:

```bash
cd ~
git clone https://github.com/IJF9GAWHY8FGA8/bookscope-api.git
cd bookscope-api
```

## 3. Create a virtualenv and install requirements

Example using Python 3.10:

```bash
mkvirtualenv bookscope-api --python=/usr/bin/python3.10
workon bookscope-api
pip install -r requirements.txt
```

Then, in the `Web` tab, set the virtualenv for the web app to:

```text
/home/YOUR_PYTHONANYWHERE_USERNAME/.virtualenvs/bookscope-api
```

## 4. Create the production `.env`

Create a `.env` file in `/home/YOUR_PYTHONANYWHERE_USERNAME/bookscope-api/.env`:

```bash
cat > .env <<'EOF'
DJANGO_SECRET_KEY=replace-with-a-long-random-secret
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=YOUR_PYTHONANYWHERE_USERNAME.pythonanywhere.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://YOUR_PYTHONANYWHERE_USERNAME.pythonanywhere.com
GOOGLE_BOOKS_API_KEY=
EOF
```

If you want these variables available in Bash after `workon`, add this to the virtualenv `postactivate` script:

```bash
echo 'set -a; source ~/bookscope-api/.env; set +a' >> ~/.virtualenvs/bookscope-api/bin/postactivate
```

Then reactivate the virtualenv:

```bash
deactivate
workon bookscope-api
```

## 5. Configure the WSGI file

PythonAnywhere does **not** use your project `bookscope/wsgi.py` directly for web app setup. You need to edit the WSGI file linked from the `Code` section of the `Web` tab, typically:

```text
/var/www/YOUR_PYTHONANYWHERE_USERNAME_pythonanywhere_com_wsgi.py
```

Replace its contents with the repository template from:

- `deployment/pythonanywhere_wsgi.py`

Required substitutions:

- `YOUR_PYTHONANYWHERE_USERNAME`

## 6. Run migrations and collect static files

From a Bash console:

```bash
cd ~/bookscope-api
workon bookscope-api
python manage.py migrate
python manage.py collectstatic --noinput
```

## 7. Configure static and media mappings

In the `Static Files` section of the `Web` tab, add:

- URL: `/static/`
- Directory: `/home/YOUR_PYTHONANYWHERE_USERNAME/bookscope-api/staticfiles`

Optional media mapping:

- URL: `/media/`
- Directory: `/home/YOUR_PYTHONANYWHERE_USERNAME/bookscope-api/media`

## 8. Reload and verify

Click `Reload` on the `Web` tab.

Then open:

- `https://YOUR_PYTHONANYWHERE_USERNAME.pythonanywhere.com/api/health/`
- `https://YOUR_PYTHONANYWHERE_USERNAME.pythonanywhere.com/api/docs/`
- `https://YOUR_PYTHONANYWHERE_USERNAME.pythonanywhere.com/admin/`

Expected health response:

```json
{
  "status": "ok",
  "service": "bookscope-api"
}
```

## 9. Optional sample data import

```bash
cd ~/bookscope-api
workon bookscope-api
python manage.py import_google_books --input-file data/samples/google_books_raw_sample.json
```

## 10. What to update after deployment succeeds

Update these files with your real public URL:

- `README.md`
- `docs/technical_report.md`
- `slides/bookscope_presentation_outline.md` if needed

Also mention the live URL during the oral presentation.
