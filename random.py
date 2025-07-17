import random
from core import loader

@loader.tds
class Randomizer(loader.Module):
    """Рандомайзер чисел и элементов"""
    strings = {"name": "Randomizer"}

    async def randcmd(self, message):
        """Выдаёт случайное число или элемент"""
        args = message.text.split()[1:]

        if not args:
            return await message.edit("❗ Укажи диапазон чисел или список элементов.")

        if len(args) == 2 and all(arg.lstrip('-').isdigit() for arg in args):
            start, end = map(int, args)
            if start > end:
                start, end = end, start
            number = random.randint(start, end)
            return await message.edit(f"🎲 Случайное число от {start} до {end}: <code>{number}</code>", parse_mode="html")
        else:
            choice = random.choice(args)
            return await message.edit(f"🎲 Случайный выбор: <code>{choice}</code>", parse_mode="html")