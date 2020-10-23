import os
import random

from application import db, Expense, HERE, application

from faker import Faker

fake = Faker()

categories = [
"Income",
"Paid",
"Loan Given",
"Loan Settled-up",
"Loan Taken",
"Loan Returned",
"Investment",
]


if bool(os.environ.get('DEBUG', '')):
    db.drop_all()

expenses = [
    Expense(
        item=fake.company(),
        amount=random.random() * random.randint(10, 1000),
        paid_to=fake.name(),
        category=random.choice(categories),
        date=fake.date_time_between(start_date="-5y", end_date="now", tzinfo=None),
        description=fake.text(100)
    ) for i in range(100)
]

db.create_all()
db.session.add_all(expenses)
db.session.commit()