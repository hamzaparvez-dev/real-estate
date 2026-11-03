# Private enquiry dashboard deployment

The static site is hosted on Vercel. The private dashboard is at `/login/`. Enquiry records are stored server-side in Upstash Redis; they are never stored in browser local storage.

## Required Vercel environment variables

Create an Upstash Redis database, then add these values under **Vercel → Project → Settings → Environment Variables** for Production:

- `UPSTASH_REDIS_REST_URL` — HTTPS REST endpoint from the Upstash database Connect panel.
- `UPSTASH_REDIS_REST_TOKEN` — Standard REST token (the API needs write access).
- `ADMIN_PASSWORD_HASH` — copy the scrypt hash from the site-owner handoff.
- `AUTH_SECRET` — copy the random secret from the site-owner handoff.

Do not put these values in GitHub files. Redeploy Vercel after adding all four values.

## Behaviour

- Public enquiries are accepted only from the same website origin.
- The API validates the visitor's name, Indian mobile number and configuration, rate-limits submissions, and saves the enquiry before opening WhatsApp.
- The dashboard uses an 8-hour signed, HttpOnly, SameSite=Strict session cookie. Password verification is server-side with scrypt.
- Only an authenticated session can read the paginated enquiry list.
- The Redis list retains the latest 5,000 submissions.
- The login page is marked noindex.

## First deployment test

1. Configure all four Vercel environment variables and redeploy.
2. Open `/login/` and sign in with the password provided to the site owner.
3. Submit one test enquiry from the public website.
4. Confirm it appears in the private dashboard and WhatsApp opens only after the save succeeds.
5. Sign out and confirm the dashboard returns to the sign-in screen.

Treat enquiry records as personal data. Limit Vercel and Upstash access to authorized staff and apply a suitable retention/deletion process. Rotating `AUTH_SECRET` invalidates existing dashboard sessions.
