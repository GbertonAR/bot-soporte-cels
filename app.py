from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, TurnContext, ActivityHandler
from botbuilder.schema import Activity, ActivityTypes
import os

print("APP_ID:", os.environ.get("MicrosoftAppId"))
print("APP_PASSWORD:", os.environ.get("MicrosoftAppPassword"))

APP_ID = os.environ.get("MicrosoftAppId")
APP_PASSWORD = os.environ.get("MicrosoftAppPassword")

print(f"App ID: {APP_ID}")
print(f"App Password: {APP_PASSWORD}")

from botbuilder.core import BotFrameworkAdapterSettings

adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)

class SaludoBot(ActivityHandler):
    async def on_members_added_activity(
        self,
        members_added,
        turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("¡Hola! Soy un bot de saludo simple.")

    async def on_message_activity(self, turn_context: TurnContext):
        await turn_context.send_activity("¡Hola! Gracias por tu mensaje.")

async def messages(req: web.Request) -> web.Response:
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return web.Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await adapter.process_activity(activity, auth_header, SaludoBot().on_turn)
    if response:
        return web.json_response(response.body, status=response.status)
    return web.Response(status=200)

async def index(req: web.Request):
    with open('index.html', 'r') as f:
        html_content = f.read()
    return web.Response(text=html_content, content_type='text/html')

async def main():
    app = web.Application()
    app.router.add_post("/api/messages", messages)
    port = int(os.environ.get("PORT", 8000))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    app = web.Application()
    app.router.add_post("/api/messages", messages)
    port = int(os.environ.get("PORT", 8000))
    web.run_app(app, host="0.0.0.0", port=port)