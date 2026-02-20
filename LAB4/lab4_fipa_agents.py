import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

# SENSOR AGENT
class SensorAgent(Agent):
    class MonitorBehaviour(CyclicBehaviour):
        async def run(self):
            msg = Message(to="dispatcher@localhost")  # send to dispatcher
            msg.set_metadata("performative", "inform")
            msg.body = "Flood Alert: Level High!"
            print(f"📡 SensorAgent: Sending INFORM -> {msg.body}")
            await self.send(msg)
            await asyncio.sleep(5)  # wait 5 seconds before next alert

    async def setup(self):
        print("🚀 SensorAgent starting...")
        self.add_behaviour(self.MonitorBehaviour())

# DISPATCHER AGENT
class DispatcherAgent(Agent):
    class DispatcherBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                print(f"📨 DispatcherAgent: Received {msg.get_metadata('performative')} -> {msg.body}")
                # Send REQUEST to ResponseAgent
                response_msg = Message(to="responder@localhost")
                response_msg.set_metadata("performative", "request")
                response_msg.body = f"Respond to: {msg.body}"
                print(f"📤 DispatcherAgent: Sending REQUEST -> {response_msg.body}")
                await self.send(response_msg)

    async def setup(self):
        print("🚀 DispatcherAgent starting...")
        self.add_behaviour(self.DispatcherBehaviour())

# RESPONSE AGENT
class ResponseAgent(Agent):
    class RespondBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                print(f"🚑 ResponseAgent: Received REQUEST -> {msg.body}")
                print("✅ ResponseAgent: Action taken!")

    async def setup(self):
        print("🚀 ResponseAgent starting...")
        self.add_behaviour(self.RespondBehaviour())

# MAIN FUNCTION
async def main():
    sensor = SensorAgent("sensor@localhost", "password")
    dispatcher = DispatcherAgent("dispatcher@localhost", "password")
    responder = ResponseAgent("responder@localhost", "password")

    await sensor.start()
    await dispatcher.start()
    await responder.start()

    await asyncio.sleep(20)  # run for 20 seconds
    await sensor.stop()
    await dispatcher.stop()
    await responder.stop()
    print("\n✅ Lab 4 Agents finished communication.")

if __name__ == "__main__":
    asyncio.run(main())