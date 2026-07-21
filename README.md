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

## Phase 3 — DRF API Foundation

- DRF installed and registered in `THIRD_PARTY_APPS`.
- `BankSerializer` and `AccountSerializer` added (`ModelSerializer`); `AccountSerializer` nests `bank_name` via `source="branch.bank.name"`, reaching through `branch → bank` in one field.
- Same two endpoints (banks list, accounts list) implemented twice, to compare DRF approaches:
  - `BankListAPIView` / `AccountListAPIView` — plain `APIView`, manual `get()` handling.
  - `BankListGenericView` / `AccountListGenericView` — DRF's `ListAPIView`, no `get()` written at all.
- URL structure restructured: login/logout moved under `/auth/`, banks/accounts APIs moved under `/api/`. Phase 2's plain `BankListView`/`AccountListView` are currently unrouted (code still present, no URL points to them).
- All 6 endpoints (`/auth/login/`, `/auth/logout/`, `/api/banks/`, `/api/banks/generic/`, `/api/accounts/`, `/api/accounts/generic/`) smoke-tested end to end.

## Phase 4 — DRF API Deep Dive

- Learning-phase views retired entirely (Phase 2's plain views, Phase 3's `APIView`/`GenericAPIView` pairs) — replaced with one production implementation per endpoint.
- Banks: `BankListAPIView(ListCreateAPIView)` for `GET/POST /api/banks/`, `BankDetailAPIView(RetrieveUpdateDestroyAPIView)` for `GET/PATCH/DELETE /api/banks/{id}/`.
- Accounts: `AccountListAPIView(ListCreateAPIView)` — list/create scoped to the requester via `get_queryset()`/`perform_create()`; `AccountDetailAPIView(RetrieveUpdateDestroyAPIView)` for `GET/PATCH/DELETE /api/accounts/{id}/`.
- `AccountSerializer` gained a writable `branch` field (needed to create an account at all); `user` deliberately kept out of the serializer entirely — always injected server-side via `perform_create()`, never trusted from client input.
- URLs simplified to 2 routes per app: list/create at the root, detail at `<int:pk>/`.
- `users/decorators.py`'s `api_login_required` removed — unused once the Phase 2 views it protected were retired.

## Phase 5 — Authentication & Permissions

- Token authentication (`rest_framework.authtoken`) is now the **only** authentication method — session auth was set up initially, then deliberately removed project-wide in favor of tokens only. `bms/authentication.py` (a CSRF-exempt session workaround) was created and later deleted once session auth was dropped entirely — tokens don't need it, since they're never cookie-based and therefore immune to CSRF by design.
- `POST /api/auth/login/` — returns a token. `POST /api/auth/logout/` — deletes the requester's token, invalidating it immediately.
- Global `DEFAULT_PERMISSION_CLASSES = (IsAuthenticated,)` in `REST_FRAMEWORK` settings — covers `banks/*` automatically (previously fully open, including `DELETE`); no per-view changes needed there.
- `accounts/permissions.py`'s `IsStaffForRetrieveDelete` — `GET` and `DELETE` on `AccountDetailAPIView` require `is_staff`, even for the account's own owner; `PATCH` stays reachable via queryset scoping alone (owner edits their own, staff can reach any).
- `AccountDetailAPIView.get_queryset()` branches: staff → `Account.objects.all()`, regular user → only their own.
- New `AccountBalanceAPIView` + `AccountBalanceSerializer` (`id`/`balance` only) — `PATCH /api/accounts/{id}/balance/`, owner-or-staff via its own `get_queryset()` branching, completely separate from the general detail endpoint.
- Full permission matrix smoke-tested: unauthenticated → `401` everywhere, token login/logout round-trip, staff-vs-owner behavior verified on detail/delete/balance.

## Phase 6 — Filtering, Search & Pagination

- `django-filter` installed and registered (`django_filters` in `THIRD_PARTY_APPS`).
- Applied globally, per the conventions doc ("pagination/authentication/permission classes defined globally"): `DEFAULT_FILTER_BACKENDS` (`DjangoFilterBackend` + DRF's own `SearchFilter` + `OrderingFilter`), `DEFAULT_PAGINATION_CLASS` (`PageNumberPagination`), `PAGE_SIZE = 10` — all in `bms/settings.py`. Only `AccountListAPIView` actually uses them, since it's the only view with `filterset_class`/`search_fields`/`ordering_fields` set.
- `accounts/filters.py` (new) — `AccountFilter`: `bank` and `is_islamic` are custom-bridged (`field_name="branch__bank"` / `"branch__bank__is_islamic"`) since `Account` has no direct field for either; `account_type` is auto-generated from the model field directly.
- `AccountListAPIView` gains `search_fields` (`user__first_name`, `user__last_name`, `user__username`) and `ordering_fields` (`balance`, `created`, `user__username`) — note: `created`, not `created_at`, matching `BaseModel`'s actual field name rather than renaming it to match the spec's wording.
- All scoped **on top of** the existing owner-only restriction — filtering/searching/ordering never expose another user's accounts, they only narrow within whatever the requester's own queryset already returns.
- Verified: `?bank=`, `?account_type=`, `?is_islamic=`, `?search=`, `?ordering=` (both directions), and pagination (`count`/`next`/`previous`/`page=`) all tested against 12 sample accounts.

## Phase 7 — Configuration & Middleware

- `django-constance` installed (`constance` in `THIRD_PARTY_APPS`), `CONSTANCE_BACKEND = MemoryBackend` (in-memory, resets on server restart — no DB table), `CONSTANCE_CONFIG` defines `MAINTENANCE_MODE` (toggleable live via Django admin, no redeploy needed).
- `bms/middlewares.py` (new) — `MaintenanceModeMiddleware`, registered right after `AuthenticationMiddleware` in `MIDDLEWARE`. Returns `503` with the required message for every request when `MAINTENANCE_MODE` is on, except:
  - `/admin/` and `/api/auth/login/` — always exempt (`bms/constants.py`'s `EXEMPT_PATH_PREFIXES`), regardless of who's asking — otherwise nobody could ever reach the switch to turn maintenance mode back off, or get a token to prove they're staff.
  - Staff users — checked two ways, since the project is token-only for the API but Django admin is still session-based: session `request.user.is_staff` (already resolved by `AuthenticationMiddleware` for admin traffic) **or** a manual `Authorization` header → `Token` model lookup (since middleware runs before DRF's own token authentication ever gets a chance to resolve `request.user`).
- Verified via `django.test.Client` against the running app state (not just unit assertions): maintenance off → normal `200`; maintenance on → regular user `503`, staff user `200` via token, `/api/auth/login/` and `/admin/login/` both still reachable during the outage.
