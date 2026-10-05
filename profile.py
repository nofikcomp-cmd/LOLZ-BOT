from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from database import get_user, set_requisite
from keyboards import profile_kb, balance_kb, back_kb
from states import ReqStates

router = Router()


@router.message(F.text == "👤 Мой профиль")
async def show_profile(message: Message):
    u = await get_user(message.from_user.id)
    text = (
        "🏆 <b>ПРОФИЛЬ LOLZ Bot</b>\n\n"
        f"👤 Имя: @{message.from_user.username or 'Нет'}\n"
        f"⭐ Рейтинг: 5.0/5.0\n"
        f"✅ Успешных сделок: {u['deals']} | Споров выиграно: 0\n"
        f"📊 Активных сделок: 0\n\n"
        "💰 <b>Баланс:</b>\n"
        f"• 💎 Gram: {u['gram']}\n"
        f"• 🇷🇺 Rub: {u['rub']}\n"
        f"• 🇺🇸 Usd: {u['usd']}\n"
        f"• 💲 Usdt: {u['usdt']}\n"
        f"• ⭐ Stars: {u['stars']}"
    )
    await message.answer(text, reply_markup=profile_kb(), parse_mode="HTML")


@router.callback_query(F.data == "refresh_profile")
async def refresh_profile(cb: CallbackQuery):
    await cb.message.delete()
    await show_profile(cb.message)
    await cb.answer("Обновлено!")


@router.message(F.text == "💰 Баланс и реквизиты")
async def show_balance(message: Message):
    u = await get_user(message.from_user.id)
    text = (
        "💰 <b>БАЛАНС И РЕКВИЗИТЫ</b>\n\n"
        "<b>Ваш баланс:</b>\n"
        f"• 💎 GRAM: {u['gram']}\n"
        f"• 🇷🇺 RUB: {u['rub']}\n"
        f"• 🇺🇸 USD: {u['usd']}\n"
        f"• 💲 USDT: {u['usdt']}\n"
        f"• ⭐ STARS: {u['stars']}\n\n"
        "<b>Ваши реквизиты:</b>\n"
        f"• 💎 Gram: {u['gram_wallet']}\n"
        f"• 💳 Карта: {u['card']}\n"
        f"• 📞 Телефон: {u['phone']}\n"
        f"• 💲 Usdt: {u['usdt_wallet']}\n\n"
        "Выберите действие:"
    )
    await message.answer(text, reply_markup=balance_kb(), parse_mode="HTML")


@router.callback_query(F.data == "balance_menu")
async def balance_menu_cb(cb: CallbackQuery):
    await cb.message.delete()
    await show_balance(cb.message)
    await cb.answer()


@router.callback_query(F.data == "set_gram")
async def set_gram_start(cb: CallbackQuery, state: FSMContext):
    await cb.message.edit_text(
        "💎 <b>GRAM КОШЕЛЁК</b>\n\nТекущий адрес:\nНе указан\n\n"
        "Отправьте новый адрес кошелька:\n• Формат: UQ... или EQA...\n"
        "• Адрес должен начинаться с UQ или EQ",
        reply_markup=back_kb(), parse_mode="HTML"
    )
    await state.set_state(ReqStates.waiting_for_gram)
    await cb.answer()


@router.message(ReqStates.waiting_for_gram)
async def save_gram(message: Message, state: FSMContext):
    await set_requisite(message.from_user.id, "gram_wallet", message.text)
    await message.answer("✅ Адрес Gram кошелька сохранён!", reply_markup=balance_kb())
    await state.clear()


@router.callback_query(F.data == "set_card")
async def set_card_start(cb: CallbackQuery, state: FSMContext):
    await cb.message.edit_text(
        "💳 <b>БАНКОВСКАЯ КАРТА</b>\n\nТекущие реквизиты:\nНе указана\n\n"
        "Отправьте новые реквизиты:\n• Формат: 2200 1234 5678 9010\n"
        "• Или: Банк — Номер карты",
        reply_markup=back_kb(), parse_mode="HTML"
    )
    await state.set_state(ReqStates.waiting_for_card)
    await cb.answer()


@router.message(ReqStates.waiting_for_card)
async def save_card(message: Message, state: FSMContext):
    await set_requisite(message.from_user.id, "card", message.text)
    await message.answer("✅ Карта сохранена!", reply_markup=balance_kb())
    await state.clear()


@router.callback_query(F.data == "set_phone")
async def set_phone_start(cb: CallbackQuery, state: FSMContext):
    await cb.message.edit_text(
        "📞 <b>НОМЕР ТЕЛЕФОНА</b>\n\nТекущий номер:\nНе указан\n\n"
        "Отправьте номер телефона:\n• Формат: +79991234567",
        reply_markup=back_kb(), parse_mode="HTML"
    )
    await state.set_state(ReqStates.waiting_for_phone)
    await cb.answer()


@router.message(ReqStates.waiting_for_phone)
async def save_phone(message: Message, state: FSMContext):
    await set_requisite(message.from_user.id, "phone", message.text)
    await message.answer("✅ Номер телефона сохранён!", reply_markup=balance_kb())
    await state.clear()


@router.callback_query(F.data == "set_usdt")
async def set_usdt_start(cb: CallbackQuery, state: FSMContext):
    await cb.message.edit_text(
        "💲 <b>USDT КОШЕЛЁК</b>\n\nТекущий адрес:\nНе указан\n\n"
        "Отправьте адрес Usdt (TON):\n• Формат: UQ... / EQ... (сеть TON)",
        reply_markup=back_kb(), parse_mode="HTML"
    )
    await state.set_state(ReqStates.waiting_for_usdt)
    await cb.answer()


@router.message(ReqStates.waiting_for_usdt)
async def save_usdt(message: Message, state: FSMContext):
    await set_requisite(message.from_user.id, "usdt_wallet", message.text)
    await message.answer("✅ Usdt кошелёк сохранён!", reply_markup=balance_kb())
    await state.clear()


@router.message(F.text == "⚡ Создать сделку")
async def create_deal(message: Message):
    await message.answer(
        "⚠️ <b>Для создания сделки необходимо привязать хотя бы одни реквизиты!</b>\n\n"
        "Перейдите в раздел «Баланс и реквизиты».",
        reply_markup=back_kb(), parse_mode="HTML"
    )


@router.message(F.text == "📦 Мои сделки")
async def my_deals(message: Message):
    await message.answer(
        "📦 <b>У ВАС ПОКА НЕТ АКТИВНЫХ СДЕЛОК</b>\n\n"
        "Создайте свою первую сделку с помощью кнопки ниже!",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⚡ Создать сделку", callback_data="stub")],
            [InlineKeyboardButton(text="🔙 В меню", callback_data="back_to_menu")]
        ]), parse_mode="HTML"
    )


@router.message(F.text == "ℹ️ Как это работает")
async def how_it_works(message: Message):
    text = (
        "ℹ️ <b>Как работает LOLZ guarantee</b>\n\n"
        "1. 🤝 Продавец создаёт сделку через главное меню по кнопке \"создать сделку\"\n"
        "2. 🔗 Продавец отправляет покупателю ссылку для подключения к сделке\n"
        "3. 💲 Покупатель подключается и оплачивает — деньги замораживаются у сервиса\n"
        "4. ⏳ Продавец ожидает сообщения об оплате от бота\n"
        "5. 📦 После получения сообщения, передаёт товар менеджеру @lolz_trans\n"
        "6. 🛡️ Менеджер проверяет получение подарка и подтверждает сделку\n"
        "7. Покупатель обращается к менеджеру @lolz_trans для получения подарка\n\n"
        "🛡️ Спор в любой момент — поможет менеджер @lolz_trans\n"
        "📊 Комиссия сервиса — 5%, платит покупатель сверху."
    )
    await message.answer(text, reply_markup=back_kb(), parse_mode="HTML")


@router.message(F.text == "📞 Поддержка")
async def support(message: Message):
    await message.answer(
        "📞 <b>Служба поддержки</b>\n\n"
        "По всем вопросам обращайтесь к менеджеру: @lolz_trans",
        reply_markup=back_kb(), parse_mode="HTML"
    )


@router.message(F.text == "🌐 Сменить язык")
async def change_lang(message: Message):
    b = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")
        ],
        [InlineKeyboardButton(text="🔙 В меню", callback_data="back_to_menu")]
    ])
    await message.answer("🌐 Выберите язык / Select language:", reply_markup=b)