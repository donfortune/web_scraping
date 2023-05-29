import time

import requests  #get page source and save as string
import selectorlib #extracts particular value btw h tags
import smtplib, ssl
from email.message import EmailMessage
import sqlite3

URL = "http://programmer100.pythonanywhere.com/tours/"



class Tours:
    def scrape(self, url):
        response = requests.get(URL)
        content = response.text
        return content

    def get_source(self, source):
        extractor = selectorlib.Extractor.from_yaml_file("source.yaml")
        value = extractor.extract(source)['tours']
        with open('tours.txt', 'a')  as file:
            file.write(value + '\n')
        return value


class SendMail:
    def send_email(self):
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

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("data.db")
    def store_to_database(self, get_source):
        row = get_source.split(',')
        row = [item.strip() for item in row ]
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
        self.connection.commit

    def read_data_db(self, get_source):
        row = get_source.split(',')
        row = [item.strip() for item in row ]
        band, city, date = row
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
        rows = cursor.fetchall()
        print(rows)
        return rows



if __name__ == "__main__":
    while True:
        tours = Tours()
        scrapped = tours.scrape(URL)
        extracted = tours.get_source(scrapped)
        extracted_info = f"The loaction and date for the next tour is: {extracted}"
        print(extracted_info)

        if extracted != 'No upcoming tours':
            if extracted not in 'tours.txt':
                sendmail = SendMail()
                sendmail.send_email()

        time.sleep(2)





