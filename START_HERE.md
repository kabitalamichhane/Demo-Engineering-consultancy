# START HERE — Highnoon Engineering Solutions website (Windows)

Extract this zip into a **new, empty folder**, open PowerShell inside the `highnoon` folder
(the one that contains `manage.py`) and run these commands one by one.

```powershell
python -m venv myenv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
myenv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt

copy .env.example .env

python manage.py makemigrations company services projects updates careers inquiries   # run again after every update that adds fields
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo_data      # services, stats, director messages AND your 4 project photos
python manage.py runserver
```

* Website: http://127.0.0.1:8000/
* Admin panel: http://127.0.0.1:8000/hes-control-panel/   (set by `ADMIN_URL` in `.env`;
  change the word, or delete the line to use /admin/)
* Admin password must be at least 12 characters.
* API documentation (development only): http://127.0.0.1:8000/api/docs/

## After the first login — fill in your content (Admin)

1. **Company Settings → Company Profile**
   * Logo and Favicon (your round Highnoon logo)
   * Homepage Hero → upload a large engineering/construction photo as *Hero image*
   * Director's Message → name, designation, photo, quote (the sample photo is used until you upload one)
   * Social Media → Facebook is pre-set; add LinkedIn/Instagram/YouTube if you have them
   * Admin → *Director messages* → add the director's own message(s); none are created automatically
   * Featured Building Showcase → a high-resolution photo, title, caption
   * Address, phone, email, map embed URL, social links
2. **Services** → edit the 11 seeded services (add photos, descriptions, features)
3. **Projects** → rename the 4 photo projects (real name, location, description), add more (featured image, gallery, tick *Featured*)
4. **Clients, Statistics, Updates, Jobs** → add real entries only

## Check everything works

```powershell
python manage.py test
```

## Before going live

Follow the security checklist in `README.md` (section 9): `DJANGO_DEBUG=False`, a real secret key,
real domain in `DJANGO_ALLOWED_HOSTS`, HTTPS, admin two-factor login
(`python manage.py setup_admin_2fa YOUR_USERNAME`), backups, and `python manage.py check --deploy`.

If any command prints an error, copy the last 15 lines of the error and send them to me.

## Sales features (WhatsApp, email alerts, lead tracker)

* **WhatsApp / Viber buttons:** Admin → Company Profile → *Chat Buttons*. WhatsApp uses the main phone number
  until you type a different one (digits with country code, e.g. 9779856082231). Viber is hidden until a number is set.
* **Email alerts:** every new quote / contact / work-with-us submission emails `COMPANY_NOTIFY_EMAIL`
  (Reply-To is the customer) and sends the customer a short acknowledgement. To send REAL emails, set in `.env`:
  `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend` and a Gmail *App password* in `EMAIL_HOST_PASSWORD`.
  Until then emails only print in the terminal. Turn the customer reply off with `SEND_AUTO_REPLY=False`.
* **Lead tracker:** Admin → Quote Requests / Contact Inquiries / Work With Us. Each lead has a stage
  (New → Contacted → Quote Sent → Won / Lost), assignee, follow-up date, deal value and private notes.
  Use the *follow-up* filter (Overdue / Due today) and the bulk actions on the list page.

## Monitoring & error alerts

* **Health page:** `https://yourdomain.com/health/` returns `{"status": "ok"}` (or HTTP 503 if the database is down).
  Point your uptime monitor at this address (check every 1–5 minutes).
* **Error emails:** when `DJANGO_DEBUG=False` and real SMTP email is configured, every server error (500)
  is emailed to `ERROR_EMAIL_TO`. Turn off with `SEND_ERROR_EMAILS=False`.

## Language switcher (English / Nepali / Hindi) — built in, no Google

The top bar has EN / नेपाली / हिन्दी buttons. The Nepali and Hindi text is **part of the website** (`company/i18n_data/`),
so it works on your computer, on the live site, offline and behind any firewall.

* **Standard text** (menus, buttons, forms, headings, the starter services, chatbot answers, director message) is already translated.
* **Text you type in Admin** (a new service, project, news article, job...) stays English until you add its translation:
  **Admin → Translations → Add** → paste the English text exactly as shown on the page, then type the Nepali and/or Hindi.
  An empty box means that language shows English. Capital letters do not matter. Admin entries override the built-in ones,
  so you can also improve any built-in wording there.
* **Add text to the code instead:** edit `company/i18n_data/ui.py`, `pages.py` or `content.py` (`'English': ('Nepali', 'Hindi')`).
  `python manage.py missing_translations` lists template text that still has no translation.
* Hide the switcher with `ENABLE_LANGUAGE_SWITCHER=False` in `.env`.
* A reader's choice is remembered in a cookie (`hes_lang`). Search engines always see the English page.
* Names, addresses, phone numbers, dates and prices are not translated.

If a button seems to do nothing: press **Ctrl + F5** once (the browser may hold an old copy of the script), then run `python manage.py site_status`.

## FAQ chatbot

A "Ask us" button (bottom-right) opens an automated assistant that answers from **Admin → Chatbot questions**
(no outside service, no cost). If it cannot answer it offers *Request a call back* (saved as a Contact Inquiry and
emailed to you), WhatsApp and the quote form. `python manage.py seed_demo_data` adds 7 starter answers using only
facts already on the site — review and edit them in Admin before the client sees the site. Add Nepali/Hindi
keywords to a question so people can ask in those languages too.

## SEO (free) — found on Google

The site now has per-page titles, share previews, schema data, a complete sitemap and image description boxes.
After you add these new fields, create and run the migration once:

```powershell
python manage.py makemigrations company services projects updates
python manage.py migrate
python manage.py test
```

Then follow **`SEO_GUIDE.md`** (Google Business Profile, Search Console, reviews, monthly routine).
Admin → Company Profile → *Google & Sharing (SEO)* holds the share image, map link, review link and verification code.

## Updating the project WITHOUT losing your Admin data

Everything you type in Admin (director messages, projects, photos, FAQs, leads) is stored in two places inside the
project folder: **`db.sqlite3`** and the **`media`** folder. They are NOT inside the zip, so:

* When you get a new zip, **unzip it over the same folder** (choose "Replace files"). Never delete `db.sqlite3` or `media`.
  If you unzip into a NEW folder, copy `db.sqlite3` and `media` from the old folder into it first.
* After updating, run `python manage.py makemigrations` and `python manage.py migrate`.
* A fresh folder = an empty database = the director message, projects and FAQs are gone (this is why they "disappear").
* Starter director message on an empty database: `python manage.py add_director_message`
  (adds one only if there are none; edit it in Admin → Director messages, tick *Active*).

## Something not showing? Run the status check

```powershell
python manage.py site_status
```

It prints the database file in use, how many director messages are saved/active, and whether the director section
appears in the rendered home page. Send me the output if anything looks wrong.
