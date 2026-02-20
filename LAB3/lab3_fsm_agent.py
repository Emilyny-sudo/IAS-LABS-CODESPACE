import asyncio
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State

# Define states
class MonitoringState(State):
    async def run(self):
        print("🔍 State 1: Monitoring environment...")
        await asyncio.sleep(2)
        self.set_next_state("ALERT")

class AlertState(State):
    async def run(self):
        print("🚨 State 2: Alert triggered!")
        await asyncio.sleep(2)
        self.set_next_state("RESPONSE")

class ResponseState(State):
    async def run(self):
        print("🚑 State 3: Emergency response activated.")
        await asyncio.sleep(2)
        self.set_next_state("END")

class EndState(State):
    async def run(self):
        print("✅ State 4: Process complete.")
        await self.agent.stop()

class DisasterAgent(Agent):
    async def setup(self):
        print("🚀 FSM Agent starting...")

        fsm = FSMBehaviour()

        fsm.add_state(name="MONITOR", state=MonitoringState(), initial=True)
        fsm.add_state(name="ALERT", state=AlertState())
        fsm.add_state(name="RESPONSE", state=ResponseState())
        fsm.add_state(name="END", state=EndState())

        fsm.add_transition(source="MONITOR", dest="ALERT")
        fsm.add_transition(source="ALERT", dest="RESPONSE")
        fsm.add_transition(source="RESPONSE", dest="END")

        self.add_behaviour(fsm)

async def main():
    agent = DisasterAgent("agent@localhost", "password")
    await agent.start()
    await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())