from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from time import sleep

def fetch_book(url="https://anylang.net/ru/books/de/malenkiy-princ/read"):
    driver = webdriver.Chrome()
    driver.get(url)
    sleep(2)
    try:
        skip_btn = driver.find_element(By.CLASS_NAME, "enjoyhint_skip_btn")
        skip_btn.click()
        print("Skip btn clicked")
    except NoSuchElementException:
        print("Skip btn not found")
    sleep(2)

    pages = []

    initial_html = driver.page_source
    soup = BeautifulSoup(initial_html, "html.parser")
    source_pages = soup.find_all(class_="page")
    for source_page in source_pages:
        if source_page.text != "loading":
            pages.append(source_page)

    height = driver.execute_script("return document.body.scrollHeight")
    previousOffset = 0
    tries = 0

    while True:
        initial_html = driver.page_source
        soup = BeautifulSoup(initial_html, "html.parser")
        source_pages = soup.find_all(class_="page")
        for source_page in source_pages:
            pass


        driver.execute_script("window.scrollBy(0, 1000);")
        scroll_offset = driver.execute_script("return window.pageYOffset")

        if scroll_offset >= height:
            print("Scrolled to bottom")
            break
        elif scroll_offset == previousOffset:
            tries = tries + 1
        if tries >= 3:
            print("Scrolling stoped")
            break
        previousOffset = scroll_offset

    previousOffset = 0
    tries = 0
    # sleep(10)

def print_pages(pages):
    for page in pages:
        print(page.text)

def write_pages(pages):
    tmp = [page.text for page in pages]
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(tmp))

def main():
    fetch_book()

if __name__ == '__main__':
    main()