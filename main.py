import sys
import asyncio
import logging
import sqlite3
import dboper

import handlers
import bot

logging.basicConfig(level=logging.INFO)


# Connect to the SQLite database and create tables if they don't exist
conn = sqlite3.connect('users.db')
c = conn.cursor()
dboper.create_users(conn, c)
dboper.create_reactions(conn, c)


async def main():
    await bot.dp.start_polling(bot.moura)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
