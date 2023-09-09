from selenium import webdriver
import os

from selenium.webdriver.common.by import By
from dotenv import load_dotenv, find_dotenv


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv(find_dotenv())


USER = os.environ.get("MONGO_USER")
PASSWORD = os.environ.get("MONGO_PASSWORD")
HOSTNAME = os.environ.get("MONGO_HOSTNAME")

uri = f"mongodb+srv://{USER}:{PASSWORD}@{HOSTNAME}/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


consulta = "Mazda CX-5"

driver = webdriver.Chrome()
driver.get("https://ecuador.patiotuerca.com/")
search_box = driver.find_element(by=By.CSS_SELECTOR, value="#search-list")

search_box.send_keys(consulta)
print("hola1")

search_button = driver.find_element(by=By.CSS_SELECTOR, value="#openSearch > div > div > div.search-ots.false > img")
search_button.click()
print("hola2")

vehicle_cards = driver.find_elements(By.CSS_SELECTOR, "#featuredUsed > div.xl3")

print("hola")
for card in vehicle_cards:
    try:
        title = card.find_element(By.CSS_SELECTOR, "div > div > div > div.card-info.card-content > div.module.tittle").text
        kms_y_city = card.find_element(By.CSS_SELECTOR, "div > div > div > div.card-info.card-content > div.latam-secondary-text.text-lighten-2.left.vehicle-highlight").text
        price = card.find_element(By.CSS_SELECTOR, "div > div > div > div.card-info.card-content > strong").text
        print(title)
        print(kms_y_city)
        print(f"${price}")

        coche_actual = {

            "title": title,
            "kms_y_city": kms_y_city,
            "price": price,

        }

        mydb = client["proyecto"]
        carros_collection = mydb["carros"]
        x = carros_collection.insert_one(coche_actual)

        # db = mongo_client.get_database('db_eig')
        #collection = db.get_collection(f'patiotuerca')

        #collection.insert_one(coche_actual)

        print("++++++++++++++++++++++++++++++++")
    except Exception as e:
        print(e)
        print("++++++++++++++++++++++++++++++++")


driver.close()