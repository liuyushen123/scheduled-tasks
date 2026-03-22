##################### Extra Hard Starting Project ######################
import datetime as dt
import os
import random
from email.message import EmailMessage
from smtplib import SMTP

import pandas as pd

FILE_PATH = f"letter_templates/letter_{random.randint(1, 10)}.txt"

today = (dt.datetime.now().month, dt.datetime.now().day, dt.datetime.now().year)
current_month = today[0]
current_day = today[1]
current_year = today[2]

my_email = os.environ["MY_EMAIL"]
my_password = os.environ["MY_PASSWORD"]


def send_email(to_email, name, content):

    msg = EmailMessage()
    msg["Subject"] = "Happy Birthday!"
    msg["From"] = my_email
    msg["To"] = to_email

    msg.set_content(content)

    with SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(my_email, my_password)
        connection.send_message(msg)


def calculate_person_age(n):
    n = abs(n)
    if 10 <= n % 100 <= 13:
        return f"{n}th"

    last_digit = n % 10

    if last_digit == 1:
        return f"{n}st"
    elif last_digit == 2:
        return f"{n}nd"
    elif last_digit == 3:
        return f"{n}rd"
    else:
        return f"{n}th"


birthday_data = pd.read_csv("birthdays.csv")
todays_birthday = birthday_data[
    (birthday_data["month"] == current_month) & (birthday_data["day"] == current_day)
]

for index, person in todays_birthday.iterrows():
    try:
        with open(FILE_PATH) as file:
            letter_template = file.read()
            letter_template = (
                letter_template.replace("[NAME]", person["name"])
                .replace("Angela", "Best Regards\nYuchen")
                .replace("[AGE]", calculate_person_age(current_year - person["year"]))
            )
            print(letter_template)
            send_email(person["email"], person["name"], letter_template)
    except Exception as e:
        print(f"Error: {e}")
        raise
