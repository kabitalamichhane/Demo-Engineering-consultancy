# SEO guide — getting Highnoon found on Google (free)

The website code is already prepared. These steps are what you (or the client) do **after the site is live**
on its real domain. Everything here is free.

## What the code already does

* A unique page title + description for every page (services, projects, updates and jobs are editable in Admin → *SEO* box).
* Share preview (Facebook / WhatsApp / Google) with a picture, title and description.
* Company, service, news-article and job data in the format Google reads (schema.org), plus breadcrumbs.
* `sitemap.xml` (every real page, no demo projects) and `robots.txt`.
* Demo projects are hidden from Google automatically (`noindex`).
* Alt text for pictures: *Image description* boxes on services, projects and updates.

## One-time setup (about 1 hour)

1. **Run the new migration** (once, on your computer and on the server):
   `python manage.py makemigrations company services projects updates` then `python manage.py migrate`.
2. **Admin → Company Profile → "Google & Sharing (SEO)"**
   * *Share image*: upload a photo of 1200 x 630 px (a good building / workshop photo with the logo). 
   * *Latitude / Longitude*: right-click the office on Google Maps and copy the two numbers.
   * *Opening hours*: for example `Su-Fr 09:00-17:00`.
3. **Google Business Profile** (https://business.google.com) — the most important step for local search.
   Use exactly the same name, address and phone as the website. Add photos and the website link.
   Google will post a postcard or call to verify the business. Then copy:
   * the Google Maps link → *Google Business Profile / Maps link*
   * the "Ask for reviews" link → *Google review link* (a "Review us on Google" link then appears in the footer)
4. **Google Search Console** (https://search.google.com/search-console) → add the domain → choose *HTML tag*
   verification → paste only the code into *Google site verification* in Admin → press *Verify*.
   Then open *Sitemaps* and submit `sitemap.xml`.
5. **Bing Webmaster Tools** (optional, https://www.bing.com/webmasters) — same idea, you can import from Search Console.
6. Check a page in https://search.google.com/test/rich-results to see the company / service data is read.
7. Test the share preview: paste a page link into WhatsApp or Facebook's Sharing Debugger.

## Every month (15–30 minutes)

* Add **one new project or update** in Admin (real photos, 100+ words, mention *Pokhara* and the service).
* Ask each finished client to leave a **Google review** (send them the review link on WhatsApp).
* Open Search Console → *Performance*: which searches bring visitors, which pages get no clicks.
* Fix anything under *Pages* or *Sitemaps* that shows an error.
* Answer new reviews on Google Business Profile.

## Writing tips that really matter

* One service = one page. Describe it in plain words: what it is, who it is for, where you work, sample projects.
* Use the words customers search: *metal fabrication Pokhara*, *steel gate*, *roof truss*, *construction company Pokhara*.
* Fill the *SEO title* (under 60 characters) and *SEO description* (under 155 characters) for the main services.
* Describe each photo in the *Image description* box.
* Use the same business name, address and phone everywhere (Facebook, Google, directories).
* Never buy backlinks or "rank #1" packages.

## Expect

Google needs time. New sites usually start to appear in 2–6 weeks and improve over 3–6 months, faster for local
searches when the Google Business Profile has photos and reviews.
