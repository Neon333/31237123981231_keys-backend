import asyncio

from dotenv import load_dotenv
import os


async def startup_event():
    print('Setup checking...')
    from core.game.models.genre import GenreRepo
    from core.user import User
    load_dotenv()
    print(await User.get_by_id(1))
    if await User.get_by_id(1) is None:
        print('Database initialized')
        await User.create(os.getenv('ADMIN_EMAIL'), os.getenv('ADMIN_PASSWORD'))

        genres = [
            "Экшен", "Приключения", "Ролевые", "Шутер", "Стратегия",
            "Симулятор", "Спорт", "Гонки", "Хоррор", "RPG", "Action RPG"
        ]
        for genre in genres:
            await GenreRepo.create(genre)


if __name__ == '__main__':
    asyncio.run(startup_event())