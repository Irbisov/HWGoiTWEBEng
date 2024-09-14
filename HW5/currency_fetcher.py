import aiohttp


API_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date="

VALID_CURRENCIES = ["USD", "EUR", "GBP"]  # Додайте необхідні валюти


class CurrencyRateFetcher:
    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()

    async def fetch_rates(self, date: str, currencies: list):
        """Отримати курси валют за обрану дату."""
        url = f"{API_URL}{date}"

        # Перевірка валют
        for currency in currencies:
            if currency not in VALID_CURRENCIES:
                return f"Невідома валюта: {currency}"

        try:
            print(f"Запит до API за датою {date} і валютами {currencies}. URL: {url}")
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()

                    # Перевірка, чи є у відповіді ключ 'exchangeRate'
                    if 'exchangeRate' not in data:
                        print(f"Помилка: API повернуло неочікуваний формат даних: {data}")
                        return "Помилка отримання даних з API."

                    filtered_data = self.filter_currencies(data['exchangeRate'], currencies)
                    if filtered_data:
                        return filtered_data
                    else:
                        return "Помилка: Валюти не знайдено в даних API."
                else:
                    print(f"Помилка отримання даних з API: {response.status} - {await response.text()}")
                    return f"Помилка отримання даних з API: {response.status}"
        except aiohttp.ClientError as e:
            print(f"Помилка мережі: {e}")
            return "Помилка мережі при отриманні курсів валют."

    def filter_currencies(self, data, currencies):
        """Фільтрація курсів валют за обраними валютами."""
        filtered_rates = {}
        for entry in data:
            # Перевірка, чи є в entry необхідні ключі
            currency_code = entry.get('currency')
            if currency_code in currencies:
                filtered_rates[currency_code] = {
                    'sale': entry.get('saleRate', entry.get('saleRateNB')),
                    'purchase': entry.get('purchaseRate', entry.get('purchaseRateNB'))
                }
        return filtered_rates
