import os
import asyncio
import datetime
import smtplib
from email.mime.text import MIMEText
from aiohttp import web
from typing import Callable
from config_canje import MAIL_ACCOUNTS
from botbuilder.core import (
    Bot,
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    TurnContext,
    MemoryStorage,
    ConversationState,
    UserState,
    MessageFactory,
    CardFactory,
)
from botbuilder.schema import Activity, ActivityTypes, HeroCard, CardAction, ActionTypes

# Cargar credenciales desde variables de entorno
# APP_ID = os.environ.get("MicrosoftAppId", "")
# APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
# print("App ID:", "✅ cargado" if APP_ID else "❌ vacío")
# print("App Password:", "✅ cargado" if APP_PASSWORD else "❌ vacío")

# # Crear adaptador del bot
# adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
# adapter = BotFrameworkAdapter(adapter_settings)

APP_ID = os.environ.get("MicrosoftAppId")
APP_PASSWORD = os.environ.get("MicrosoftAppPassword")
APP_Secret = os.environ.get("secreto")

print(f"App ID: {APP_ID}")
print(f"App Password: {APP_PASSWORD}")

#from botbuilder.core import BotFrameworkAdapterSettings

adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)

print("App ID:", "✅ cargado" if APP_ID else "❌ vacío")
print("App Password:", "✅ cargado" if APP_PASSWORD else "❌ vacío")

# Estado
memory = MemoryStorage()
conversation_state = ConversationState(memory)
user_state = UserState(memory)

import json
import urllib.parse




accent_color = "#FFC107"  # Amarillo ámbar
background_color = "#f0f8ff"  # Alice Blue (un azul muy claro)
bot_avatar_bg = "#007bff"  # Azul primario
user_avatar_bg = "#28a745"  # Verde éxitos
custom_styles = {
    "bubbleBackground": "#e0f7fa",  # Azul claro para las burbujas del bot
    "bubbleTextColor": "#1a237e",  # Azul oscuro para el texto del bot
    "userBubbleBackground": "#fffde7", # Amarillo muy claro para las burbujas del usuario
    "userBubbleTextColor": "#4a148c", # Morado oscuro para el texto del usuario
    "botAvatarImage": "URL_DEL_AVATAR_DE_TU_BOT",
    "userAvatarImage": "URL_DEL_AVATAR_DEL_USUARIO_POR_DEFECTO",
    "typingAnimationBackgroundColor": "#ffeb3b", # Amarillo brillante para la animación de escritura
    "sendButtonBackground": accent_color,
    "sendButtonColor": "#fff"
}
style_options_json = json.dumps(custom_styles)
encoded_style_options = urllib.parse.quote(style_options_json)

# ========================== BOT ==========================

class SupportBot(Bot):
    def __init__(self):
        self.count = 0

    async def on_turn(self, turn_context: TurnContext):
        if turn_context.activity.type == ActivityTypes.message:
            await self._handle_message(turn_context)
        elif turn_context.activity.type == ActivityTypes.conversation_update:
            await self._welcome_user(turn_context)

    async def _handle_message(self, turn_context: TurnContext):
        text = turn_context.activity.text.strip().lower()
        print(f"Mensaje recibido (en _handle_message): '{text}'")
        
        if text in ("hola", "hi", "iniciar"):
            print("Coincidencia con 'hola', 'hi' o 'iniciar' (inicial)")
            await turn_context.send_activity("¡Hola! ¿En qué puedo ayudarte hoy?")
            await self.show_menu(turn_context)
        elif text == "menu":
            print("Coincidencia con 'menu'")
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
            print("No hubo coincidencia")
            await turn_context.send_activity("No entendí. Escribe 'hola', 'iniciar' o 'menú' para ver opciones.")

    async def _welcome_user(self, turn_context: TurnContext):
        for member in turn_context.activity.members_added:
            if member.id != turn_context.activity.recipient.id:
                user_name = member.name  # Intentamos obtener el nombre del miembro

                if user_name:
                    await turn_context.send_activity(f"¡Hola, {user_name}! Soy el bot de soporte. Escribe 'hola' o 'menú' para comenzar.")
                else:
                    await turn_context.send_activity("¡Hola! Soy el bot de soporte. Escribe 'hola' o 'menú' para comenzar.")
                    
    async def show_menu(self, turn_context: TurnContext):
        card = HeroCard(
            title="Menú Principal",
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
        attachment = CardFactory.hero_card(card)
        await turn_context.send_activity(
            Activity(
                type=ActivityTypes.message,
                attachments=[attachment]
            )
        )
        
    async def show_documents(self, turn_context: TurnContext):
        documents = [
            {"title": "Documento de Requisitos del Proyecto", "link": "enlace_simulado_requisitos.pdf"},
            {"title": "Guía de Inicio Rápido", "link": "enlace_simulado_guia.pdf"},
            {"title": "Preguntas Frecuentes (FAQ)", "link": "enlace_simulado_faq.pdf"},
        ]
        response = "==== Documentos Disponibles ====\n\n"
        for i, doc in enumerate(documents):
            response += f"{i+1}. {doc['title']} (Descargar: {doc['link']})\n"
        response += "\nEscribe el número del documento para más detalles o 'salir'."
        await turn_context.send_activity(response)

    async def share_documents(self, turn_context: TurnContext):
        await turn_context.send_activity(
            "Envía tus documentos por correo electrónico a [dirección simulada]. Incluye una breve descripción.\n\n"
            "Esta función aún está en desarrollo."
        )
        
    # async def on_message_activity(self, turn_context: TurnContext):
    #         text = turn_context.activity.text.lower()
    #         if text == "hola" or text == "inicio" or text == "menu":
    #             await turn_context.send_activity("¡Aquí tienes el menú/inicio/saludo!")
    #         else:
    #             await turn_context.send_activity("No entendí. Escribe 'hola', 'iniciar' o 'menú' para ver opciones.")

    async def complete_forms(self, turn_context: TurnContext):
            card_json = {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.0",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": "Por favor, completa el siguiente formulario:",
                            "weight": "Bolder",
                            "size": "Medium"
                        },
                        {
                            "type": "Input.Text",
                            "id": "nombre",
                            "placeholder": "Tu nombre completo"
                        },
                        {
                            "type": "Input.Text",
                            "id": "email",
                            "placeholder": "Tu correo electrónico",
                            "style": "email"
                        },
                        {
                            "type": "Input.Number",
                            "id": "dni",
                            "placeholder": "Tu DNI"
                        }
                    ],
                    "actions": [
                        {
                            "type": "Action.Submit",
                            "title": "Enviar"
                        }
                    ]
                }
            attachment = CardFactory.adaptive_card(card_json)
            await turn_context.send_activity(
                    Activity(
                        type=ActivityTypes.message,
                        attachments=[attachment]
                    )
                )
            await turn_context.send_activity("La funcionalidad para completar formularios estará disponible pronto.")

    async def document_library(self, turn_context: TurnContext):
        await turn_context.send_activity("Accediendo a la biblioteca de documentos...")

    async def live_support(self, turn_context: TurnContext):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_id = turn_context.activity.from_property.id
        log_message = f"[{now}] Solicitud de soporte en vivo del usuario: {user_id}"
        print(log_message)

        with open("soporte_en_vivo.log", "a") as log_file:
            log_file.write(log_message + "\n")

        mail_account = MAIL_ACCOUNTS.get("mesa_entradas", {})
        sender_email = mail_account.get('email')
        sender_password = mail_account.get('password')
        receiver_email = "gberton1967@gmail.com"

        message = MIMEText(f"Solicitud de soporte en vivo del usuario ID: {user_id} a las {now}")
        message['Subject'] = f"Soporte en Vivo - Usuario {user_id}"
        message['From'] = sender_email
        message['To'] = receiver_email

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            print("Correo de soporte enviado.")
        except Exception as e:
            print(f"Error enviando correo: {e}")

        await turn_context.send_activity("Tu solicitud ha sido registrada. Un agente se contactará contigo pronto.")

bot = SupportBot()

# ========================== AIOHTTP ==========================

async def handle(request):
    path = request.path
    print(f"[{datetime.datetime.now()}] Request: {path}")

    if request.match_info.route.name == "messages":
        if "application/json" in request.headers.get("Content-Type", ""):
            try:
                body = await request.json()
                activity = Activity().deserialize(body)
                auth_header = request.headers.get("Authorization", "")
                response = await adapter.process_activity(activity, auth_header, bot.on_turn)
                if response:
                    return web.json_response(response.body, status=response.status)
                return web.Response(status=200)
            except Exception as e:
                print(f"Error procesando actividad: {e}")
                return web.json_response({"error": str(e)}, status=500)
        return web.Response(status=415)

    elif request.match_info.route.name == "root":
            #web_chat_url = f"https://webchat.botframework.com/embed/mi-nuevo-bot-ansv?s={APP_Secret}&botAvatarInitials=Bot&userAvatarInitials=User"
            # web_chat_url = f"https://webchat.botframework.com/embed/mi-nuevo-bot-ansv?s={WEBCHAT_SECRET}&botAvatarInitials=Bot&userAvatarInitials=User"
            web_chat_url = f"https://webchat.botframework.com/embed/mi-nuevo-bot-ansv?s={APP_Secret}&botAvatarInitials=Bot&userAvatarInitials=User&styleOptions={encoded_style_options}"
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Bienvenido Bot Activo</title>
                <script src="https://cdn.botframework.com/botframework-webchat/latest/webchat.js"></script>
                <style>
                    body {{
                        background-color: #0000FF;
                        color: #FFFFFF;
                        font-family: Monserrat, sans-serif;
                        font-size: 2.2em;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                    }}
                    #webchat-container {{
                        margin-top: 20px;
                        min-width: 400px;
                        width: 100%;
                        max-width: 800px;
                        min-height: 500px;
                        border: none;
                    }}
                    /* Media query para pantallas más pequeñas */
                    @media (max-width: 600px) {{
                        #webchat-container {{
                            min-width: 100%;
                            height: 70vh;
                        }}
                    }}
                </style>
            </head>
            <body>
                <h1>Bienvenido Bot Activo</h1>
                <iframe id="webchat-container" src="{web_chat_url}" scrolling="auto"></iframe>
                
            </body>
            </html>
            """
            return web.Response(text=html_content, content_type="text/html")
    #elif request.match_info.route.name == "root":    
    return web.Response(status=404)

app = web.Application()
app.router.add_post("/api/messages", handle, name="messages")
app.router.add_get("/", handle, name="root")

# ========================== MAIN ==========================

def main():
    port = int(os.environ.get("PORT", 8000))
    print(f"🌐 Servidor iniciado en http://0.0.0.0:{port}")
    try:
        web.run_app(app, host="0.0.0.0", port=port)
    except Exception as error:
        print(f"Error iniciando servidor: {error}")

if __name__ == "__main__":
    main()
