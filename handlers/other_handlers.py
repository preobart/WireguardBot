from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.content_type.in_({"text", "photo", "video", "sticker", "document", "audio", "voice", "animation"}))
async def send_photo(message: Message):
    photo_id = "AgACAgIAAxkBAAIBfGe2M88BoIzIsMZlt0b-IY72bXBaAAL56jEbrZqwSddAntg8-2pRAQADAgADeAADNgQ"
    await message.answer_photo(photo_id)
