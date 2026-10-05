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


### Assignment 4

This assignment adds authentication, role-based access control, and a star feature to the portfolio.

| Role | Can do |
|---|---|
| Visitor (not logged in) | View all pages. Clicking Star redirects to login. |
| Regular user | Everything above, plus star and unstar experiences. |
| Editor | Everything above, plus edit experiences and achievements. |
| Owner (superuser) | Everything above, plus create and delete experiences and achievements. |

- **Authentication:** Register, login, and logout use Django's built-in `User` model with `UserCreationForm` and `AuthenticationForm`. The navbar shows "Hi, username" and a Logout link when logged in, and Login/Register links otherwise.
- **Editor role:** A Django Group called `Editor` with the `change_experience` and `change_achievement` permissions, assigned to users through the Django admin.
- **Access control:** Every create, edit, delete, and star view has `@login_required`, so visitors are redirected to `/login/`. Edit views check `request.user.has_perm(...)`, and create and delete views check `is_superuser`, raising `PermissionDenied` (HTTP 403) otherwise. Because superusers hold every permission, one `has_perm` check covers both the editor and the owner.
- **Hidden controls:** Templates show the Add, Edit, and Delete buttons only to users allowed to use them, via `{% if perms.main.change_... %}` and `{% if user.is_superuser %}`.
- **Star feature:** `Experience` has a `starred_by` `ManyToManyField` to `User`. The `toggle_star` view is POST-only with `{% csrf_token %}`, and adds or removes the current user. A many-to-many link can only exist once per user and item, so each user can star an item at most once. Each card shows the total count and whether you have starred it (Star / Unstar).
- **API integrity:** The Experience JSON and XML endpoints serialize with `use_natural_foreign_keys=True`, so `starred_by` lists usernames instead of internal user database ids. I also moved the achievement data routes above `json/<str:id>/` and `xml/<str:id>/` in `main/urls.py`, since the catch-all routes were capturing `/json/achievements/` and crashing it.

## Ai Disclosure:
I used gemini flash-lite in this assignment. I used it to confirm wether my logic regarding the creation of roles and assigning of roles was correct. Some aspects gemini got wrong were in guiding me on how to add the role itself, it assumed alot about my project without directly confirming the hierarchy or structure of my project. I ended up having to manually find the permission for editor itself.
 
Chat log link: https://share.gemini.google/AFIBXqtiDVwp

### Assignment 5

1. Debouncing is a process where function calls are delayed so only one function will call in a given time. This is important for AJAX programs since it focuses on updates on small sections of the website itself. It will help prevent network traffic and server overload since only one function will run in a specific time

2. fetch() doesn't return the response itself. It returns a Promise, which is a placeholder that settles later, once the network request finishes. await pauses that one async function until the Promise settles and then gives back the real value. Everything else on the page keeps running in the meantime, so the browser doesn't freeze while it waits. In fetchAchievements I await twice. The first await fetch(url) waits for the response headers so I can check response.ok. The second await response.json() waits for the body to arrive and be parsed into an array. Without await, response would be a pending Promise rather than a Response. response.ok would be undefined, so the check would treat every request as failed and throw. achievementData.length would also be undefined, so neither the empty state nor the grid would ever show. The code would run straight on with data that doesn't exist yet. Leaving out await also changes error handling: a failed request would be a rejected Promise that nothing waits on, so my try/catch would never catch it and the error state would never appear. The same applies to addAchievement. Without await, the toast and fetchAchievements() would run before the server had even answered the POST.

3. Cross-Site Scripting (XSS) is an attack where someone stores or injects text that contains HTML or JavaScript, such as <img src="x" onerror="alert('XSS!')">, and the page later puts it into the DOM as real markup. The browser then runs the script in the page's own context. That gives it access to the visitor's session and lets it act as them: read the page, send requests with their cookies, or change what they see. A Django template protects against this by default, because {{ achievement.title }} is auto-escaped, so < becomes &lt; and the payload shows up as plain text. Once the data comes through AJAX, Django never touches it. The JSON is just raw strings, and the HTML is built in JavaScript. Template-literal strings assigned to innerHTML, as in buildAchievementCardElement, are parsed as live HTML with no escaping at all. Every value I insert is now my responsibility, and one forgotten field is enough to open a hole. That's why each field from the server goes through escapeHtml before it reaches innerHTML. As a second layer, clean_title, clean_issuer and clean_description in AchievementForm run strip_tags, so the payload is either stripped or rejected before it gets into the database. I tested it with the <img onerror> payload: a title made only of tags is rejected with a 400 error, and no alert appears.

## AI Disclosure:
I did nto use AI for this task, i referenced Tutorial 5 and the experience part of my code while changing the variables to match the achievements.