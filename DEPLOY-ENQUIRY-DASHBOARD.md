# Private enquiry CRM deployment

The private dashboard is at `/login/`. Enquiries and follow-up metadata are stored server-side in Upstash Redis by Vercel functions.

## Required Vercel environment variables

Create an Upstash Redis database, then add these under **Vercel → Project → Settings → Environment Variables** for Production:

- `UPSTASH_REDIS_REST_URL` — HTTPS REST endpoint from the Upstash database Connect panel.
- `UPSTASH_REDIS_REST_TOKEN` — Standard REST token with write access.
- `ADMIN_PASSWORD_HASH` — scrypt hash supplied to the site owner.
- `AUTH_SECRET` — random session-signing secret supplied to the site owner.

Never commit these secrets to GitHub. Redeploy Vercel after adding them.

## CRM features

- Search by name, mobile, configuration, purpose, message or source.
- Filter by lead status and marketing consent.
- Track New, Contacted, Qualified and Closed leads.
- Save internal follow-up notes and use Call / WhatsApp actions.
- Export only contacts who explicitly opted into future marketing.
- An 8-hour signed, HttpOnly, SameSite=Strict admin session.
- Up to 5,000 retained enquiries.

## Contact and cookie privacy

Contact details are collected only when a visitor voluntarily submits the enquiry form. Submitting requests contact about that specific enquiry. A separate optional, unchecked box records permission for future property updates and offers. The marketing CSV export includes only contacts with that recorded opt-in.

Cookies are not used to infer names, phone numbers or email addresses. The dashboard uses a strictly necessary session cookie only after administrator sign-in. Do not add advertising or analytics trackers without separate disclosure and appropriate consent.

## First production test

1. Add all four environment variables and redeploy.
2. Open `/login/` and authenticate with the password supplied to the site owner.
3. Submit a test enquiry without marketing consent; confirm **Enquiry only**.
4. Submit another with marketing consent checked; confirm **Marketing opted in**.
5. Update a lead status and notes; refresh to verify persistence.
6. Export opted-in leads; verify only the second test appears.
7. Sign out and verify the dashboard returns to login.

Treat enquiry details as personal data. Restrict Vercel and Upstash access, define a retention period, honour opt-out requests, and delete records when no longer needed. Rotating `AUTH_SECRET` invalidates existing sessions.
