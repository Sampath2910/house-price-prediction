import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# =========================================================
# CONFIGURATION
# =========================================================
# ⚠️ Replace these with your actual Gmail credentials
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"  # use App Password, not your main password

# =========================================================
# FUNCTION TO SEND EMAIL
# =========================================================
def send_contact_email(name, sender_email, subject, message):
    try:
        receiver_email = EMAIL_ADDRESS
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = f"📩 Contact Form: {subject or 'No Subject'}"

        body = f"""
        Name: {name}
        Email: {sender_email}

        Message:
        {message}
        """

        msg.attach(MIMEText(body, "plain"))

        # Connect to Gmail SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(sender_email, receiver_email, msg.as_string())

        print(f"✅ Email successfully sent from {sender_email} to {receiver_email}")

    except Exception as e:
        print(f"❌ Error sending email: {e}")
        raise e
