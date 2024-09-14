import asyncio
import websockets


async def listen():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            command = input("Enter a command (use command 'help'): ")
            await websocket.send(command)
            response = await websocket.recv()
            print(f"Server response: {response}")


if __name__ == "__main__":
    asyncio.run(listen())
