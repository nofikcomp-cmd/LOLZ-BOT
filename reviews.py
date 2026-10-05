import asyncio
import random
from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from database import get_reviews, get_reviews_count, add_review
from keyboards import reviews_kb

router = Router()

FAKE_NAMES = [
    "Пользователь", "User123", "Alex", "Maxim", "Nikita", "Dmitry",
    "Иван", "Сергей", "Артём", "Владислав", "Кирилл", "Роман",
    "Трейдер", "Скупщик", "Клиент", "Покупатель"
]

FAKE_TEXTS = [
    "ахах думал будет дольше, а тут за минуту управились",
    "Сделка быстрая была и деньги пришли",
    "Всё прошло отлично спасибо за работу.",
    "Быстро, чётко, без проблем. Рекомендую!",
    "Первый раз тут, всё понравилось 👍",
    "Менеджер топ, всё сделал за 2 минуты",
    "Деньги пришли моментально, спасибо!",
    "Норм сервис, буду ещё пользоваться",
    "Всё честно, без кидков. Доволен!",
    "Спасибо большое, выручили 🙏",
    "Работает быстро, комиссия норм",
    "Лучший гарант, проверено временем",
    "Оперативно решили вопрос, респект",
    "Всё супер, сделка прошла гладко",
    "Быстро и надёжно, как всегда 🔥",
]

MONTHS = {
    1: "янв", 2: "фев", 3: "мар", 4: "апр", 5: "мая", 6: "июн",
    7: "июл", 8: "авг", 9: "сен", 10: "окт", 11: "ноя", 12: "дек"
}


def format_date(dt: datetime) -> str:
    return f"{dt.day} {MONTHS[dt.month]}. {dt.year} г."


def format_reviews_text(reviews: list, total_count: int) -> str:
    avg = 4.8
    text = (
        "⭐ <b>Отзывы</b>\n"
        "Что говорят пользователи о сделках\n\n"
        f"📊 <b>{total_count}</b> отзывов | <b>{avg}</b> средняя оценка | <b>24/7</b> сделки\n\n"
    )
    for r in reviews:
        stars = "⭐" * r["stars"]
        text += (
            f"👤 <b>{r['username']}</b>  {stars}\n"
            f"<i>{r['date']}</i>\n"
            f"{r['text']}\n\n"
        )
    return text.strip()


@router.message(F.text == "⭐ Отзывы")
async def show_reviews(message: Message):
    reviews = await get_reviews(limit=10)
    total = await get_reviews_count()
    text = format_reviews_text(reviews, total)
    await message.answer(text, reply_markup=reviews_kb(), parse_mode="HTML")


@router.callback_query(F.data == "refresh_reviews")
async def refresh_reviews(cb: CallbackQuery):
    reviews = await get_reviews(limit=10)
    total = await get_reviews_count()
    text = format_reviews_text(reviews, total)
    await cb.message.edit_text(text, reply_markup=reviews_kb(), parse_mode="HTML")
    await cb.answer("Обновлено!")


@router.callback_query(F.data == "leave_review")
async def leave_review(cb: CallbackQuery):
    await cb.answer("Форма отзыва появится здесь", show_alert=True)


async def seed_reviews_if_empty():
    """Закидываем 3 стартовых отзыва, как на скрине."""
    if await get_reviews_count() == 0:
        today = format_date(datetime.now())
        await add_review("Пользователь", 5, "ахах думал будет дольше, а тут за минуту управились", today)
        await add_review("Пользователь", 5, "Сделка быстрая была и деньги пришли", today)
        await add_review("Пользователь", 5, "Всё прошло отлично спасибо за работу.", today)


async def auto_add_review_loop():
    """Каждые 5-15 минут добавляет новый фейковый отзыв."""
    while True:
        await asyncio.sleep(random.randint(300, 900))
        name = random.choice(FAKE_NAMES)
        text = random.choice(FAKE_TEXTS)
        stars = random.choice([4, 5, 5, 5, 5])
        date = format_date(datetime.now())
        await add_review(name, stars, text, date)