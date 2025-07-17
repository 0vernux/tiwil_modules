from core import loader
import random
import string

@loader.tds
class PasswordGenMod(loader.Module):
    """Генератор случайных паролей"""
    
    strings = {"name": "PasswordGen"}

    async def genpasscmd(self, message):
        """[длина] [nospec] — сгенерировать случайный пароль"""
        args = message.text.split()[1:]

        # Длина по умолчанию
        length = 12
        use_specials = True

        if args:
            try:
                # Проверяем число
                if args[0].isdigit():
                    length = int(args[0])
                    if length < 6 or length > 64:
                        return await message.edit("❗ Длина пароля должна быть от 6 до 64 символов.")
                    args = args[1:]
            except Exception:
                return await message.edit("❌ Укажи корректную длину пароля.")

        if args and "nospec" in args[0].lower():
            use_specials = False

        charset = string.ascii_letters + string.digits
        if use_specials:
            charset += "!@#$%^&*()-_=+[]{}<>?"

        password = ''.join(random.choice(charset) for _ in range(length))
        await message.edit(f"<b>🔐 Сгенерированный пароль:</b>\n<code>{password}</code>", parse_mode="html")