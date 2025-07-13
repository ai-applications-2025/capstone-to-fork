import asyncio
import websockets
import json
import os

# Adjust this to match your game engine's WebSocket server address
WEBSOCKET_URL = "ws://ai.thewcl.com:8700"


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def format_cell(value, index):
    upper = str(value).upper()
    return upper if upper in ["X", "O"] else str(index)


def render_board(positions):
    def row(start):
        return f" {format_cell(positions[start], start)} | {format_cell(positions[start + 1], start + 1)} | {format_cell(positions[start + 2], start + 2)} "

    line = "---+---+---"
    print(row(0))
    print(line)
    print(row(3))
    print(line)
    print(row(6))
    print()


async def listen_for_updates():
    async with websockets.connect(WEBSOCKET_URL) as ws:
        print(f"Connected to {WEBSOCKET_URL}")
        async for message in ws:
            try:
                data = json.loads(message)
                positions = data.get("positions")
                if isinstance(positions, list) and len(positions) == 9:
                    clear_terminal()
                    render_board(positions)
                else:
                    print("Invalid board data received.")
            except json.JSONDecodeError:
                print("Received non-JSON message.")


if __name__ == "__main__":
    asyncio.run(listen_for_updates())
