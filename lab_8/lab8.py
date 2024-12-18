from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time
from datetime import date
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.edge.options import Options

options = Options()
options.add_argument('--ignore-certificate-errors')

service = Service(r"D:\Vlad\Все ДЗ(2)\Python\bomba-python\msedgedriver.exe")
driver = webdriver.Edge(service=service, options=options)

def extract_dates_and_headlines(filtered_c_feed_log_y):
    list_with_converted_time = []
    for index in range(1, len(filtered_c_feed_log_y), 2):
        date_from_list = filtered_c_feed_log_y[index]
        filtered_c_feed_log_y_no_time = date_from_list.split(', ')
        for elem in filtered_c_feed_log_y_no_time[1::2]:
            data_object = datetime.strptime(elem, "%d.%m.%y")
            formatted_date = data_object.strftime("%Y-%m-%d")
            list_with_converted_time.append(formatted_date)
            text_from_list = filtered_c_feed_log_y[index - 1]
            list_with_converted_time.append(text_from_list)
    return list_with_converted_time

def TSN():
    today = date.today()
    print(today)

    driver.get("https://tsn.ua/en")
    key_phrase = "war"

    dictionary = {}

    try:
        cookie_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]"))
        )
        cookie_button.click()
    except Exception as e:
        print("Не вдалося знайти або закрити банер cookie:", e)

    while True:
        c_feed_log_y = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@class='c-feed-log--y c-feed-log--y-start c-feed-log--md']"))
        )

        filtered_c_feed_log_y = c_feed_log_y.text.split('\n')[1::2]
        list_with_conwerted_time = extract_dates_and_headlines(filtered_c_feed_log_y)

        for index in range(0, len(list_with_conwerted_time), 2):
            data_object = datetime.strptime(list_with_conwerted_time[index], "%Y-%m-%d")
            differenceInData = today - data_object.date()
            print(differenceInData)
            if differenceInData.days > 170:
                print("Новини старші за 6 місяців, вихід із циклу.")
                print(dictionary)
                return

            month = data_object.month
                
            if key_phrase in list_with_conwerted_time[index + 1]:
                if month not in dictionary:
                    dictionary[month] = []
                if month in dictionary:
                    dictionary[month].append(list_with_conwerted_time[index + 1])
        print(dictionary)

        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@class='i-before i-arrow-ltr i-arrow--sm i-before--spacer-l']"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            next_button.click()
        except ElementClickInterceptedException:
            print("Помилка натискання кнопки: перехоплення елемента.")
            break
        except Exception as e:
            print("Помилка при натисканні кнопки Next:", e)
            break

TSN()

time.sleep(10000)
driver.quit()
