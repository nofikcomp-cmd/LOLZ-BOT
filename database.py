import aiosqlite
from config import DB_PATH


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                role TEXT DEFAULT 'user',
                deals INTEGER DEFAULT 0,
                referrals INTEGER DEFAULT 0,
                tag TEXT DEFAULT 'Не установлен',
                rub REAL DEFAULT 0.0,
                usd REAL DEFAULT 0.0,
                gram REAL DEFAULT 0.0,
                usdt REAL DEFAULT 0.0,
                stars INTEGER DEFAULT 0,
                card TEXT DEFAULT 'Не указана',
                phone TEXT DEFAULT 'Не указан',
                gram_wallet TEXT DEFAULT 'Не указан',
                usdt_wallet TEXT DEFAULT 'Не указан'
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                stars INTEGER,
                text TEXT,
                date TEXT
            )
        """)
        await db.commit()