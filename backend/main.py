from application import app

with app.app_context():
    from application.models import User
    
    librarian = app.config['LIBRARIAN']
    librarian_email = librarian["email"]
    librarian_object = User.get_librarian_by_email(librarian_email)

    if librarian_object is None:
        print("===== Creating Librarian Account =======")
        librarian_name = librarian["name"]
        librarian_password = librarian["password"]

        librarian_object = User(name=librarian_name, email = librarian_email, librarian = True)
        librarian_object.set_password(librarian_password)
        librarian_object.save()


if __name__ == '__main__':
    app.run(port=5000)