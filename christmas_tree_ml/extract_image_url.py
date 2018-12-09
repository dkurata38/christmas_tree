import re
from itertools import tee
from time import sleep
from urllib.parse import unquote

import requests
from selene.driver import SeleneDriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def extract_image_url_from_google_image_search(image_count: int):
    options = Options()
    options.add_argument("--headless")
    driver = SeleneDriver.wrap(Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options))

    url = "https://www.google.co.jp/search?q=%E6%9C%A8+%E7%94%BB%E5%83%8F&tbm=isch&source=lnt&tbs=itp:photo&sa=X&ved=0ahUKEwiYiY_gw5HfAhXIVbwKHWwfBK0QpwUIIA&biw=1280&bih=290&dpr=2"
    driver.get(url)

    def scroll():
        def scroll_unit(prev_count: int):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(10)
            image_elements = driver.find_elements(By.CSS_SELECTOR, "div.rg_bx.rg_di.rg_el.ivg-i")
            current_count = len(image_elements)
            print(current_count)

            # 前回検索結果と今回検索結果で数が同じ場合は今取得できた要素数で結果を返す.
            # 検索済みの要素数が要求された数に達したら, 今取得できた要素分だけurlを返す.
            if current_count == prev_count or current_count >= image_count:
                decoded_urls = []
                for image_element in image_elements:
                    image_anchor_element = image_element.find_element(By.CSS_SELECTOR, "a.rg_l")
                    if image_anchor_element is None:
                        continue
                    image_href_text = str(image_anchor_element.get_attribute("href"))
                    encoded_url = re.sub(r".+imgurl=([^&]+).*", "\\1", image_href_text)
                    decoded_urls.append(unquote(encoded_url))
                    if len(decoded_urls) == image_count:
                        break
                return decoded_urls

            # 検索済みの要素数が要求された数に満たない場合はもう一度スクロールをする.
            if current_count < image_count:
                return scroll_unit(current_count)
        return scroll_unit(0)
    return scroll()


def extract_image_url_from_google_data_set(image_count):

    options = Options()
    options.add_argument("--headless")
    driver = SeleneDriver.wrap(Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options))

    url = "https://www.google.com/search?biw=981&bih=563&tbm=isch&sa=1&ei=2l8MXKWVFYyH8wXBxoDwBQ&q=%E3%82%AF%E3%83%AA%E3%82%B9%E3%83%9E%E3%82%B9%E3%83%84%E3%83%AA%E3%83%BC+%E5%AE%B6%E5%BA%AD%E7%94%A8&oq=%E3%82%AF%E3%83%AA%E3%82%B9%E3%83%9E%E3%82%B9%E3%83%84%E3%83%AA%E3%83%BC+%E5%AE%B6%E5%BA%AD%E7%94%A8&gs_l=img.3..0l2j0i8i30l2j0i24.2293.5032..5521...3.0..0.74.628.9......1....1..gws-wiz-img.......0i4i37j0i4i37i24j0i23j0i8i30i23j0i24i23.6Nxkfgj1YN0"
    driver.get(url)
    pull_down_elements = driver.find_all(".tt-selectable")

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


urls = extract_image_url_from_google_data_set(100)

for i, target in enumerate(urls): # imagesからtargetに入れる
    response = requests.get(target)
    name_and_extension = re.sub(r"(.+)(\?.+)", "\\1", target.split("/")[-1]).split(".")
    if len(name_and_extension) == 1:
        continue

    filename = 'img/' + str(i) + "." + name_and_extension[1]

    with open(filename, 'wb') as f: # imgフォルダに格納
        f.write(response.content) # .contentにて画像データとして書き込む
 
print("ok") # 確認
