from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from config import VIDEO_PATH, MANAGER_USERNAME
from database import get_user
from keyboards import main_menu_kb

router = Router()

E_WELCOME = '<tg-emoji emoji-id="5368324170671202286">💼</tg-emoji>'
E_FIRE = '<tg-emoji emoji-id="5368324170671202286">🔥</tg-emoji>'
E_SHIELD = '<tg-emoji emoji-id="5368324170671202286">🛡</tg-emoji>'
E_HANDSHAKE = '<tg-emoji emoji-id="5368324170671202286">🤝</tg-emoji>'


@router.message(CommandStart())
async def cmd_start(message: Message):
    user = await get_user(message.from_user.id, message.from_user.username)
    caption = (
        f"{E_WELCOME} <b>Добро пожаловать в LOLZ Bot</b>\n\n"
        f"{E_FIRE} <i>Ваш надёжный P2P-гарант:</i>\n"
        "1️⃣ Автоматические сделки с NFT и подарками\n"
        f"2️⃣ {E_SHIELD} Полная защита обеих сторон\n"
        f"3️⃣ {E_SHIELD} Огромный функционал бота и сайта\n"
        f"4️⃣ {E_HANDSHAKE} Передача товаров через менеджера: {MANAGER_USERNAME}\n\n"
        "🔹 Выберите действие ниже 🔹"
    )
    try:
        video = FSInputFile(VIDEO_PATH)
        await message.answer_video(video=video, caption=caption,
                                   reply_markup=main_menu_kb(user["role"]), parse_mode="HTML")
    except Exception:
        await message.answer(caption, reply_markup=main_menu_kb(user["role"]), parse_mode="HTML")


@router.message(F.text == "🔙 В меню")
async def back_to_menu(message: Message):
    user = await get_user(message.from_user.id)
    await message.answer("Главное меню:", reply_markup=main_menu_kb(user["role"]))
