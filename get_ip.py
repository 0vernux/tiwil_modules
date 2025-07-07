from core import loader
import requests

@loader.tds
class GetIP(loader.Module):
    """Показывает твой внешний IP"""

    strings = {"name": "GetIP"}

    async def ipcmd(self, message):
        """Показывает твой внешний IP-адрес"""
        await message.edit("🔍 Получаю IP...")
        try:
            ip = requests.get("https://api.ipify.org").text.strip()
            await message.edit(f"🌐 Твой IP: <code>{ip}</code>", parse_mode="html")
        except Exception as e:
            await message.edit(f"❌ Ошибка получения IP:\n<code>{e}</code>", parse_mode="html")