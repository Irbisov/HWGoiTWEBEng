from datetime import datetime, timedelta
import random


# Функція для генерації випадкової дати в заданому діапазоні
def random_date():
    start_date = datetime(2023, 9, 1)
    end_date = datetime(2024, 5, 31)
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
