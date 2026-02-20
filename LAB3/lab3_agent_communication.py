import asyncio
import datetime

class ReceiverAgent:
    async def receive_message(self, message):
        time = datetime.datetime.now()
        print(f"[{time}] 📩 ReceiverAgent received message: {message}")


class SenderAgent:
    def __init__(self, receiver):
        self.receiver = receiver

    async def send_message(self):
        time = datetime.datetime.now()
        message = "Disaster Alert: High Flood Risk Detected!"
        print(f"[{time}] 📤 SenderAgent sending message...")
        await asyncio.sleep(2)
        await self.receiver.receive_message(message)


async def main():
    receiver = ReceiverAgent()
    sender = SenderAgent(receiver)

    print("🚀 Lab 3 Agent Communication Started...\n")
    await sender.send_message()
    print("\n✅ Communication Complete.")


if __name__ == "__main__":
    asyncio.run(main())