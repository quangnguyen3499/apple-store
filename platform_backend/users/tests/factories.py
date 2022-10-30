from factory.django import DjangoModelFactory
from platform_backend.users.models import User
from faker import Factory

faker = Factory.create()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    uuid = faker.uuid4()
    email = faker.email() + "@gmail.com"
    first_name = faker.first_name()
    last_name = faker.last_name()
    password = 'abcd1234'
