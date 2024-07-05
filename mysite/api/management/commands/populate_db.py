import random
from django.core.management.base import BaseCommand
from api.models import User, Contact, Spam
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting old data...')
        self._clear_data()

        self.stdout.write('Creating new data...')
        self._create_users()
        self._create_contacts()
        self._create_spams()

        self.stdout.write('Database population complete.')

    def _clear_data(self):
        User.objects.all().delete()
        Contact.objects.all().delete()
        Spam.objects.all().delete()

    def _create_users(self):
        for _ in range(10):
            user = User.objects.create_user(
                name=fake.name(),
                phone_number=fake.phone_number(),
                password='password123',
                email=fake.email()
            )
            user.save()

    def _create_contacts(self):
        users = User.objects.all()
        for user in users:
            for _ in range(random.randint(5, 15)):
                contact = Contact.objects.create(
                    name=fake.name(),
                    phone_number=fake.phone_number(),
                    user=user
                )
                contact.save()

    def _create_spams(self):
        users = User.objects.all()
        for _ in range(20):
            user = random.choice(users)
            spam = Spam.objects.create(
                phone_number=fake.phone_number(),
                marked_by=user
            )
            spam.save()
