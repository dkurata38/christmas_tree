from time import sleep

from selene.driver import SeleneDriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import requests


def extract_image_url_from_google_data_set(image_count):

    options = Options()
    options.add_argument("--headless")
    driver = SeleneDriver.wrap(Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options))

    url = "https://storage.googleapis.com/openimages/web/visualizer/index.html?set=train&c=%2Fm%2F025nd"
    driver.get(url)
    pull_down_elements = driver.find_all("tt-selectable")

    for pull_down_element in pull_down_elements:
        if pull_down_element.text == "Christmas tree":
            pull_down_element.click()
            break

    sleep(10)

    image_elements = driver.find_all(".img-overlay-wrap img")
    image_urls = []
    for i in range(0, image_count - 1, 1):
        image_element = image_elements.__getitem__(i)
        image_url = image_element.get_attribute("data-src")

        if image_url is not None:
            image_urls.append(str(image_url))

    driver.quit()
    return image_urls


urls = extract_image_url_from_google_data_set(2)

for target in urls: # imagesからtargetに入れる
    re = requests.get(target)
    filename = 'img/' + target.split("/")[-1].replace("?", "")

    with open('img/' + target.split('/')[-1], 'wb') as f: # imgフォルダに格納
        f.write(re.content) # .contentにて画像データとして書き込む
 
print("ok") # 確認
