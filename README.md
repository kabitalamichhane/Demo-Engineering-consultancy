# Highnoon Engineering Solutions Pvt. Ltd. — Corporate Website

A full-stack Django + Django REST Framework corporate website for **Highnoon
Engineering Solutions Pvt. Ltd.**, an engineering, construction, infrastructure
and metal fabrication company based in Pokhara, Nepal.

> Design and structure are original work inspired only by the general
> category of professional engineering/construction company websites. No
> text, images, logos, branding or code were copied from any third-party site.

---

## 1. Features

- Public site: Home, About Us, Services (incl. a dedicated Metal Fabrication
  page), Projects, Updates (news), Careers, **Work With Us** (B2B/partnership
  page, separate from Careers), Contact Us, Get a Quote.
- Every piece of company information (address, phone, email, hero content,
  services, projects, statistics, clients) is editable from **Django Admin**
  — no code changes required.
- Django REST Framework API with JWT authentication, filtering, search,
  pagination and Swagger/ReDoc documentation.
- SEO: per-page meta title/description, Open Graph tags, canonical URLs,
  `sitemap.xml`, `robots.txt`, semantic HTML, image alt text, JSON-LD.
- Responsive, animated, premium engineering-company design (navy/charcoal,
  white, gray, amber accent) — desktop, tablet and mobile.
- Private inquiry data (contact messages, quote requests, work-with-us
  inquiries, job applications, appointments) is **not** publicly readable.

## 2. Project Structure

```
highnoon/
├── manage.py
├── requirements.txt
├── .env.example
├── highnoon/          # Project settings, urls, sitemaps, robots.txt
├── company/           # CompanyProfile, Statistic, Client + Home/About views
├── services/          # Service model + service pages (incl. metal-fabrication)
├── projects/          # Project, ProjectImage
├── updates/           # Update (news/blog)
├── careers/           # Job, JobApplication
├── inquiries/         # ContactInquiry, QuoteRequest, WorkWithUsInquiry, Appointment
├── api/                # DRF serializers, viewsets, permissions, routers, urls
├── templates/          # All HTML templates (base, includes, per-app pages)
├── static/             # css/style.css, js/main.js, img/
└── media/              # User-uploaded files (created at runtime)
```

## 3. Local Setup

### 3.1 Prerequisites
- Python 3.11+ (project developed against 3.12)
- pip / virtualenv

### 3.2 Installation

```bash
cd highnoon
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env            # then edit .env with real values
```

### 3.3 Database migrations

```bash
python manage.py makemigrations company services projects updates careers inquiries
python manage.py migrate
```

### 3.4 Create an admin user

```bash
python manage.py createsuperuser
```

### 3.5 Seed initial content (optional but recommended)

Creates the CompanyProfile row (with the values in this brief), the 11
initial service categories, and a small set of **clearly marked demo
projects** (`is_demo=True`) for local development/preview only:

```bash
python manage.py seed_demo_data
```

Remove or replace the demo projects from Django Admin before going live.

### 3.6 Run the development server

```bash
python manage.py runserver
```

- Website: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/hes-control-panel/ (the ADMIN_URL from your `.env`; without a `.env` it is /admin/)
- API root (browsable): http://127.0.0.1:8000/api/
- Swagger UI: http://127.0.0.1:8000/api/docs/
- ReDoc: http://127.0.0.1:8000/api/redoc/
- Sitemap: http://127.0.0.1:8000/sitemap.xml
- robots.txt: http://127.0.0.1:8000/robots.txt

### 3.7 Static & media files in production

```bash
python manage.py collectstatic
```
Serve `staticfiles/` and `media/` via your web server (Nginx, WhiteNoise, or
a CDN/S3-compatible bucket) in production. `DEBUG=False` disables Django's
own static/media serving.

## 4. Admin-Editable Content

Everything below is managed from **Django Admin** without touching code:

| Model              | What it controls                                              |
|---------------------|-----------------------------------------------------------------|
| `CompanyProfile`    | Name, tagline, address, phone, email, hero section, logo, SEO defaults, social links |
| `Statistic`         | Homepage/About counters                                        |
| `Client`            | Client/partner logos                                           |
| `Service`           | All services, incl. Metal Fabrication                          |
| `Project`, `ProjectImage` | Portfolio, categories, status, gallery                    |
| `Update`            | News / announcements                                            |
| `Job`               | Job openings                                                    |
| `ContactInquiry`, `QuoteRequest`, `WorkWithUsInquiry`, `Appointment`, `JobApplication` | Read-only submission records for staff review |

`CompanyProfile` is enforced as a singleton — only one row can exist, and it
is auto-created on first request if missing.

## 5. API Overview

Base path: `/api/`

| Endpoint | Method(s) | Access |
|---|---|---|
| `/api/services/` | GET (list/detail), POST/PUT/PATCH/DELETE | Public read, staff write |
| `/api/projects/` | GET, POST/PUT/PATCH/DELETE | Public read, staff write |
| `/api/updates/` | GET, POST/PUT/PATCH/DELETE | Public read (published only), staff write |
| `/api/clients/` | GET, POST/PUT/PATCH/DELETE | Public read (active only), staff write |
| `/api/statistics/` | GET, POST/PUT/PATCH/DELETE | Public read, staff write |
| `/api/jobs/` | GET, POST/PUT/PATCH/DELETE | Public read (active only), staff write |
| `/api/company-profile/` | GET | Public |
| `/api/contact/` | POST (create), GET/PATCH/DELETE | Public create, staff-only read/manage |
| `/api/quotes/` | POST, GET/PATCH/DELETE | Public create, staff-only read/manage |
| `/api/work-with-us/` | POST, GET/PATCH/DELETE | Public create, staff-only read/manage |
| `/api/appointments/` | POST, GET/PATCH/DELETE | Public create, staff-only read/manage |
| `/api/job-applications/` | POST, GET/PATCH/DELETE | Public create, staff-only read/manage |
| `/api/auth/token/` | POST | Obtain JWT access/refresh token pair |
| `/api/auth/token/refresh/` | POST | Refresh JWT access token |

All list endpoints support pagination (`?page=`), search (`?search=`) and
ordering (`?ordering=`); filterable endpoints also support field filters
(e.g. `/api/projects/?category=metal_fabrication&status=completed`).

Full interactive documentation: `/api/docs/` (Swagger) and `/api/redoc/`.

### Example: obtaining a JWT token

```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your-password"}'
```

### Example: submitting a Work With Us inquiry

```bash
curl -X POST http://127.0.0.1:8000/api/work-with-us/ \
  -H "Content-Type: application/json" \
  -d '{
        "full_name": "Jane Contractor",
        "company_name": "ABC Builders",
        "email": "jane@example.com",
        "phone": "9800000000",
        "organization_type": "contractor",
        "project_type": "Industrial Shed",
        "project_location": "Pokhara",
        "message": "Interested in partnering on an upcoming project."
      }'
```

## 6. Running Tests

```bash
python manage.py test
```

Covers: CompanyProfile singleton behaviour, home/about pages, service pages
(including the metal-fabrication landing page and inactive-service 404
handling), project listing/filtering, contact/work-with-us form submissions,
and public-vs-authenticated API access rules.

## 7. SEO Notes

- Global defaults come from `CompanyProfile.default_seo_title` /
  `default_seo_description`; every `Service` and `Project` can override
  these individually via their own `seo_title` / `seo_description` fields.
- The phrase **"Metal Fabrication Company in Pokhara, Nepal"** is used as
  the SEO title of `/services/metal-fabrication/` and appears naturally in
  its content — it is not repeated elsewhere as keyword stuffing.
- `sitemap.xml` and `robots.txt` are generated dynamically from live data.

## 8. Notes on Demo Data

Per the brief, no fabricated real-world project claims (client names,
project counts, years of operation) are hard-coded anywhere in the
templates or seed data. The `seed_demo_data` management command creates a
small number of **clearly flagged** (`is_demo=True`) placeholder projects
for local development/preview only — replace or delete them via Django
Admin before deploying to production.

## 9. Security

No website is "unhackable". This project makes attacks hard, limits the damage if
one succeeds, and records suspicious activity. Some parts must be done on the
server — see the checklist at the end.

### 9.1 What the code does

| Protection | Where |
|---|---|
| SQL injection / XSS / CSRF | Django ORM, template auto-escaping, CSRF middleware |
| **Login lockout** — 5 failed logins blocks the IP for 1 hour (admin **and** `/api/auth/token/`) | `django-axes` (`AXES_*` in settings) |
| **Admin two-factor auth** (authenticator app + backup codes) | `django-otp`, `ADMIN_REQUIRE_2FA` |
| **Custom admin URL** (not `/admin/`), hidden from `robots.txt` | `ADMIN_URL` |
| **Content-Security-Policy**, Permissions-Policy, COOP, X-Frame-Options, nosniff | `company/security_middleware.py` |
| **Private uploads** — CVs and quote attachments are stored outside the public media folder and downloadable only by logged-in staff | `PRIVATE_MEDIA_ROOT`, `/private-files/` view |
| **Upload validation** (size, extension **and real file content**) on web forms **and** API | `company/security.py` |
| Honeypot spam trap + per-IP rate limit on every public form | `company/security.py` |
| API throttling: 5 submissions/hour/IP on public POST endpoints | `api/throttles.py` |
| Spoof-proof client IP (`X-Forwarded-For` ignored unless `TRUSTED_PROXY_COUNT` is set) | `get_client_ip()` |
| Applications to inactive jobs rejected via API | `api/serializers.py` |
| Swagger/ReDoc and the browsable API disabled in production | `ENABLE_API_DOCS`, `DEBUG` |
| JWT: 30-min access tokens, refresh tokens rotate and are blacklisted | `SIMPLE_JWT` |
| 12-character minimum password length | `AUTH_PASSWORD_VALIDATORS` |
| **App refuses to start in production** with the default secret key or without explicit allowed hosts | `settings.py` |
| Security log (lockouts, rate limits, honeypot hits, private downloads) | `logs/security.log` |

### 9.2 One-time setup after pulling these changes

```bash
pip install -r requirements.txt
python manage.py makemigrations company inquiries careers
python manage.py migrate
python manage.py test
```

### 9.3 Enable admin 2FA

Do this **before** setting `ADMIN_REQUIRE_2FA=True` (it is automatically on when `DJANGO_DEBUG=False`):

```bash
python manage.py setup_admin_2fa YOUR_USERNAME
```

Add the printed key to Google/Microsoft Authenticator or Authy ("enter a setup key",
time-based) and store the backup codes safely. Repeat for every staff account.
Lost your device? An admin with shell access runs the command again with `--reset`.

### 9.4 Production configuration (`.env`)

```
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=<50+ random characters>
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
ADMIN_URL=<something-only-you-know>
TRUSTED_PROXY_COUNT=1          # 1 for Nginx, 2 for Cloudflare + Nginx
DJANGO_BEHIND_PROXY_SSL=True   # if Nginx/Cloudflare terminates HTTPS
DJANGO_HSTS_SECONDS=31536000   # after HTTPS is confirmed working
CSRF_TRUSTED_ORIGINS=https://yourdomain.com
```

Then run `python manage.py check --deploy` and fix every warning it reports.

### 9.5 Server checklist (cannot be done in code)

- [ ] HTTPS certificate (Let's Encrypt or Cloudflare); put Cloudflare in front for DDoS/WAF
- [ ] Run Gunicorn behind Nginx — never `runserver`
- [ ] Nginx must **not** serve `private_media/`, `logs/`, `.env` or `db.sqlite3`; serve only `/static/` and `/media/`
- [ ] Nginx: `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;` and `X-Forwarded-Proto`
- [ ] PostgreSQL with a dedicated low-privilege database user
- [ ] Shared cache (Redis) if running more than one worker, so rate limits and lockouts are shared
- [ ] SSH keys only, firewall (80/443/SSH), Fail2ban, automatic OS security updates
- [ ] Automated off-server backups of the database, `media/` and `private_media/` — test a restore
- [ ] Monthly: `pip install -U -r requirements.txt`, then `pip install -r requirements-dev.txt && pip-audit`
- [ ] Quarterly: review staff accounts; each person gets their own account with minimal permissions
- [ ] Watch `logs/security.log` (or ship it to Sentry/your log tool) for repeated lockouts

## 10. License / Ownership

All source code in this repository was written for Highnoon Engineering
Solutions Pvt. Ltd. and may be modified, extended and deployed by the
company as needed.
