import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import CallbackQuery

from config import BOT_TOKEN
from database import init_db
from handlers import start, profile, verification, worker_panel, admin_panel, reviews
from handlers.reviews import auto_add_review_loop, seed_reviews_if_empty

logging.basicConfig(level=logging.INFO)


async def main():
    # 1) Инициализация базы
    await init_db()
    await seed_reviews_if_empty()

    # 2) Бот и диспетчер
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # 3) Роутеры
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(verification.router)
    dp.include_router(worker_panel.router)
    dp.include_router(admin_panel.router)
    dp.include_router(reviews.router)

    # 4) Общие callback-хэндлеры
    @dp.callback_query(lambda c: c.data == "back_to_menu")
    async def back_to_menu_cb(cb: CallbackQuery):
        await cb.message.delete()
        from handlers.start import cmd_start
        # Пересоздаём сообщение — просто вызываем старт
        # (без /start, а тот же ответ)
        from database import get_user
        from keyboards import main_menu_kb
        user = await get_user(cb.from_user.id)
        await cb.message.answer(
            "Главное меню:", reply_markup=main_menu_kb(user["role"])
        )
        await cb.answer()

    @dp.callback_query(lambda c: c.data == "cancel_action")
    async def cancel_action_cb(cb: CallbackQuery):
        from keyboards import worker_panel_kb
        await cb.message.delete()
        await cb.message.answer("Действие отменено.", reply_markup=worker_panel_kb())
        await cb.answer()

    @dp.callback_query(lambda c: c.data == "stub")
    async def stub_cb(cb: CallbackQuery):
        await cb.answer("Функция в разработке", show_alert=True)

    # 5) Фоновая задача авто-отзывов
    asyncio.create_task(auto_add_review_loop())

    print("🚀 Бот запущен! Все системы работают.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
