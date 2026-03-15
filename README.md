# 🎓 Certificate Generator Studio

A browser-based tool to generate personalized certificates from an image template + Excel sheet and email them to recipients — deployed on **Vercel** with a Python serverless backend.

---

## ✨ Features

- Upload any PNG/JPG certificate template
- Upload an Excel (`.xlsx`) or CSV file with recipient data
- Click directly on the certificate to position each text field
- Fine-tune font size, color, and alignment per field
- Preview every certificate before sending
- Send personalized certificates with the certificate attached as PNG
- Download all certificates locally (no email needed)

---

## 📁 Project Structure

```
cert-generator/
├── public/
│   └── index.html          # Full frontend — upload, map, preview, send
├── api/
│   ├── ping.py             # GET /api/ping — health check
│   └── send.py             # POST /api/send — sends one email via Gmail SMTP
├── vercel.json             # Vercel routing + build config
├── requirements.txt        # Python dependencies (stdlib only)
└── README.md
```

---

## 🚀 Deploy to Vercel

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
gh repo create cert-generator --public --push
```

### 2. Import on Vercel

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repository
3. Framework preset: **Other**
4. Root directory: `cert-generator` (or `/` if you pushed the folder contents directly)
5. Click **Deploy**

### 3. Done

Your app will be live at `https://your-project.vercel.app`

---

## 🔑 Gmail App Password Setup

Standard Gmail passwords won't work — you need an **App Password**:

1. Go to [myaccount.google.com/security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** if not already on
3. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
4. Create a new App Password — name it anything (e.g. "Certificates")
5. Copy the 16-character password → paste it as `GMAIL_PASS` in Vercel

---

## 📊 Excel / CSV Format

Your spreadsheet must have at minimum:

| Name          | Email                  | (any other columns...) |
|---------------|------------------------|------------------------|
| Arun Kumar    | arun@example.com       | Python Basics          |
| Priya Sharma  | priya@example.com      | Data Science           |

- The column containing email addresses must have **"email"** anywhere in its name (case-insensitive). Examples: `Email`, `email`, `Leader Email`, `EMAIL` — all work.
- The name column must have **"name"** in its name. Examples: `Name`, `Team Name`, `Full Name`.
- All other columns are available as `{{ColumnName}}` variables in the email body template.

---

## 🖼️ How to Use

1. **Upload** — drop your certificate image and Excel file
2. **Fields** — click on the certificate preview to place each column's text; adjust font size, color, alignment in the table
3. **Preview** — flip through each person's generated certificate; download a sample
4. **Email** — customize subject and body (use `{{Name}}`, `{{Course}}` etc.); click **Test connection** to verify the API
5. **Send** — hit **Send all emails** to dispatch; watch the live log

---

## 🛠️ Local Development

No Node.js or build step needed. Just run a static server:

```bash
cd cert-generator
python3 -m http.server 8080 --directory public
```

For the email API locally, you can still use the original `server.py` (from the non-Vercel version) running on port 5050, then change the API endpoint in Step 4 back to `http://localhost:5050`.

---

## 🔒 Security Notes

- Gmail credentials are entered by the user on Step 4 **each time** they want to send — they are never stored in the browser, in any database, or in the source code
- The `/api/send` function receives credentials per-request over HTTPS, uses them once to authenticate with Gmail, then discards them — no logging, no persistence
- No environment variables needed

---

## 📦 Dependencies

| Layer    | Dependencies                                      |
|----------|---------------------------------------------------|
| Frontend | [SheetJS (xlsx)](https://sheetjs.com/) via CDN    |
| Backend  | Python stdlib only (`smtplib`, `email`, `base64`) |
| Hosting  | Vercel (free tier is sufficient)                  |

---

## 🐛 Troubleshooting

| Problem | Fix |
|---|---|
| "No email column found" | Rename your email column to include the word "email" |
| "Gmail authentication failed" | Double-check `GMAIL_PASS` — use App Password, not your Gmail password |
| Certificate text is in the wrong position | Go back to Step 2, click the correct spot on the certificate |
| Test connection fails on Vercel | Make sure you redeployed after adding environment variables |
| Emails going to spam | Add your Gmail as a verified sender in Google Workspace, or ask recipients to mark as not spam |
