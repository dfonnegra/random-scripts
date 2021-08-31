import re
import time

import requests
from bs4 import BeautifulSoup
import telegram_send



sleep_time = 60
url = "https://shopyphos.com/collections/tanzen"
api_id = '6481175'
api_hash = '833525a9d3e2960dac734f03cf674164'
token = '1816841495:AAGo2RqHKNuYtUfxCjiWXrD9y4sIoxB5cK0'
phone = "+4915735633867"
event = "Sisyphos | 27. August"

def is_ticket_available():
    response = requests.get(
        url,
        headers={
            "cookie": '_y=4aad59c3-e2d9-4a4d-ae87-e0c332f492a0; _shopify_y=4aad59c3-e2d9-4a4d-ae87-e0c332f492a0; secure_customer_sig=; cart_currency=EUR; _orig_referrer=; _landing_page=/collections/tanzen; _s=5500f5dc-17e4-4d37-9615-f647ae88da9f; _shopify_s=5500f5dc-17e4-4d37-9615-f647ae88da9f; _shopify_sa_p=; fsb_previous_pathname=/collections/tanzen; locksmith-params={"geonames_feature_ids":[2921044,6255148],"geonames_feature_ids:signature":"e28b076e850ebae7ed833066f9bc965fa911510e3b73ad66a842dd5f56fb0c7c"}; cart=832f20515fde3380777c14bbf6490a2a; cart_ts=1629632429; cart_sig=6de4567153712774997bd37628b04b0d; cart_ver=gcp-us-east1:1; fsb_total_price_381844=0; scapp_now=2; _shopify_sa_t=2021-08-22T11:40:30.237Z; scapp_next=3',
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
        if title.text == event and "grid-view-item--sold-out" not in product["class"]:
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

    