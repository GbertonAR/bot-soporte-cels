import asyncio
import sys
import os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'botnormativa', 'canje')))
#print(sys.path)
from typing import Callable
from config_canje import MAIL_ACCOUNTS
from botbuilder.core import (
    Bot,
    BotAdapter,
    BotFrameworkAdapter,
    ConversationState,
    MemoryStorage,
    TurnContext,
    UserState,
)
from botbuilder.schema import Activity, ActivityTypes, ActionTypes, HeroCard, CardAction
#from botbuilder.core.adapters import SimpleAdapter  # Ya no lo usaremos directamente
#from botbuilder.dialogs import DialogSet, WaterfallDialog, TextPrompt, DialogTurnResult
from botbuilder.core import Bot, BotAdapter, BotFrameworkAdapter, ConversationState, MemoryStorage, TurnContext, UserState, MessageFactory, CardFactory
# from botbuilder.schema import ActionTypes, HeroCard, CardAction
from aiohttp import web

class SupportBot(Bot):
    def __init__(self):
        self.count = 0

    async def on_turn(self, turn_context: TurnContext):
        if turn_context.activity.type == ActivityTypes.message:
            text = turn_context.activity.text.lower()
            if text in ("hola", "hi", "iniciar"):
                await turn_context.send_activity("¡Hola! ¿En qué puedo ayudarte hoy?")
                await self.show_menu(turn_context)
            elif text == "menu":
                await self.show_menu(turn_context)
            elif text == "1":
                await self.show_documents(turn_context)
            elif text == "2":
                await self.share_documents(turn_context)
            elif text == "3":
                await self.complete_forms(turn_context)
            elif text == "4":
                await self.document_library(turn_context)
            elif text == "5":
                await self.live_support(turn_context)
            elif text == "salir":
                await turn_context.send_activity("Gracias por tu consulta. ¡Hasta luego!")
            else:
                await turn_context.send_activity("Lo siento, no entendí. Escribe 'hola', 'iniciar' o 'menú' para ver las opciones.")
        elif turn_context.activity.type == ActivityTypes.conversation_update:
            for member in turn_context.activity.members_added:
                if member.id != turn_context.activity.recipient.id:
                    await turn_context.send_activity("¡Hola! Soy el bot de soporte. Escribe 'hola' o 'menú' para comenzar.")

    async def show_menu(self, turn_context: TurnContext):
        print("Mostrando menú")
        card = HeroCard(
            title="**Menú Principal**",
            text="Por favor, elige una opción:",
            buttons=[
                CardAction(type=ActionTypes.im_back, title="1. Obtener documentos", value="1"),
                CardAction(type=ActionTypes.im_back, title="2. Compartir documentos", value="2"),
                CardAction(type=ActionTypes.im_back, title="3. Completar formularios", value="3"),
                CardAction(type=ActionTypes.im_back, title="4. Biblioteca de documentos", value="4"),
                CardAction(type=ActionTypes.im_back, title="5. Soporte en vivo", value="5"),
                CardAction(type=ActionTypes.im_back, title="Salir", value="salir"),
            ],
        )
        reply = MessageFactory.attachment(CardFactory.hero_card(card))
        print(f"Contenido del reply: {reply}")
        await turn_context.send_activity(reply)

    async def show_documents(self, turn_context: TurnContext):
        documents = [
            {"title": "**Documento de Requisitos del Proyecto**", "link": "enlace_simulado_requisitos.pdf"},
            {"title": "**Guía de Inicio Rápido**", "link": "enlace_simulado_guia.pdf"},
            {"title": "**Preguntas Frecuentes (FAQ)**", "link": "enlace_simulado_faq.pdf"},
        ]
        response = "==== Documentos Disponibles ====\n\n"
        for i, doc in enumerate(documents):
            response += f"{i+1}. {doc['title']} (Descargar: {doc['link']})\n"
        response += "\nEscribe el número del documento para más detalles (funcionalidad no implementada en esta versión) o 'salir' para terminar."
        await turn_context.send_activity(response)

    async def share_documents(self, turn_context: TurnContext):
        await turn_context.send_activity(
            "Para compartir documentos, puedes enviarlos por correo electrónico a [dirección de correo electrónico simulada].\n\n"
            "Por favor, asegúrate de incluir una breve descripción del documento que estás compartiendo.\n\n"
            "Esta funcionalidad está en desarrollo y la recepción de documentos no está automatizada en esta versión."
        )

    async def complete_forms(self, turn_context: TurnContext):
        await turn_context.send_activity("La funcionalidad para completar formularios estará disponible próximamente.")

    async def document_library(self, turn_context: TurnContext):
        await turn_context.send_activity("Accediendo a la biblioteca de documentos...")

    # async def live_support(self, turn_context: TurnContext):
    #     await turn_context.send_activity("Conectando con un agente de soporte en vivo...")
        
    async def live_support(self, turn_context: TurnContext):
            import datetime
            import smtplib
            from email.mime.text import MIMEText

            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"[{timestamp}] Solicitud de soporte en vivo del usuario: {turn_context.activity.from_property.id}"
            print(f"REGISTRO: {log_message}")
            with open("soporte_en_vivo.log", "a") as log_file:
                log_file.write(log_message + "\n")

            # Configuración del correo electrónico
            #             email_address = mail_account_config.get('email')
            # password = mail_account_config.get('password')
            
            # smtp_server = mail_account_config.get('SMTP_SERVER')
            # port = mail_account_config.get('PORT')
            mail_account_config = MAIL_ACCOUNTS.get("mesa_entradas")
            sender_email = mail_account_config.get('email')  # Reemplaza con tu dirección
            sender_password = mail_account_config.get('password')  # Reemplaza con tu contraseña o contraseña de aplicación
            receiver_email = "gberton1967@gmail.com"  # Reemplaza con la dirección del agente

            message = MIMEText(f"Se ha recibido una solicitud de soporte en vivo del usuario con ID: {turn_context.activity.from_property.id} a las {timestamp}")
            message['Subject'] = f"Solicitud de Soporte en Vivo - Usuario {turn_context.activity.from_property.id}"
            message['From'] = sender_email
            message['To'] = receiver_email

            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:  # Cambia el servidor y el puerto si no usas Gmail
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, receiver_email, message.as_string())
                print("Correo electrónico de notificación enviado.")
            except Exception as e:
                print(f"Error al enviar el correo electrónico: {e}")

            await turn_context.send_activity("Se ha registrado tu solicitud de soporte en vivo. Un agente se pondrá en contacto contigo a la brevedad.")
        
bot = SupportBot()

# adapter = SimpleAdapter(bot)  # Comenta o elimina esta línea

MEMORY = MemoryStorage()
CONVERSATION_STATE = ConversationState(MEMORY)
USER_STATE = UserState(MEMORY)

# adapter = BotFrameworkAdapter(
#     settings={
#         "APP_ID": os.environ.get("MicrosoftAppId", ""),
#         "APP_PASSWORD": os.environ.get("MicrosoftAppPassword", ""),
#     }
# )

# adapter = BotFrameworkAdapter(
#     settings={
#         "app_credentials": {
#             "app_id": os.environ.get("MicrosoftAppId", ""),
#             "app_password": os.environ.get("MicrosoftAppPassword", ""),
#         }
#     }
# )

adapter = BotFrameworkAdapter(settings={})

async def messages(req: web.Request) -> web.Response:
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return web.Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await adapter.process_activity(activity, auth_header, bot.on_turn)
    if response:
        return web.json_response(response.body, status=response.status)
    return web.Response(status=200)


# app = web.Application()
# app.router.add_post("/api/messages", handle, name="messages")
# app.router.add_get("/", handle, name="root")

async def handle(request):
    if request.match_info.route.name == "messages":
        # Handle bot messages
        body = await request.json()
        activity = Activity().deserialize(body)
        auth_header = request.headers.get("Authorization", "")
        response = await adapter.process_activity(activity, auth_header, bot.on_turn)
        if response:
            return web.json_response(response.body, status=response.status)
        return web.Response(status=200)
    elif request.match_info.route.name == "root":
        # Serve the welcome HTML page
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Bienvenido Bot Activo</title>
            <style>
                body {
                    background-color: #0000FF; /* Azul */
                    color: #FFFFFF; /* Blanco */
                    font-family: Monserrat, sans-serif;
                    font-size: 2.2em; /* Tamaño mediano */
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    font-family: sans-serif;
                }
            </style>
        </head>
        <body>
            <h1>Bienvenido Bot Activo</h1>
        </body>
        </html>
        """
        return web.Response(text=html_content, content_type="text/html")
    return web.Response(status=404)

app = web.Application()
app.router.add_post("/api/messages", handle, name="messages")
app.router.add_get("/", handle, name="root")

# app = web.Application()
# app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    try:
        web.run_app(app, host="0.0.0.0", port=port)
    except Exception as error:
        print(f"Error starting server: {error}")
        raise error
    
# # === Iniciar servidor ===
# if __name__ == "__main__":
#     app.run(debug=False)    