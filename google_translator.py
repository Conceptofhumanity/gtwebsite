#remember to make a program that automatically google translates text
#like 20 times. 
#I'm not paying for this.
#I'm not paying for this.
#I'm not paying for this.
#I'm not paying for this.
#I'm not paying for this.
#aI????? anyways, timme to make it manually enter the text into google translate and copy the result
#translating it again.
#I'm not paying for this.
#I'm not paying for this.
#I'm not paying for this.
#I'm not paying for this.
#I'm not paying for this.
#I'm not paying for this.
#I'm not paying for this.
#I'm not paying for this.
#I'm not paying for this.
#I'm not paying for this.
#I'm not paying for this.

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random

def translate(text, iterations=5):
    driver = webdriver.Chrome()
    languages = [
        'ja', 'ko', 'ru', 'ar', 'hi', 'es', 'fr', 'en', 'bg', 'cs',
        'pl', 'sk', 'zh', 'gu', 'zh-TW', 'af', 'ar', 'da', 'de', 'id', 'it',
        'fa', 'nl'
    ]
    current_text = text
    try:
        available_languages = languages.copy()
        for i in range(iterations):
            try:
                #lang = languages[random.randint(0, len(languages)-1)]
                if not available_languages:
                    available_languages = languages.copy()
                lang = random.choice(available_languages)
                available_languages.remove(lang)
                driver.get(f"https://translate.google.com/?sl=auto&tl={lang}")
                input_box = driver.find_element(By.CLASS_NAME, "er8xn")
                input_box.clear()
                input_box.send_keys(current_text)

                time.sleep(wait_time)

                results = driver.find_elements(By.CLASS_NAME, "ryNqvb")
                current_text = "\n".join([result.text for result in results])

                print(f"Translation #{i+1}, Language: {lang}")
                print(f"Result: {current_text}\n")
            except Exception as e:
                print(f"Error in translation (i+1): {e}")
                continue
    finally:
        driver.get("https://translate.google.com/?sl=auto&tl=en")
        input_box = driver.find_element(By.CLASS_NAME, "er8xn")
        input_box.clear()
        input_box.send_keys(current_text)

        time.sleep(wait_time)

        results = driver.find_elements(By.CLASS_NAME, "ryNqvb")
        current_text = "\n".join([result.text for result in results])

        print(f"Final Translation: \n {current_text}")
        driver.quit()

text = """
Test message test message hi I eat rabbits sometimes no I dont that was i lie i do like cats, hats, bats, mats, tats, and rats though.
"""
iterations = 50
wait_time = 7
#make a website that contains this, along with some other text based t hings, like checking text for words in the Bible.
translate(text, iterations)