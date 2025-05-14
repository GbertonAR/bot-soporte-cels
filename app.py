from botbuilder.adapters import ConsoleAdapter
from botbuilder.core import (
    Bot,
    TurnContext,
    MessageFactory,
    ConversationState,
    MemoryStorage
)


from botbuilder.schema import Activity, ActivityTypes
from typing import List, Dict, Any
import asyncio

class EchoBot(Bot):
    async def on_turn(self, turn_context: TurnContext):
        if turn_context.activity.type == ActivityTypes.message:
            await turn_context.send_activity(MessageFactory.text(f"Has dicho: '{ turn_context.activity.text }'"))

async def main():
    # Crear adaptador.
    adapter = ConsoleAdapter()  # Modifica esta línea

    # Crear estado de conversación.
    memory = MemoryStorage()
    conversation_state = ConversationState(memory)

    # Crear el bot.
    bot = EchoBot()

    # Simular una conversación (esto se reemplazará con la conexión al emulador).
    async def message_handler(activity: Activity):
        turn_context = TurnContext(adapter, activity)
        await bot.on_turn(turn_context)

    # Ejemplo de un mensaje entrante.
    activity = Activity(
        type=ActivityTypes.message,
        text="Hola Bot"
    )

    await message_handler(activity)

if __name__ == "__main__":
    asyncio.run(main())