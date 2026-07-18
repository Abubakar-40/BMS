# BMS

A Django + DRF training project covering banks, branches, accounts, and transactions.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then visit `http://127.0.0.1:8000/admin/` to add sample banks, branches, and accounts.

## Phase 1 — Django Foundation

- Django project created (`django-admin startproject`), settings package renamed to `bms` to match the repo name.
- Three apps created at the repo root — `banks`, `accounts`, `users` — and registered in `INSTALLED_APPS` (split into `DEFAULT_APPS`/`THIRD_PARTY_APPS`/`CUSTOM_APPS` tuples).
- Custom `User` model (`AbstractUser` + `phone`, `date_of_birth`) set as `AUTH_USER_MODEL` before the first migration.
- Domain models defined: `Bank` (name, swift code, `is_islamic`, established date), `Branch` (FK to `Bank`), `Account` (FK to `User` and `Branch`, `account_type` via `TextChoices`, `balance`, `is_active`). Model names follow the "don't repeat the app name" convention — `banks.Branch` and `accounts.Account`, not `BankBranch`/`BankAccount`.
- Migrations generated and applied (`makemigrations`, `migrate`), creating `db.sqlite3` and all tables.
- All four models registered in Django admin with `list_display`, `list_filter`, `search_fields`; superuser created and sample data (2 banks, 2 branches, 2 users, 3 accounts) added through the admin UI.
- ORM practiced in `bms/practice.py` (run directly with `python bms/practice.py`) — `filter`, `get`, `values`, `select_related` across relationships, `annotate` for per-bank account counts, and a multi-hop relationship filter (Islamic banks with active accounts).

## Phase 2 — Basic Django Views

- Pure JSON API, no templates — every response is a `JsonResponse`, tested via Postman.
- Session-based login/logout using Django's built-in `authenticate()`/`login()`/`logout()`: `POST /login/` (form-encoded `username`/`password`), `POST /logout/`. Both are CSRF-exempt since there's no frontend to carry a CSRF token.
- Custom `api_login_required` decorator (`users/decorators.py`) wraps each protected view's `dispatch()` method and returns a JSON `401` for unauthenticated requests, instead of Django's default redirect-to-login behaviour, which doesn't make sense for a pure API.
- `GET /banks/` — all banks with an annotated branch count, auth required.
- `GET /accounts/` — only the logged-in user's own accounts (`Account.objects.filter(user=request.user)`), auth required.
- All routes wired up through per-app `urls.py` files (namespaced with `app_name`), included into the root `bms/urls.py`.
- Full flow smoke-tested end to end: unauthenticated request → `401`, login → session cookie issued, authenticated requests → real data scoped to the logged-in user, logout → session cleared, subsequent request → `401` again.
