from core.loader import Module, tds
import requests

@tds
class WeatherModule(Module):
    """Прогноз погоды через OpenWeather"""
    strings = {"name": "Weather"}

    def __init__(self):
        super().__init__()
        self.name = self.strings["name"]
        self.api_key = "7c9f1d584b3b1afcaea70a61002ee561"  # твой ключ
        self.api_url = "http://api.openweathermap.org/data/2.5/weather"

    async def wtrcmd(self, event):
        city = event.pattern_match.group(1).strip()
        if not city:
            return await event.edit("❌ Укажи город, например: `.wtr Минск`")

        await event.edit("⛅ Получаю погоду...")

        try:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",
                "lang": "ru"
            }
            response = requests.get(self.api_url, params=params)
            data = response.json()

            if data.get("cod") != 200:
                return await event.edit(f"❌ Город не найден: <code>{city}</code>")

            name = data["name"]
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            description = data["weather"][0]["description"].capitalize()
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]

            text = (
                f"🌍 <b>{name}</b>\n"
                f"🌡 Температура: <b>{temp}°C</b>\n"
                f"🤔 Ощущается как: <b>{feels_like}°C</b>\n"
                f"💧 Влажность: <b>{humidity}%</b>\n"
                f"🌬 Ветер: <b>{wind} м/с</b>\n"
                f"☁️ Состояние: <b>{description}</b>"
            )

            await event.edit(text, parse_mode="html")
        except Exception as e:
            await event.edit(f"❌ Ошибка запроса: <code>{e}</code>")