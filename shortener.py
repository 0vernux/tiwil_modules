from core import loader
import requests

@loader.tds
class ShortenerMod(loader.Module):
    """Сокращает ссылки через is.gd"""
    strings = {"name": "Shortener"}

    async def shortcmd(self, message):
        """Сокращает ссылку: .short <ссылка>"""
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            return await message.edit("❗ Укажи ссылку для сокращения.")
        
        url = args[1].strip()

        try:
            response = requests.get("https://is.gd/create.php", params={"format": "simple", "url": url})
            short_link = response.text.strip()
            if short_link.startswith("Error:"):
                await message.edit(f"❌ Ошибка: {short_link}")
            else:
                await message.edit(f"🔗 Сокращённая ссылка:\n{short_link}")
        except Exception as e:
            await message.edit(f"❌ Не удалось сократить ссылку:\n<code>{e}</code>", parse_mode="html")