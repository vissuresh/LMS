from celery import shared_task
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from application.models import User

@shared_task(ignore_result=False)
def send_daily_emails():
    print("Sending daily emails")
    logging.info("Sending daily emails")
    user_emails = [user.email for user in User.query.filter(User.librarian == False).all()]
    try:
        smtp_server = '127.0.0.1'
        smtp_port = 1025
        smtp_username = '@wiz@gmail.com'
        smtp_password = 'wiz'

        from_email = smtp_username
        subject = 'Daily Reminder - LMS'
        body = 'This is your daily reminder!'

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)

        for to_email in user_emails:
            msg['To'] = to_email
            server.sendmail(from_email, to_email, msg.as_string())
            logging.info(f"Email sent to user: {to_email}")

        # Close the SMTP connection
        server.quit()

    except Exception as e:
        logging.error(f"Failed to send daily emails: {e}")



@shared_task(ignore_result=False)
def add(x, y):
    return x + y