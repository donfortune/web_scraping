import time

import requests  #get page source and save as string
import selectorlib #extracts particular value btw h tags
import smtplib, ssl
from email.message import EmailMessage
import sqlite3

URL = "http://programmer100.pythonanywhere.com/tours/"

connection = sqlite3.connect("data.db")


def scrape(url):
    response = requests.get(URL)
    content = response.text
    return content

def get_source(source):
    extractor = selectorlib.Extractor.from_yaml_file("source.yaml")
    value = extractor.extract(source)['tours']
    with open('tours.txt', 'a')  as file:
        file.write(value + '\n')
    return value


def send_email():
    host = "smtp.gmail.com"
    port = 465
    username = 'donfortunet.df@gmail.com'
    password = 'dqpeojyayhvpcvcy'
    receiver_email = 'osowoayiobi@gmail.com'
    message = EmailMessage()
    message['Subject'] = 'New Location Found'
    message.set_content(extracted_info)


    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=context) as file:
        file.login(username, password)
        file.sendmail(username, receiver_email, message.as_string())
        file.quit()

def store_to_database(get_source):
    row = get_source.split(',')
    row = [item.strip() for item in row ]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit

def read_data_db(get_source):
    row = get_source.split(',')
    row = [item.strip() for item in row ]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    rows = cursor.fetchall()
    print(rows)
    return rows



if __name__ == "__main__":
    while True:
        scrapped = scrape(URL)
        extracted = get_source(scrapped)
        extracted_info = f"The loaction and date for the next tour is: {extracted}"
        print(extracted_info)

        if extracted != 'No upcoming tours':
            if extracted not in 'tours.txt':
                send_email()

        time.sleep(2)





