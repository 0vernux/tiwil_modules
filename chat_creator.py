"""
создает группы, каналы по команде
• .create g/s/c
"""
from telethon import events, functions

def setup(bot):
    pattern = r"^\.\s*create\s+(?P<type>[gsc])"  # Базовый паттерн
    pattern += r"(?:\s+(?P<title>[^\|]+))?"  # Опциональное название
    pattern += r"(?:\s*\|\s*(?P<description>.+))?"  # Опциональное описание

    @bot.client.on(events.NewMessage(pattern=pattern))
    async def create_chat_handler(event):
        args = event.pattern_match
        chat_type = args["type"]
        title = args["title"] or "Новый чат"
        description = args["description"] or ""

        try:
            if chat_type == "g":  # Группа
                await bot.client(functions.messages.CreateChatRequest(
                    users=[],
                    title=title
                ))
                await event.edit(f"✅ Группа **{title}** создана!")

            elif chat_type == "s":  # Супергруппа
                await bot.client(functions.channels.CreateChannelRequest(
                    title=title,
                    about=description,
                    megagroup=True
                ))
                await event.edit(f"✅ Супергруппа **{title}** создана!")

            elif chat_type == "c":  # Канал
                await bot.client(functions.channels.CreateChannelRequest(
                    title=title,
                    about=description,
                    megagroup=False
                ))
                await event.edit(f"✅ Канал **{title}** создан!")

        except Exception as e:
            await event.edit(f"❌ Ошибка: {str(e)}")

    # Добавляем в help
    bot.modules["chat_creator"] = {
        "name": "Создание чатов",
        "description": "Создаёт группы/каналы по команде .create g/s/c",
        "commands": [".create"]
    }
