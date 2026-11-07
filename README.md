# CampusConnect

A Django app with sign-up, login, a dashboard and an editable profile page, styled with Bootstrap 5.

- **Name:** SINAY, LADY DIVINAH M.
- **Section:** BSIT 3 - G1

## Features

- Sign-up with a success message (Django messages framework, shown as a Bootstrap alert)
- Login / logout
- Profile page (class-based `UpdateView`) where a logged-in user can view and edit their own profile only
- Shared `base.html` with the Bootstrap 5 CDN and a navigation bar; every page extends it

## How to run

1. Clone the repository and go into the folder:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   ```
3. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply the migrations:
   ```bash
   python manage.py migrate
   ```
5. (Optional) Create an admin account:
   ```bash
   python manage.py createsuperuser
   ```
6. Start the server and open http://127.0.0.1:8000/
   ```bash
   python manage.py runserver
   ```

## Pages

| URL | Page |
| --- | --- |
| `/accounts/signup/` | Sign up |
| `/accounts/login/` | Log in |
| `/accounts/profile/` | My profile (login required) |
| `/` | Dashboard (login required) |

## Running the tests

```bash
python manage.py test
```
