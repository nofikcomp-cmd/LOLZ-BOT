from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from config import OWNER_ID
from database import find_by_username, update_role

router = Router()


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != OWNER_ID:
        await message.answer("❌ У вас нет доступа.")
        return
    text = (
        "👑 <b>ПАНЕЛЬ ВЛАДЕЛЬЦА</b>\n\n"
        "Для назначения роли используйте команду:\n"
        "<code>/setrole @username роль</code>\n\n"
        "Доступные роли: <b>admin, worker, user</b>\n"
        "Пример: <code>/setrole @dgsgsgg воркер</code>"
    )
    await message.answer(text, parse_mode="HTML")


@router.message(Command("setrole"))
async def set_role(message: Message):
    if message.from_user.id != OWNER_ID:
        await message.answer("❌ У вас нет доступа.")
        return

    args = message.text.split()
    if len(args) != 3:
        await message.answer("❌ Формат: /setrole @username роль\nРоли: воркер, админ, user")
        return

    target_username = args[1].replace("@", "")
    role_input = args[2].lower()

    role_map = {
        "воркер": "worker", "админ": "admin", "пользователь": "user",
        "worker": "worker", "admin": "admin", "user": "user"
    }
    if role_input not in role_map:
        await message.answer("❌ Неверная роль. Доступно: воркер, админ, user")
        return

    user = await find_by_username(target_username)
    if not user:
        await message.answer(f"❌ Пользователь @{target_username} не найден. Пусть он нажмёт /start.")
        return

    await update_role(user["user_id"], role_map[role_input])
    await message.answer(f"✅ @{target_username} теперь <b>{role_map[role_input]}</b>", parse_mode="HTML")