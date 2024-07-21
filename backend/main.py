from application import app

with app.app_context():
    from application.models import User, Librarian
    from application import db
    
    print("========= Updating librarian table =========")
    
    librarian_emails = app.config['LIBRARIAN_EMAILS']

    current_librarians = Librarian.get_all_librarians()
    emails_to_add = set(librarian_emails) - set(current_librarians)
    emails_to_remove = set(current_librarians) - set(librarian_emails)
    
    for email in emails_to_add:
        user = User.get_user_by_email(email)
        if user:
            new_librarian = Librarian(user_id=user.id)
            db.session.add(new_librarian)
    
    for email in emails_to_remove:
        librarian_to_remove = Librarian.get_librarian_by_email(email)
        if librarian_to_remove:
            db.session.delete(librarian_to_remove)
    
    db.session.commit()


if __name__ == '__main__':
    app.run(port=5000)
    