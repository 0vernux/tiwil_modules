from core import loader

@loader.tds
class CalculatorMod(loader.Module):
    """Вычисляет простые математические выражения"""

    strings = {"name": "Calculator"}

    async def calccmd(self, message):
        """Использование: .calc <выражение>"""
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            return await message.edit("❗ Укажи выражение для вычисления.")

        expression = args[1]

        try:
            # Ограниченное eval с безопасной средой
            result = eval(expression, {"__builtins__": None}, {})
            await message.edit(f"🧮 <b>{expression}</b> = <code>{result}</code>", parse_mode="html")
        except Exception as e:
            await message.edit(f"❌ Ошибка вычисления:\n<code>{e}</code>", parse_mode="html")