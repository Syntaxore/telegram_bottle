import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

API_TOKEN = 'token'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Хранение игроков и состояния игры
players = []
game_state = "waiting_for_players"

@dp.message(Command("start"))
async def start_game(message: types.Message):
    await message.answer("Привет! Напиши /join, чтобы присоединиться к игре.")

@dp.message(Command("join"))
async def join_game(message: types.Message):
    global players
    if message.from_user.id not in players:
        players.append(message.from_user.id)
        await message.answer("Ты присоединился к игре! Участники: " + ', '.join([str(user) for user in players]))
    else:
        await message.answer("Ты уже в игре!")

@dp.message(Command("start_game"))
async def start_game_command(message: types.Message):
    global game_state
    if game_state == "waiting_for_players" and len(players) >= 2:
        game_state = "game_in_progress"
        await message.answer("Игра началась! Нажмите /kiss, чтобы поцеловаться через бутылку.")
    else:
        await message.answer("Нужно как минимум 2 игрока для начала игры.")

@dp.message(Command("kiss"))
async def kiss_command(message: types.Message):
    global game_state
    if game_state == "game_in_progress":
        kissed_player = random.choice(players)
        await message.answer(f"Поцелуй достался игроку: {kissed_player}!")
    else:
        await message.answer("Игра еще не началась. Используйте /start_game для начала.")

@dp.message(Command("end_game"))
async def end_game(message: types.Message):
    global game_state, players
    game_state = "waiting_for_players"
    players = []
    await message.answer("Игра окончена. Вы можете начать новую игру с /start.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
