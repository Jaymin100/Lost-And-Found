# Lost & Found System

SE480 team project — a web-based lost and found system for the university.
Admins log in, add found items with a photo, move items to the archive, and view
the active and archive lists. Guests see only counts and "added yesterday" style
updates, with no details.

## Team

| Person | Owns |
|---|---|
| Jackson Stahnke | Backend + DB setup (`db/schema.sql`, `db/seed_admins.py`, DB connection code, item endpoints) |
| Jaymin Swedlund | Architect + backend (API contract, auth endpoints, auto-archive logic) |
| Jacob Weller | Frontend / UI (everything in `public/`) |
| Mason Sunderlin | QA + team lead (manual test checklist, bug reports) |

## First-time local setup

1. Install Python 3.16, MySQL 8.0, and Git.
2. Clone the repo, create a virtual environment, activate it, and install dependencies:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your local MySQL password and a random `SECRET_KEY`.
4. Create the tables:
   ```
   mysql -u root -p < db/schema.sql
   ```
5. Create the admin logins:
   ```
   python db/seed_admins.py
   ```
6. Start the app:
   ```
   flask --app app run --debug
   ```
   Open http://localhost:5000.

## Project structure

```
lost-and-found/
├── app.py                 Flask app; registers all routes and serves public/
├── backend/
│   ├── config.py          reads .env
│   ├── db.py              PyMySQL connection, sets time_zone to UTC
│   ├── auth.py            login / logout / me + login_required decorator
│   ├── items.py           active + archive lists, add, archive, photo endpoints
│   ├── public.py          guest summary + item types
│   └── archiving.py       archive_expired_items()
├── public/                frontend (Jacob)
│   ├── index.html
│   ├── css/styles.css
│   └── js/
│       ├── app.js         hash router + nav bar
│       ├── api.js         one function per API endpoint
│       └── pages/         guest.js, login.js, active.js, archive.js, add-item.js
├── db/
│   ├── schema.sql         source of truth for tables
│   └── seed_admins.py     creates the 5 admin logins with hashed passwords
├── requirements.txt
├── .env.example
├── .env                   (never committed)
├── .gitignore
└── README.md
```

## Git workflow

Everyone commits straight to `main`.

- Pull before you start, every time: `git pull --rebase`.
- Stay in your lane. Jacob edits `public/`; Jackson and Jaymin edit `backend/`, `app.py`, and `db/`.
  Touching someone else's files? Say so in Discord first.
- Pull again right before you push. Fix conflicts locally, run the app, then push.
- Schema or API changes: update the team context doc and post in Discord in the same hour.

See the full Team Context Doc for the API contract, database schema, security rules, and the
manual test checklist.
