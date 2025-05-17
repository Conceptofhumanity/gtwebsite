from flask import *
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random

wait_time = 5
iterations = 50
text = """
hello this is a lot of text a large amount of text to translate so it'll actually have interesting results
"""
app = Flask(__name__)

@app.route('/translate_text', methods=['POST'])  

def translate_text():  
    #nabs the text from the website, yk request.get dunno what json is about
    text = request.json.get('text')  
    result = translate(text['text'], text['iterations'])  
    return jsonify({"translated_text": result})  

def translate():
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
            #if each language has been used, reset the language pool
            if not available_languages:
                available_languages = languages.copy()
            lang = random.choice(available_languages)
            available_languages.remove(lang)

            #go to google translate
            driver.get(f"https://translate.google.com/?sl=auto&tl={lang}")

            #find input box, type text.
            input_box = driver.find_element(By.CLASS_NAME, "er8xn")
            input_box.clear()
            input_box.send_keys(current_text)

            time.sleep(wait_time) #wait a moment or else it would just bam bam bam not work
                
            #grab and print translation text
            results = driver.find_elements(By.CLASS_NAME, "ryNqvb")
            current_text = "\n".join([result.text for result in results])
                
            print(f"Translation #{i+1}, Language: {lang}")
            print(f"Result: {current_text}\n")

        #Translate back to english
        driver.get("https://translate.google.com/?sl=auto&tl=en")
        input_box = driver.find_element(By.CLASS_NAME, "er8xn")
        input_box.clear()
        input_box.send_keys(current_text)

        time.sleep(wait_time)

        results = driver.find_elements(By.CLASS_NAME, "ryNqvb")
        final_text = "\n".join([result.text for result in results])

        print(f"Final Translation: \n {current_text}")

    except Exception as e:
        print(f"Error in translation (i+1): {e}")
        return jsonify({'error':str(e)})
    
    finally:
        #exit google translate
        driver.quit

if __name__ == '__main__':
    app.run(debug=True)
