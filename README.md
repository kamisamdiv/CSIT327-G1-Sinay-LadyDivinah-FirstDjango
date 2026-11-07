# CyclePrep – First Django Lab

**Name:** Lady Divinah M. Sinay
**Section:** CSIT327 – G1

CyclePrep is a lightweight web app that gives students an early heads-up before their next cycle.
This lab covers accounts: **Sign up**, **Login/Logout**, and a **Profile** page where each user manages
their own details and cycle settings (cycle type, cycle length, period length, reminder days).

## Features in this lab

- **Profile page** built with Django's class-based `UpdateView` (`accounts/views.py → ProfileUpdateView`).
  - `LoginRequiredMixin` sends logged-out visitors to the login page.
  - The URL is just `/profile/` with no id. `get_object()` always returns `request.user`'s profile,
    so a user can never open or edit someone else's profile.
- **Sign-up success message** using Django's messages framework, shown as a Bootstrap alert.
- **Responsive, Notion-inspired workspace** with cycle-focused navigation and red, pink, and baby-pink styling in the shared `templates/base.html`.
- All forms are styled with Bootstrap classes (`form-control`, `form-select`, `btn`) and include `{% csrf_token %}`.

## How to run

1. Clone the repository and open the project folder:
   ```bash
   git clone https://github.com/<your-username>/CSIT327-G1-Sinay-LadyDivinah-FirstDjango.git
   cd CSIT327-G1-Sinay-LadyDivinah-FirstDjango
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   ```
   Windows PowerShell:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```
   macOS / Linux:
   ```bash
   source .venv/bin/activate
   ```
3. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. Create the database tables:
   ```bash
   python manage.py migrate
   ```
5. (Optional) Create an admin account:
   ```bash
   python manage.py createsuperuser
   ```
6. Start the server and open http://127.0.0.1:8000/:
   ```bash
   python manage.py runserver
   ```

To run the automated tests: `python manage.py test accounts`

## Pages

| URL | Page | Login required |
|-----|------|----------------|
| `/` | Home | No |
| `/signup/` | Sign up | No |
| `/login/` | Log in | No |
| `/logout/` | Log out (POST only) | Yes |
| `/profile/` | View and edit your own profile | Yes |
| `/admin/` | Django admin | Staff only |

## Project structure

```
cycleprep/        project settings and root URLs
accounts/         sign-up, login, profile (models, forms, views, urls, tests)
templates/        base.html, home.html, accounts/, registration/, includes/
```

## Notes

- The secret key is read from the `DJANGO_SECRET_KEY` environment variable. The built-in fallback is for local development only.
- `venv/`, `__pycache__/`, `db.sqlite3` and `.env` files are excluded by `.gitignore`.
