import os
from pymongo import MongoClient
from decouple import config

# Отримання значень з середовища
mongo_username = os.getenv('MONGO_USERNAME')
mongo_password = os.getenv('MONGO_PASSWORD')

# Створення строки підключення до MongoDB
mongo_uri = f"mongodb+srv://{mongo_username}:{mongo_password}@cluster0.xik54.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Підключення до MongoDB через pymongo
client = MongoClient(mongo_uri, ssl=True)

# Вибір бази даних
db = client['your_database_name']

# Приклад використання: отримання колекції
collection = db['your_collection_name']

# Виконання операцій з колекцією
result = collection.find_one()  # приклад запиту
print(result)
