import requests

def obtener_token_direct_line(secret):
    response = requests.post(
        "https://directline.botframework.com/v3/directline/tokens/generate",
        headers={"Authorization": f"Bearer {secret}"}
    )
    return response.json()["token"]