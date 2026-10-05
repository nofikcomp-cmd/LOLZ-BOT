from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards import verification_kb

router = Router()


@router.message(F.text == "🌐 Верификация")
async def show_verification(message: Message):
    text = (
        "🛡️ <b>ПРОГРАММА ВЕРИФИКАЦИИ LOLZ OTC</b>\n\n"
        "<b>ПРЕИМУЩЕСТВА ВЕРИФИКАЦИИ:</b>\n"
        "🛡️ 0% комиссии на вывод\n"
        "⚡ Вывод в течение часа\n"
        "🔒 Без дополнительных проверок\n\n"
        "💲 <b>ОСОБОЕ УСЛОВИЕ:</b>\n"
        "При покупке верификации, полная стоимость вернется на ваш баланс!\n\n"
        "<b>СТОИМОСТЬ ВЕРИФИКАЦИИ:</b>\n"
        "• 💳 Карта РФ: 1000 RUB\n"
        "• 💲 USDT (TON): 13 USDT\n"
        "• 💎 GRAM (TON): 13 GRAM\n"
        "• 🇰🇿 KZT: 5600 KZT\n"
        "• 🇧🇾 BYN: 40 BYN\n"
        "• ⭐ Stars: 900 Stars\n\n"
        "После оплаты отправьте чек для подтверждения"
    )
    await message.answer(text, reply_markup=verification_kb(), parse_mode="HTML")


@router.callback_query(F.data == "verification_menu")
async def verification_menu_cb(cb: CallbackQuery):
    await cb.message.delete()
    await show_verification(cb.message)
    await cb.answer()


@router.callback_query(F.data.startswith("pay_"))
async def pay_stub(cb: CallbackQuery):
    await cb.answer("Оплата временно недоступна. Обратитесь в поддержку.", show_alert=True)