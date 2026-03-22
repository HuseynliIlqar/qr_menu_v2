# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Activate virtual environment
source .venv/Scripts/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver

# Create a tenant (restaurant)
python manage.py create_tenant

# Collect static files
python manage.py collectstatic
```

## Architecture

This is a **Django 6 multi-tenant SaaS QR menu platform** for restaurants, powered by **django-tenants** with PostgreSQL schema-based isolation.

### Multi-Tenancy Model

- **Shared schema** (`public` app): `Client` and `Domain` models — one row per restaurant
- **Per-tenant schema** (`qr_menu_app`): all restaurant data lives in isolated PostgreSQL schemas
- `TenantMainMiddleware` routes each request to the correct schema based on domain
- `SHARED_APPS` / `TENANT_APPS` in `core/settings.py` controls which Django apps belong to which layer

### Data Models (`qr_menu_app/models/`)

Each model enforces a max-items constraint in `save()` — not in migrations:

| Model | Limit | Notes |
|---|---|---|
| `MainSectionModel` | 1 | Core restaurant config: name, icon, contact info |
| `MenuItem` | — | Has `original_price`, `discount_price`, `price_save` |
| `ItemCategory` | — | Auto-generates slug; controls display order |
| `IndexSliderPhotoModel` | 3 | Hero carousel images |
| `SocialMediaIconModel` | 3 | Social links |
| `InfoSection` | 4 | Info cards with description + URL |
| `RestoranGaleryModel` | 5 | Gallery photos |

### View Layer

`qr_menu_app/views/index_view.py` — single view (`index_page`) that uses `Prefetch` and `.only()` for optimized loading of all related data in one pass.

### Environment Variables

Copy `.env.example` to `.env` and fill in:

```
SECRET_KEY=
DEBUG=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=      # defaults to localhost
DB_PORT=      # defaults to 5432
```

PostgreSQL is required — SQLite is not supported due to schema-based multi-tenancy.
