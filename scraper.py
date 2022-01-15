from bs4 import BeautifulSoup
import requests
import smtplib
import sys
import time


class Tracker:

    def __init__(self, url, target_price, email):
        self.url = url
        self.target_price = target_price
        self.email = email
        self.personalID = ""
        self.password = ""
        self.headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
        }

        self.connection = smtplib.SMTP('smtp.gmail.com', 587)
        self.connection.ehlo()
        self.connection.starttls()
        self.connection.ehlo()
        self.connection.login(self.personalID, self.password)
        self.driver()

    def check_price(self):
        # returns all the date from the website:
        self.page = requests.get(self.url, headers=self.headers)

        soup = BeautifulSoup(self.page.content, 'html.parser')

        self.title = soup.find(id="productTitle").get_text().strip()

        self.price = soup.find("span", {"class": "a-price-whole"}).get_text()

        self.converted_price = float(self.price[:-1].replace(",", ""))

        if self.converted_price < float(self.target_price):
            self.send_email()

    def send_email(self):
        subject = f"The price of {self.title} fell down"
        body = f"Please Check the following link \n\n {self.url} "

        self.msg = f"Subject : {subject} \n\n {body}"

        self.connection.sendmail(
            'abhinavkhanna05@gmail.com',
            self.email,
            self.msg
        )

        print("The Email has been sent")
        self.connection.quit()
        sys.exit()

    def driver(self):
        while True:
            self.check_price()
            print("Will Check tomorrow Now")
            time.sleep(10)


def main():
    print("Welcome to Amazon Price Tracker")
    print("Enter the URL of the Product")
    url = input()
    print("Enter the target price")
    price = input()
    print("enter the email to notify")
    email = input()
    try:
        Tracker(url, price, email)
    except KeyboardInterrupt:
        sys.exit()


if __name__ == '__main__':
    main()
