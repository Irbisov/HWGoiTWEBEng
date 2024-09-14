import asyncio
import websockets
from currency_fetcher import CurrencyRateFetcher
from aiofile import AIOFile
from datetime import datetime
import traceback

LOG_FILE = 'exchange_log.txt'


async def log_command(command, response=None):
    async with AIOFile(LOG_FILE, 'a') as afp:
        log_entry = f"{datetime.now()}: Command: {command}"
        if response:
            log_entry += f" | Response: {response}"
        await afp.write(log_entry + '\n')


async def log_connection(client_ip, status):
    async with AIOFile(LOG_FILE, 'a') as afp:
        await afp.write(f"{datetime.now()}: Client {client_ip} {status}\n")


def format_rates(rates):
    if not rates:
        return "No rates available."

    formatted = "\n" + "=" * 40 + "\n"
    for date, rate_info in rates.items():
        formatted += f"Date: {date}\n"
        formatted += "-" * 40 + "\n"
        for currency, details in rate_info.items():
            if isinstance(details, dict):
                formatted += f"{currency}:\n"
                formatted += f"  Purchase: {details.get('purchase', 'N/A'):.2f} | Sale: {details.get('sale', 'N/A'):.2f}\n"
            else:
                formatted += f"{currency}: {details:.2f}\n"
        formatted += "-" * 40 + "\n"
    formatted += "=" * 40 + "\n"
    return formatted


async def handle_current_command(websocket, currencies):
    async with CurrencyRateFetcher() as fetcher:
        try:
            rates = await fetcher.fetch_rates(datetime.now().strftime("%d.%m.%Y"), currencies)
            if rates:
                response = format_rates(rates)
            else:
                response = "Error fetching current rates."
            await websocket.send(response)
            await log_command(f"current {' '.join(currencies)}", response)
        except Exception as e:
            error_message = f"Error while fetching current rates: {str(e)}"
            await websocket.send(error_message)
            await log_command(f"current {' '.join(currencies)}", error_message)


async def handle_exchange_command(websocket, days, currencies):
    try:
        if days > 10:
            await websocket.send("You can only request rates for up to 10 days.")
            return

        async with CurrencyRateFetcher() as fetcher:
            rates = await fetcher.get_rates_for_last_days(days, currencies)
            response = format_rates(rates)
            await websocket.send(response)
            await log_command(f"exchange {days} {' '.join(currencies)}", response)
    except Exception as e:
        error_message = f"Error while fetching exchange rates: {str(e)}"
        await websocket.send(error_message)
        await log_command(f"exchange {days} {' '.join(currencies)}", error_message)


async def handle_help_command(websocket):
    try:
        help_text = (
            "Available commands:\n"
            "1. `current <currency1> <currency2>` - Get current exchange rates for specified currencies.\n"
            "2. `exchange <days> <currency1> <currency2>` - Get exchange rates for the last <days> days.\n"
            "3. `help` - Show this help message."
        )
        await websocket.send(help_text)
        await log_command("help", help_text)
    except Exception as e:
        error_message = f"Error while sending help: {str(e)}"
        await websocket.send(error_message)
        await log_command("help", error_message)


async def command_handler(websocket, message):
    try:
        parts = message.split()
        command = parts[0]
        if command == 'current':
            if len(parts) < 2:
                await websocket.send("Please specify at least one currency.")
                return
            currencies = parts[1:]
            await handle_current_command(websocket, currencies)
        elif command == 'history':
            if len(parts) < 3:
                await websocket.send("Please specify the number of days and at least one currency.")
                return
        elif command == 'exchange':
            if len(parts) < 3:
                await websocket.send("Please specify the number of days and at least one currency.")
                return
            try:
                days = int(parts[1])
                currencies = parts[2:]
                await handle_exchange_command(websocket, days, currencies)
            except ValueError:
                await websocket.send("Invalid number of days specified. Please provide a valid integer.")
        elif command == 'help':
            await handle_help_command(websocket)
        else:
            await websocket.send("Unknown command. Use 'help' to get a list of available commands.")
    except Exception as e:
        error_message = f"Error processing command '{message}': {str(e)}"
        await websocket.send(error_message)
        await log_command("error", error_message)


async def handler(websocket, path):
    client_ip = websocket.remote_address[0]
    await log_connection(client_ip, "connected")
    try:
        async for message in websocket:
            await command_handler(websocket, message)
    except websockets.ConnectionClosed as e:
        await log_connection(client_ip, f"disconnected (reason: {e})")
    except Exception as e:
        error_trace = traceback.format_exc()
        await websocket.send(f"An internal error occurred: {str(e)}")
        await log_command("error", error_trace)
        await log_connection(client_ip, f"disconnected (reason: {e})")


async def main():
    start_server = websockets.serve(handler, "localhost", 8765)
    await start_server
    print("WebSocket server started on ws://localhost:8765")
    await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
