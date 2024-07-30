from celery import shared_task
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from application.models import User, BookIssue, BookRequest, Book, Section
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader
from application import app
from io import StringIO, BytesIO
import csv
from flask import jsonify, send_file, Blueprint
from celery.result import AsyncResult
from flask_sse import sse
import time


task_bp = Blueprint(
    'tasks',
    __name__
)


@shared_task(ignore_result=False)
def send_daily_emails():
    print("Sending daily emails")
    logging.info("Sending daily emails")
    users = User.query.filter(User.librarian == False).all()

    try:
        smtp_server = '127.0.0.1'
        smtp_port = 1025
        smtp_username = '@wiz@gmail.com'

        from_email = smtp_username
        subject = 'Daily Reminder - LMS'

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['Subject'] = subject

        server = smtplib.SMTP(smtp_server, smtp_port)

        for user in users:
            if len(user.books) == 0:
                continue

            body = ''

            for i in range(len(user.books)):
                book = user.books[i]
                issue = BookIssue.query.filter_by(user_id = user.id, book_id = book.id).first()
                if issue.expiry > datetime.now():
                    formatted_expiry = issue.expiry.strftime("%d - %b - %Y - %H:%M") 
                    body += f"{i+1}. {book.name} ::\t {formatted_expiry}\n"

            if body != '':
                to_email = user.email

                body = f"Hello {user.name}.\nThis is your daily reminder. Your following books expire soon:\n\n" + body
                msg.attach(MIMEText(body, 'plain'))
                msg['To'] = to_email
                server.sendmail(from_email, to_email, msg.as_string())
                logging.info(f"Email sent to user: {to_email}")

        server.quit()
        return True

    except Exception as e:
        logging.error(f"Failed to send daily emails: {e}")
        return False
    


@shared_task(ignore_result=False)
def generate_activity_report():
    print("Generating activity report")
    logging.info("Generating activity report")

    month, year = datetime.now().strftime('%B'), datetime.now().year

    books = {}
    sections = {}

    issues = BookIssue.query.filter(BookIssue.issued_at > datetime.now() - timedelta(days=30)).all()
    for issue in issues:
        book_obj = Book.query.get(issue.book_id)

        if books.get(issue.book_id) is None:
            book = {}

            book['name'] = book_obj.name
            book['rating'] = book_obj.rating
            book['issue_count'] = 1
            book['request_count'] = 0

            books[issue.book_id] = book

        else:
            book = books[issue.book_id]
            book['issue_count'] += 1

        if sections.get(book_obj.section_id) is None:
            section = {}

            section_obj = Section.query.get(book_obj.section_id)
            section['name'] = section_obj.name
            section['issue_count'] = 1
            section['request_count'] = 0

            sections[book_obj.section_id] = section

        else:
            section = sections[book_obj.section_id]
            section['issue_count'] += 1



    requests = BookRequest.query.filter(BookRequest.requested_at > datetime.now() - timedelta(days=30)).all()
    for request in requests:
        book_obj = request.book

        if books.get(request.book_id) is None:
            book = {}
            
            book['name'] = book_obj.name
            book['rating'] = book_obj.rating
            book['request_count'] = 1
            book['issue_count'] = 0
            books[request.book_id] = book

        else:
            book = books[request.book_id]
            book['request_count'] += 1
            book['issue_count'] = book.get('issue_count', 0)


        
        if sections.get(book_obj.section_id) is None:
            section = {}

            section_obj = Section.query.get(book_obj.section_id)
            section['name'] = section_obj.name
            section['request_count'] = 1
            section['issue_count'] = 0

            sections[book_obj.section_id] = section

        else:
            section = sections[book_obj.section_id]
            section['request_count'] += 1
            section['issue_count'] = section.get('issue_count', 0)

    

    for book_id, book in books.items():
        book['id'] = book_id

    for section_id, section in sections.items():
        section['id'] = section_id

    books_data = list(books.values())
    sections_data = list(sections.values())


    logging.info(books_data)
    logging.info(sections_data)

    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('report_template.html')
    html_report = template.render(sections=sections_data, books=books_data, month=month, year=year)

    sender_email = "wiz@gmail.com"
    receiver_email = "wiz@gmail.com"
    subject = f"Activity Report - {month} {year}"
    smtp_server = "127.0.0.1"
    smtp_port = 1025

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    part = MIMEText(html_report, "html")
    msg.attach(part)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.sendmail(sender_email, receiver_email, msg.as_string())
        logging.info("Activity report sent successfully")
    except Exception as e:
        logging.error(f"Failed to send activity report: {e}")
        return False

    return True



@shared_task(bind=True, ignore_result=False)
def generate_csv(self):
    time.sleep(5)
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'operation_id', 'operation_type', 'operation_time', 'book_id', 'book_name', 'section_id', 'section_name', 
        'author', 
    ])
    
    issued_books = [(issue.id, 'issue', issue.issued_at, Book.query.get(issue.book_id)) for issue in BookIssue.query.filter(BookIssue.expiry > datetime.now()).all()]
    expired_books = [(issue.id, 'revoke/return', issue.expiry, Book.query.get(issue.book_id)) for issue in BookIssue.query.filter(BookIssue.expiry <= datetime.now()).all()]
    requested_books = [(request.id, 'request', request.requested_at, request.book) for request in BookRequest.query.all()]

    all_books = issued_books + expired_books + requested_books

    for operation_id, operation_type, operation_time, book in all_books:
        writer.writerow([
            operation_id, operation_type, operation_time, book.id, book.name, book.section_id, book.section.name, book.author
        ])

    csv_data = output.getvalue()
    output.close()
    sse.publish({"task_id": self.request.id, "status": "SUCCESS", "csv_data": csv_data}, type='task_status')
    return True


@task_bp.get('/export-csv')
def export_csv():
    task = generate_csv.delay()
    return jsonify({"task_id": task.id}), 202