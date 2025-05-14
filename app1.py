from botbuilder.core import Bot, TurnContext, MessageFactory, MemoryStorage, ConversationState
from botbuilder.schema import Activity, ActivityTypes
import asyncio

class EchoBot(Bot):
    async def on_turn(self, turn_context: TurnContext):
        if turn_context.activity.type == ActivityTypes.message:
            print(f"Usuario dice: {turn_context.activity.text}")
            await turn_context.send_activity(MessageFactory.text(f"Bot responde: Has dicho: '{turn_context.activity.text}'"))

async def main():
    # Simulación básica de un adaptador y contexto
    async def send_activity(activity: Activity):
        print(f"Enviando actividad: {activity.text}")

    class SimpleAdapter:
        async def send_activities(self, context: TurnContext, activities: list[Activity]):
            for activity in activities:
                await send_activity(activity)

        async def process_activity(self, activity: Activity, bot: Bot):
            turn_context = TurnContext(self, activity)
            await bot.on_turn(turn_context)

    adapter = SimpleAdapter()
    bot = EchoBot()

    # Simulación de un mensaje entrante
    activity = Activity(
        type=ActivityTypes.message,
        text="Hola Bot desde la consola"
    )

    await adapter.process_activity(activity, bot)

if __name__ == "__main__":
    asyncio.run(main())