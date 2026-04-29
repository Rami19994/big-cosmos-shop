# Nova Commerce Django

A production-ready Django e-commerce and management system scaffold with bilingual English/Arabic storefront, RTL/LTR support, product catalog, cart, checkout, order management, inventory, coupons, content pages, blog, and a custom staff dashboard.

## Run locally

1. Create and activate a Python 3 virtual environment.
2. Install dependencies: `pip3 install -r requirements.txt`
3. Create the database: `python3 manage.py migrate`
4. Create an admin user: `python3 manage.py createsuperuser`
5. Start the server: `python3 manage.py runserver`
6. Open `http://127.0.0.1:8000/en/` or `http://127.0.0.1:8000/ar/`.

## Key URLs

- Storefront: `/en/`
- Products: `/en/products/`
- Cart: `/en/cart/`
- Checkout: `/en/orders/checkout/`
- Account: `/en/account/login/`
- Custom dashboard: `/en/dashboard/`
- Django admin: `/en/admin/`

## Production notes

- Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0`, `DJANGO_ALLOWED_HOSTS`, SMTP settings, and database environment variables in production.
- Use PostgreSQL for production and object storage/CDN for media.
- Compile translations with `python3 manage.py compilemessages` after editing `.po` files.
- Payment providers are represented with a clean integration structure; add real Stripe/PayPal credentials and webhook handlers before accepting live card payments.
