import re
import time

import requests
from bs4 import BeautifulSoup
import telegram_send



sleep_time = 60
url = "https://shopyphos.com/collections/tanzen"
api_id = ''
api_hash = ''
token = ''
phone = ""
event = "Sisyphos | 5. September"

def is_ticket_available():
    response = requests.get(
        url,
        headers={
            "cookie": '',
        },
        allow_redirects=True
    )
    soup = BeautifulSoup(response.content.decode("utf-8"), 'html.parser')
    products = soup.body.find_all("div", class_="grid-view-item")
    print(f"Found {len(products)} products.")
    # if len(products) > 5:
    #     return True
    for product in products:
        titles = product.find_all("div", class_="product-card__title")
        if len(titles) == 0: continue
        title = titles[0]
        if event in title.text and "grid-view-item--sold-out" not in product["class"]:
            return True
    return False

if __name__ == "__main__":
    hour_count = 0
    while True:
        try:
            if is_ticket_available():
                 telegram_send.send(messages=[f"There are tickets available for {event}!! Fucking buy"], conf="./config")
            if (hour_count + sleep_time) % (6 * 3600) == 0:
                telegram_send.send(messages=["Still alive, no worries."], conf="./config")
            hour_count += sleep_time
        except Exception as e:
            telegram_send.send(messages=["I died, something happened :(."], conf="./config")
        time.sleep(sleep_time)

    
