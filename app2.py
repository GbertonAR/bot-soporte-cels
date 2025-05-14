from botbuilder.core import Bot, TurnContext, MessageFactory, MemoryStorage, ConversationState
from botbuilder.schema import Activity, ActivityTypes
import asyncio

import unicodedata

class SupportBot(Bot):
    async def on_turn(self, turn_context: TurnContext):
        if turn_context.activity.type == ActivityTypes.message:
            text = turn_context.activity.text.lower()
            text_sin_acentos = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

            if text_sin_acentos == "hola" or text_sin_acentos == "iniciar":
                await self.show_menu(turn_context)
            elif text == "1":
                await self.show_documents(turn_context)
            elif text == "2":
                await self.share_documents(turn_context)
            elif text == "3":
                await self.complete_forms(turn_context)  # Llamamos a una nueva función
            elif text == "4":
                await turn_context.send_activity(MessageFactory.text("Opción 4: Biblioteca de documentos (en desarrollo)"))
            elif text == "5":
                await turn_context.send_activity(MessageFactory.text("Opción 5: Soporte en vivo (en desarrollo)"))
            elif text_sin_acentos == "ayuda" or text_sin_acentos == "menu":
                await self.show_menu(turn_context)
            elif text_sin_acentos == "salir" or text_sin_acentos == "terminar" or text_sin_acentos == "adiós" or text_sin_acentos == "adios":
                await turn_context.send_activity(MessageFactory.text("Gracias por tu consulta. ¡Hasta luego!"))
            else:
                await turn_context.send_activity(MessageFactory.text("Lo siento, no entendí. Escribe 'hola', 'iniciar' o 'menú' para ver las opciones."))
        elif turn_context.activity.type == ActivityTypes.conversation_update:
            if not turn_context.activity.members_added == turn_context.activity.members_removed:
                await self.show_menu(turn_context)

    async def show_menu(self, turn_context: TurnContext):
        menu = (
            "Por favor, elige una opción:\n\n"
            "1. Obtener documentos\n"
            "2. Compartir documentos\n"
            "3. Completar formularios\n"
            "4. Biblioteca de documentos\n"
            "5. Soporte en vivo\n\n"
            "Escribe el número de la opción que deseas o 'salir' para terminar."
        )
        await turn_context.send_activity(MessageFactory.text(menu))

    async def show_documents(self, turn_context: TurnContext):
        documents = [
            {"title": "Documento de Requisitos del Proyecto", "link": "enlace_simulado_requisitos.pdf"},
            {"title": "Guía de Inicio Rápido", "link": "enlace_simulado_guia.pdf"},
            {"title": "Preguntas Frecuentes (FAQ)", "link": "enlace_simulado_faq.pdf"},
        ]

        response = "Aquí tienes algunos documentos disponibles:\n\n"
        for i, doc in enumerate(documents):
            response += f"{i+1}. {doc['title']} (Descargar: {doc['link']})\n"

        response += "\nEscribe el número del documento para más detalles (funcionalidad no implementada en esta versión) o 'salir' para terminar."
        await turn_context.send_activity(MessageFactory.text(response))

    async def share_documents(self, turn_context: TurnContext):
        response = (
            "Para compartir documentos, puedes enviarlos por correo electrónico a [dirección de correo electrónico simulada].\n\n"
            "Por favor, asegúrate de incluir una breve descripción del documento que estás compartiendo.\n\n"
            "Esta funcionalidad está en desarrollo y la recepción de documentos no está automatizada en esta versión."
        )
        await turn_context.send_activity(MessageFactory.text(response))

    async def complete_forms(self, turn_context: TurnContext):
        response = (
            "Puedes encontrar los formularios para completar en el siguiente enlace:\n\n"
            "[enlace simulado a la página de formularios]\n\n"
            "Por favor, sigue las instrucciones proporcionadas en la página para completar y enviar los formularios."
        )
        await turn_context.send_activity(MessageFactory.text(response))

async def main():
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
    bot = SupportBot()  # Usamos nuestra nueva clase de bot

    # Simulación de un mensaje entrante para mostrar el menú al inicio
    activity = Activity(
        type=ActivityTypes.conversation_update,
        members_added=[Activity()] # Simula que el bot se une a la conversación
    )
    await adapter.process_activity(activity, bot)

    while True:
        user_input = input("Escribe tu opción: ")
        user_activity = Activity(
            type=ActivityTypes.message,
            text=user_input
        )
        await adapter.process_activity(user_activity, bot)

if __name__ == "__main__":
    asyncio.run(main())