"""
Vercel Serverless Function — POST /api/send

Receives one email job per call and dispatches it via Gmail SMTP.
Credentials (gmail_user, gmail_pass) are supplied by the browser each time
the user initiates a send — they are never logged or persisted.

No environment variables are required.
"""

import json
import smtplib
import base64
import traceback
from http.server import BaseHTTPRequestHandler
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formataddr


CORS = {
    "Access-Control-Allow-Origin":  "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Content-Type": "application/json",
}


class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        for k, v in CORS.items():
            self.send_header(k, v)
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        try:
            data = json.loads(self.rfile.read(length))
        except json.JSONDecodeError:
            self._respond(400, {"ok": False, "error": "Invalid JSON"})
            return

        # ── Required fields ────────────────────────────────────────────────
        required = ["gmail_user", "gmail_pass", "to_email", "subject", "body", "attachment_b64"]
        for f in required:
            if not data.get(f):
                self._respond(400, {"ok": False, "error": f"Missing: {f}"})
                return

        gmail_user      = data["gmail_user"].strip()
        gmail_pass      = data["gmail_pass"].replace(" ", "").strip()
        from_name       = data.get("from_name", "Certificate System").strip()
        to_email        = data["to_email"].strip()
        to_name         = data.get("to_name", "").strip()
        subject         = data["subject"]
        body_text       = data["body"]
        attachment_b64  = data["attachment_b64"]
        attachment_name = data.get("attachment_name", "certificate.png")

        # ── Send ───────────────────────────────────────────────────────────
        try:
            img_bytes = base64.b64decode(attachment_b64)

            msg = MIMEMultipart()
            msg["From"]    = formataddr((from_name, gmail_user))
            msg["To"]      = formataddr((to_name, to_email)) if to_name else to_email
            msg["Subject"] = subject

            msg.attach(MIMEText(body_text, "plain", "utf-8"))

            img_part = MIMEImage(img_bytes, name=attachment_name)
            img_part.add_header("Content-Disposition", "attachment", filename=attachment_name)
            msg.attach(img_part)

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(gmail_user, gmail_pass)
                smtp.sendmail(gmail_user, to_email, msg.as_string())

            self._respond(200, {"ok": True})

        except smtplib.SMTPAuthenticationError:
            self._respond(401, {
                "ok": False,
                "error": "Gmail login failed. Double-check your address and app password."
            })

        except smtplib.SMTPRecipientsRefused:
            self._respond(400, {
                "ok": False,
                "error": f"Gmail refused the recipient address: {to_email}"
            })

        except Exception as e:
            print(traceback.format_exc())
            self._respond(500, {"ok": False, "error": str(e)})

    def _respond(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        for k, v in CORS.items():
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
