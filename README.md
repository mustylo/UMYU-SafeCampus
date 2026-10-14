# UMYU SafeCampus

Secure Flask prototype for campus reports, role-scoped workflows, Lost & Found, safety alerts and a local phishing analyzer.

## Windows setup

1. Open PowerShell in this folder and run `py -m venv .venv`.
2. Run `.\.venv\Scripts\Activate.ps1` then `py -m pip install -r requirements.txt`.
3. Copy `.env.example` to `.env`; set a long random `SECRET_KEY` and your local PostgreSQL `DATABASE_URL`.
4. Run `flask --app run.py db upgrade`, then `flask --app run.py seed-catalog`, then `flask --app run.py run`.
5. Run tests with `pytest`.

The analyzer never fetches submitted URLs. Use a production WSGI server, HTTPS, a managed database and `FLASK_ENV=production` for deployment.

## Demo seed guidance

`flask --app run.py seed-catalog` safely creates only missing departments and categories; it does not remove records. Run it first on a development database and review production changes before using it there.
