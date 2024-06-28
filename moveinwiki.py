from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def main():
    # Инициализация браузера
    driver = webdriver.Chrome()

    try:
        while True:
            query = input("Введите запрос для поиска на Википедии: ")
            if not query:
                break

            search_wikipedia(driver, query)

            while True:
                print("\nВыберите действие:")
                print("1. Листать параграфы текущей статьи")
                print("2. Перейти на страницу из списка поиска")
                print("3. Показать все ссылки в текущей статье")
                print("4. Выйти из программы")
                action = input("Введите номер действия: ")

                if action == '1':
                    scroll_through_paragraphs(driver)
                elif action == '2':
                    visit_search_result_page(driver)
                elif action == '3':
                    list_all_links_in_article(driver)
                elif action == '4':
                    print("Выход из программы.")
                    return
                else:
                    print("Некорректный выбор, попробуйте снова.")
    finally:
        driver.quit()


def search_wikipedia(driver, query):
    driver.get("https://ru.wikipedia.org/")
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "search"))
    )
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "mw-content-text"))
    )
    time.sleep(2)


def scroll_through_paragraphs(driver):
    paragraphs = driver.find_elements(By.TAG_NAME, 'p')
    for p in paragraphs:
        print(p.text)
        user_input = input("Нажмите Enter для продолжения или 'q' для выхода: ")
        if user_input.lower() == 'q':
            break


def visit_search_result_page(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mw-search-results"))
        )
        search_results = driver.find_element(By.CLASS_NAME, "mw-search-results")
        links = search_results.find_elements(By.CLASS_NAME, "mw-search-result-heading")
        for i, link in enumerate(links):
            title = link.text
            url = link.find_element(By.TAG_NAME, 'a').get_attribute('href')
            print(f"{i + 1}. {title} - {url}")

        choice = input("Введите номер ссылки для перехода: ")
        try:
            choice = int(choice) - 1
            if 0 <= choice < len(links):
                driver.get(links[choice].find_element(By.TAG_NAME, 'a').get_attribute('href'))
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "mw-content-text"))
                )
                time.sleep(2)
            else:
                print("Некорректный выбор, попробуйте снова.")
        except ValueError:
            print("Некорректный ввод, попробуйте снова.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def list_all_links_in_article(driver):
    try:
        content = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "mw-content-text"))
        )
        links = content.find_elements(By.TAG_NAME, 'a')
        for i, link in enumerate(links):
            title = link.get_attribute('title')
            url = link.get_attribute('href')
            if title and url:
                print(f"{i + 1}. {title} - {url}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
