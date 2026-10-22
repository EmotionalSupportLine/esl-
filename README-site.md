# The Emotional Support Line site + the Nest app

No build step, no database. Deploy this folder to Vercel as-is.

- `index.html` public site, `app/` the Nest (member data stays on each device)
- `assets/config.js` every price and link in one place
- `api/` three tiny functions that check Stripe and unlock membership

Vercel environment variables:
- `STRIPE_SECRET_KEY` restricted key, read-only: Checkout Sessions, Customers, Subscriptions
- `MEMBER_SECRET` long random string
- `MEMBER_BOOK_URL` the $50 member booking page
- `GROUP_CALL` text shown to members about the monthly group call
- `LIBRARY_JSON` optional class list; otherwise `api/_library.json`

Stripe Payment Links: set the after-payment redirect to
`https://theemotionalsupportline.com/app/?session_id={CHECKOUT_SESSION_ID}`
