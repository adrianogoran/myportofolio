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

