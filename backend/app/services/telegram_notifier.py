import os
import httpx
from dotenv import load_dotenv

load_dotenv()

def send_telegram_message(text):
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}

    try:
        with httpx.Client(timeout=3) as client:
            response = client.post(url, json=payload)

        data = response.json()

        if response.status_code == 200 and data.get("ok") is True:
            return "success"

        if response.status_code == 401:
            return "invalid_token"

        if response.status_code == 400:
            description = data.get("description", "").lower()
            if "chat not found" in description:
                return "invalid_chat_id"

        if response.status_code == 403:
            description = data.get("description", "").lower()
            if "bot was blocked by the user" in description:
                return "user_blocked_bot"

        if data.get("ok") is False:
            return "telegram_ok_false"

        return "unknown_telegram_error"

    except httpx.ConnectError:
        return "connection_error"

    except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.WriteTimeout):
        return "timeout_error"

    except httpx.HTTPError:
        return "general_http_error"