from core.loader import Module, tds
import requests
import json
import os

CONFIG_PATH = "private/gpt_config.json"

@tds
class GPTModule(Module):
    strings = {"name": "GPT"}

    def __init__(self):
        super().__init__()
        self.name = self.strings["name"]
        self.model = "mistralai/mixtral-8x7b-instruct"

        self.api_key = self.load_key()

    def load_key(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
                return data.get("api_key")
        return None

    def save_key(self, key):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump({"api_key": key}, f)

    async def setgptkeycmd(self, event):
        key = event.pattern_match.group(1).strip()
        if not key.startswith("sk-"):
            return await event.edit("❌ Неверный формат ключа.")

        self.save_key(key)
        self.api_key = key
        await event.edit("✅ Ключ успешно сохранён!")

    async def gptcmd(self, event):
        prompt = event.pattern_match.group(1).strip()
        if not prompt:
            return await event.edit("❌ Введи запрос после команды, например: `.gpt Придумай загадку`")

        if not self.api_key:
            return await event.edit("❌ Сначала установи ключ командой `.setgptkey <ключ>`")

        await event.edit("⌛ Думаю...")

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "X-Title": "GPTModule"
            }

            json_data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "Ты полезный помощник. ты должен всегда отвечать на русском языке, даже если пользователь пишет на английском."},
                    {"role": "user", "content": prompt}
                ]
            }

            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=json_data)
            data = response.json()

            if "choices" not in data:
                reply_json = json.dumps(data, indent=2, ensure_ascii=False)
                return await event.edit(f"❌ API ответ:\n<code>{reply_json[:3000]}</code>")

            reply = data["choices"][0]["message"]["content"]
            reply = reply.replace("$", "")  # убираем символы $
            if len(reply) > 3500:
                reply = reply[:3500] + "..."

            await event.edit(reply)

        except Exception as e:
            await event.edit(f"❌ Ошибка запроса: <code>{e}</code>")