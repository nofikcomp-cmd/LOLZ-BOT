from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from config import SITE_URL, CHANNEL_USERNAME, MANAGER_USERNAME


def main_menu_kb(role: str):
    b = ReplyKeyboardBuilder()
    b.row(KeyboardButton(text="👤 Мой профиль"), KeyboardButton(text="⚡ Создать сделку"))
    b.row(KeyboardButton(text="🌐 Верификация"), KeyboardButton(text="💰 Баланс и реквизиты"))
    b.row(KeyboardButton(text="⭐ Отзывы"), KeyboardButton(text="🌐 Сменить язык"))
    b.row(KeyboardButton(text="📞 Поддержка"))
    b.row(KeyboardButton(text="ℹ️ Как это работает"))
    b.row(
        KeyboardButton(text="🌐 Сайт", url=SITE_URL),
        KeyboardButton(text="📢 Канал", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")
    )
    if role in ["owner", "admin", "worker"]:
        b.row(KeyboardButton(text="🛠 Воркер панель"))
    return b.as_markup(resize_keyboard=True)


def worker_panel_kb():
    b = ReplyKeyboardBuilder()
    b.row(KeyboardButton(text="📊 Моя статистика"), KeyboardButton(text="📦 Мои сделки"))
    b.row(KeyboardButton(text="📉 Накрутка сделок"), KeyboardButton(text="💰 Накрутка баланса"))
    b.row(KeyboardButton(text="📈 Открутка сделок"), KeyboardButton(text="✂️ Урезать профиль"))
    b.row(KeyboardButton(text="🏷 Мой тег"), KeyboardButton(text="👥 Мои мамонты"))
    b.row(KeyboardButton(text="🔙 В меню"))
    return b.as_markup(resize_keyboard=True)


def back_kb():
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="🔙 В меню", callback_data="back_to_menu"))
    return b.as_markup()


def cancel_kb():
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_action"))
    return b.as_markup()


def profile_kb():
    b = InlineKeyboardBuilder()
    b.row(
        InlineKeyboardButton(text="🔄 Обновить", callback_data="refresh_profile"),
        InlineKeyboardButton(text="📦 Мои сделки", callback_data="my_deals")
    )
    b.row(InlineKeyboardButton(text="💰 Баланс и реквизиты", callback_data="balance_menu"))
    b.row(InlineKeyboardButton(text="🌐 Верификация", callback_data="verification_menu"))
    b.row(InlineKeyboardButton(text="🔙 В меню", callback_data="back_to_menu"))
    return b.as_markup()


def balance_kb():
    b = InlineKeyboardBuilder()
    b.row(
        InlineKeyboardButton(text="💳 Пополнить баланс", callback_data="deposit"),
        InlineKeyboardButton(text="💸 Вывести", callback_data="withdraw")
    )
    b.row(
        InlineKeyboardButton(text="💎 Gram кошелёк", callback_data="set_gram"),
        InlineKeyboardButton(text="💳 Карта", callback_data="set_card")
    )
    b.row(
        InlineKeyboardButton(text="📞 Телефон", callback_data="set_phone"),
        InlineKeyboardButton(text="💲 Usdt кошелёк", callback_data="set_usdt")
    )
    b.row(InlineKeyboardButton(text="🔙 В меню", callback_data="back_to_menu"))
    return b.as_markup()


def verification_kb():
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="💳 Оплатить картой", callback_data="pay_card"))
    b.row(InlineKeyboardButton(text="💲 Оплатить USDT (TON)", callback_data="pay_usdt"))
    b.row(InlineKeyboardButton(text="💎 Оплатить GRAM (TON)", callback_data="pay_gram"))
    b.row(
        InlineKeyboardButton(text="🇰🇿 Оплатить KZT", callback_data="pay_kzt"),
        InlineKeyboardButton(text="🇧🇾 Оплатить BYN", callback_data="pay_byn")
    )
    b.row(InlineKeyboardButton(text="⭐ Оплатить Stars", callback_data="pay_stars"))
    b.row(
        InlineKeyboardButton(text="📞 Поддержка", url=f"https://t.me/{MANAGER_USERNAME.replace('@', '')}"),
        InlineKeyboardButton(text="🔙 В меню", callback_data="back_to_menu")
    )
    return b.as_markup()


def tag_kb():
    b = InlineKeyboardBuilder()
    b.row(
        InlineKeyboardButton(text="Установить тег", callback_data="set_tag_start"),
        InlineKeyboardButton(text="🗑 Удалить тег", callback_data="delete_tag")
    )
    b.row(InlineKeyboardButton(text="🔙 В меню", callback_data="back_to_menu"))
    return b.as_markup()


def reviews_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔄 Обновить", callback_data="refresh_reviews"),
            InlineKeyboardButton(text="✍️ Оставить отзыв", callback_data="leave_review")
        ],
        [InlineKeyboardButton(text="🔙 В меню", callback_data="back_to_menu")]
    ])