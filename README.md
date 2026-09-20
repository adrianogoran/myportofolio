# Personal Portfolio

- **Name:** Goran Adriano Tamrella
- **NPM:** 2506558251
- **Class:** PBP KKI
- Semester 3 Portfolio project

## Setup to Access the Website

Requires Python 3.12+ and Git.


```

git clone https://github.com/adrianogoran/myportofolio.git
cd myportofolio
python -m venv env
.\env\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

```


The site runs at `http://127.0.0.1:8000/`.

### Assignment 1

1. Yes. I used `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, and `<footer>`, plus a `<dl>` for the NPM and Program pairs since those are name/value data rather than a plain list. `<article>` was the most useful, each experience entry is one `<article>`, which made it a clean repeating unit to style. I learned this the hard way when I accidentally nested the second `<article>` inside the first, the layout broke immediately, which showed me how directly the HTML structure drives the CSS Grid result.

2. The main challenge was the Experience section, which uses a fixed 160px column for the date and `1fr` for the content on desktop. On a phone that fixed rail takes too much of the screen, so I collapsed it to a single column and let the date stack above the text. For the hero I used `grid-template-areas`, which let me change the order entirely on mobile. Name first, then photo, then details, instead of just shrinking things. I also capped the photo at 220px, since a full-width square image would push all my actual information below the fold.

3. Every experience entry is hand-typed HTML, so my three entries are three near-identical `<article>` blocks. Adding a fourth means copying the whole structure, and changing the layout means editing every block by hand. Next time, I would like to be able to use a loop to help reduce the redundancy of manually typing out each structure again.

## AI Disclosure

I used AI (Claude) to help me understand the logic of how the CSS works, especially during the experience section where I added the pink railing as a separator, and I also asked for help on how to align the text in the experience header and the content below it to make the section look cleaner.

For the website's color scheme, I took inspiration from a portfolio design I found at https://figma.com/resource-library/portfolio-website-examples/, where I used "Example 3, Perry Wang" as a reference. I had originally planned for a dark mode website, and I used Claude to help find the exact color scheme so I could apply it to my CSS.

### Assignment 2
1. When a user opens `/achievements/`, the request first reaches `portofolio/urls.py`, the project-level URL configuration. It matches the prefix and hands the remaining path to `main/urls.py` via `include()`, which is why the `main` app doesn't need to know where it is mounted. `main/urls.py` matches `achievements/` against its `urlpatterns` and calls the associated view, `show_achievements`. The view queries the model with `Achievement.objects.all()`, which the ORM translates into SQL against the database. The returned QuerySet is placed in a context dictionary under the key `achievement_list` and passed to `render()` along with the template name. The template, `achievements.html`, loops over that list with `{% for %}` and substitutes each row's fields into the HTML. The rendered HTML is returned as an `HttpResponse` and the browser displays it. The division of labour is: the project `urls.py` routes between apps, the app `urls.py` routes between views, the view fetches and prepares data, the model defines the data's structure and handles database access, and the template decides how it is presented.

2. Storing the data in a model separates content from presentation. Hard-coded HTML means every new achievement requires editing a template and redeploying the site, and the same markup has to be copied and adjusted by hand each time, so the more entries there are, the more places a mistake can hide. With a model, the template contains one card written once, and the number of entries is a property of the data rather than of the markup. The data also becomes queryable: `Meta.ordering` sorts by `date_awarded` for every query without the view repeating itself, and filtering by category or counting entries takes one line instead of new logic. It persists independently of the code, so restarting or redeploying doesn't lose it. For future development it means the data can be edited through the admin panel or, later, a form on the site, with no code change at all — and unit tests can create rows directly rather than parsing HTML.

3. `makemigrations` reads the current state of `models.py`, compares it against the existing migration files, and writes a new migration describing the difference. It only creates a file; it does not touch the database. `migrate` executes the unapplied migration files against the database, running the actual SQL and recording what has been applied. The split exists so that schema changes are version-controlled files that can be committed and replayed on any machine, my local SQLite and the PWS Postgres both get the same schema from the same files.

## AI Disclosure
I did not use AI for this task, my main references for adding elements and classes was mainly from W3Schools (https://www.w3schools.com/django/django_models.php)

### Assigment 3
1. Django's `ModelForm` builds the form directly from the model, so field definitions and validation rules live in one place instead of being duplicated between `models.py` and hand-written HTML. It renders the inputs, re-populates them when validation fails, and `form.save()` writes straight to the database without me mapping `request.POST` keys to model attributes by hand. Writing the form manually would mean keeping `max_length`, required-ness, and the `ACHIEVEMENT_CHOICES` options in sync across two files, and re-implementing error display myself. `{% csrf_token %}` inserts a per-session token that Django verifies on every POST. Without it, another site could submit a form to my app using my logged-in session cookie, since the browser attaches cookies automatically regardless of which page the request originated from. This is also why my delete action uses a POST form inside the modal rather than a plain GET link, a GET-deletable URL could be triggered by something as simple as an `<img src>` tag on another page.
   
2. JSON maps directly onto native JavaScript data types, so `response.json()` returns a usable object immediately, while XML requires walking a document tree to extract each value. JSON is also lighter over the network since it has no closing tags, and it is easier to read when debugging, comparing my `/json/achievements/` and `/xml/achievements/` endpoints side by side makes the difference obvious. XML's strengths, such as schemas, namespaces, and attribute-based metadata, solve problems that a portfolio API does not have, so the extra verbosity is cost without benefit here.

3. The request hits a URL pattern in `main/urls.py`, which routes it to the view. The view runs a QuerySet to retrieve the model instances, then `serializers.serialize("json", queryset)` converts them into a JSON string, returned inside an `HttpResponse` with `content_type="application/json"` so the client knows how to interpret the body. Serialization is necessary because model instances are live Python objects bound to a database connection, containing methods and internal state that have no meaning outside the server process. They cannot travel over HTTP, so they need a text representation both ends agree on. In my `show_achievements` view the data is serialized by `get_achievement_json` and then immediately deserialized back into `Achievement` instances with `serializers.deserialize` before rendering, which is the full round-trip this week's material demonstrates and is why `{{ achievement.get_category_display }}` still works in the template.

## AI Disclosure
I did not use AI for this week's task again, i referenced the result from my Tutorial 3, I changed the structure of it to match my original achievements html but this time using the base extension etc.
