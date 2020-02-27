from backend.models import Address, User


def create_user():
    username = "sampleuser"
    password = "securepassword"
    email = "asdfsdf@gmail.com"
    number = "09121234589"
    location = "Inja, oonja, hameja"

    user = User(username=username, number=number, email=email)
    user.set_password(password)
    user.save()

    Address.objects.create(location=location, user=user)

    return user
