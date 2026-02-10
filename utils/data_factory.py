# utils/data_factory.py
from faker import Faker
import random

fake = Faker()

class UserFactory:
    @staticmethod
    def build(overrides: dict = None) -> dict:
        """
        Returns a complete dict matching the API's createAccount params.
        Pass overrides to customise specific fields.
        """
        user = {
            "name": fake.name(),
            "email": f"test_{fake.uuid4()[:8]}@testmail.com",  # unique every time
            "password": "Test@1234!",
            "title": random.choice(["Mr", "Mrs", "Miss"]),
            "birth_date": str(fake.day_of_month()),
            "birth_month": str(fake.month()),
            "birth_year": str(fake.year()),
            "firstname": fake.first_name(),
            "lastname": fake.last_name(),
            "company": fake.company(),
            "address1": fake.street_address(),
            "address2": fake.secondary_address(),
            "country": "United States",
            "zipcode": fake.zipcode(),
            "state": fake.state(),
            "city": fake.city(),
            "mobile_number": fake.phone_number()[:15],
        }
        if overrides:
            user.update(overrides)
        return user