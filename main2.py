import requests
import smtplib
from bs4 import BeautifulSoup
import os

my_gmail = os.environ['MY_GMAIL']
gmail_smtp = os.environ['GMAIL_SMTP']
gpassword = os.environ['GPASSWORD']

ITEM_WEBSITE = 'https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6'
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": "\"Not)A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"127\", \"Chromium\";v=\"127\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
}

amazon_item = (requests.get(ITEM_WEBSITE, headers=headers)).text
soup = BeautifulSoup(amazon_item, 'html.parser')

product_name = " ".join((soup.find(id='productTitle').getText()).split())
price_dollars = soup.find('span', class_='a-price-whole').getText()
price_cents = soup.find('span', class_='a-price-fraction').getText()

print(f"{product_name[:70]}... currently costs ${price_dollars}{price_cents}")

price = int(float(price_dollars))

if price <= 100:
    with smtplib.SMTP(gmail_smtp) as connection:
        connection.starttls()
        # tls means transport layer security
        connection.login(user=my_gmail, password=gpassword)
        connection.sendmail(
            from_addr=my_gmail,
            to_addrs=my_gmail,
            msg=f"Subject:Price Alert!\n\nYour item is below your target price!\n{ITEM_WEBSITE}"
        )
