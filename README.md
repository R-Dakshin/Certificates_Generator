# Certificate Generator (Business Edition)

A lightweight, self‑hosted solution for generating and distributing personalized certificates at scale.
This project combines a single‑page frontend with a small serverless backend so your team can upload a template, map recipient data, preview certificates, and email finalized assets from a standard Gmail account.

---

## What this project does

- Generates PDF/PNG certificates from a design template and spreadsheet data
- Personalizes each certificate using column values (e.g., name, course, date)
- Sends certificates as email attachments via Gmail SMTP (App Password required)
- Runs entirely on Vercel (frontend + serverless Python API)

---

## Key benefits for business usage

- **No backend infrastructure to manage** — deployed as a Vercel Serverless project
- **Data stays under your control** — recipient spreadsheets remain on your device
- **Secure, disposable credentials** — Gmail app passwords are supplied per send and are not stored
- **Audit-friendly** — send logs are visible in the browser interface

---

## How to use

### Prepare your assets

1. Create a certificate design (PNG/JPG).
2. Create a recipient spreadsheet (`.xlsx` or `.csv`) with at least:
   - A column containing email addresses (header must include the word `email`).
   - A column containing recipient names (header must include the word `name`).
   - Any additional columns become template variables (`{{ColumnName}}`).

### Send certificates

1. Open the deployed application in your browser.
2. Upload your certificate image and spreadsheet.
3. Click the certificate preview to place each text field.
4. Customize email subject + body; use `{{ColumnName}}` placeholders as needed.
5. Enter your Gmail address and **App Password**.
6. Click **Send all emails** and monitor the send log.

---

## Deployment notes (Vercel)

This project is configured for Vercel via `vercel.json`.
The frontend lives in `public/` and the API lives in `api/`.

If you need to deploy manually, push the repo to GitHub and import it in Vercel.

---

## Security considerations

- The backend never stores credentials or recipient data.
- Emails are sent through Gmail SMTP using credentials provided at send time.
- Use a dedicated Gmail account and an App Password to reduce risk.

---

## Support & troubleshooting

### Common issues

- **No email column found**: ensure the spreadsheet column header contains `email`.
- **Authentication errors**: confirm you are using a valid Gmail App Password.
- **Deployment fail**: check that `vercel.json` exists and the `/api` routes are present.

For any other issues, consult your Vercel deployment logs or check the browser console for errors.

---

## Project layout

- `public/index.html`: single‑page frontend UI
- `api/ping.py`: health check endpoint
- `api/send.py`: SMTP email sender (Gmail)
- `vercel.json`: deployment routing + build configuration
- `pyproject.toml`: Python build metadata (Vercel build support)
