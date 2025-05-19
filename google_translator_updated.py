from flask import *
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
from flask_cors import CORS


app = Flask(__name__)
CORS(app) 
wait_time = 5
@app.route('/translate', methods=['POST'])  

def translate():
    print("Incoming JSON:", request.get_json())
    data = request.get_json()
    current_text = data.get('text', '')
    print(current_text)
    iterations = int(data.get('iterations', 100))

    driver = webdriver.Chrome()
    languages = [
        'ja', 'ko', 'ru', 'ar', 'hi', 'es', 'fr', 'en', 'bg', 'cs',
        'pl', 'sk', 'zh', 'gu', 'zh-TW', 'af', 'ar', 'da', 'de', 'id', 'it',
        'fa', 'nl'
    ]


    try:
        available_languages = languages.copy()
        if iterations == "":
            iterations = 10
        for i in range(iterations):
            if not available_languages:
                available_languages = languages.copy()
            lang = random.choice(available_languages)
            available_languages.remove(lang)

            driver.get(f"https://translate.google.com/?sl=auto&tl={lang}")

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

        print(f"Final Translation: \n {final_text}")
        return jsonify({"translated_text": final_text}) 

    except Exception as e:
        print(f"Error in translation (i+1): {e}")
        return jsonify({'error':str(e)})
    
    finally:
        #exit google translate
        driver.quit

if __name__ == '__main__':
    app.run(debug=True)


    app.run(debug=True)
