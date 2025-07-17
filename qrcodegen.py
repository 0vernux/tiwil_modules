from core import loader
from io import BytesIO

try:
    import qrcode
except ImportError:
    qrcode = None

@loader.tds
class QRGen(loader.Module):
    """Генерация QR-кода из текста"""
    strings = {"name": "QRGen"}

    async def qrcmd(self, message):
        """Создаёт QR-код: .qr <текст или ссылка>"""
        if qrcode is None:
            return await message.edit(
                "❌ Не установлен модуль <code>qrcode</code>.\n"
                "Установи его: <code>pip install qrcode[pil]</code>"
            )

        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            return await message.edit("❗ Укажи текст для генерации QR-кода.")

        text = args[1]

        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        await message.client.send_file(
            message.chat_id,
            buffer,
            reply_to=message.id
        )
        await message.delete()