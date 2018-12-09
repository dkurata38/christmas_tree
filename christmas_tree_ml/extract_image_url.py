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

    url = "https://www.google.com/search?biw=981&bih=563&tbm=isch&sa=1&ei=2l8MXKWVFYyH8wXBxoDwBQ&q=%E3%82%AF%E3%83%AA%E3%82%B9%E3%83%9E%E3%82%B9%E3%83%84%E3%83%AA%E3%83%BC+%E5%AE%B6%E5%BA%AD%E7%94%A8&oq=%E3%82%AF%E3%83%AA%E3%82%B9%E3%83%9E%E3%82%B9%E3%83%84%E3%83%AA%E3%83%BC+%E5%AE%B6%E5%BA%AD%E7%94%A8&gs_l=img.3..0l2j0i8i30l2j0i24.2293.5032..5521...3.0..0.74.628.9......1....1..gws-wiz-img.......0i4i37j0i4i37i24j0i23j0i8i30i23j0i24i23.6Nxkfgj1YN0"
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


urls = extract_image_url_from_google_data_set(100)

for target in urls: # imagesからtargetに入れる
    re = requests.get(target)
    filename = 'img/' + target.split("/")[-1].replace("?", "")

    with open(filename, 'wb') as f: # imgフォルダに格納
        f.write(re.content) # .contentにて画像データとして書き込む
 
print("ok") # 確認
