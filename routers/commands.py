import asyncio

from aiogram import Bot, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

command_router = Router()


@command_router.message(CommandStart())
async def command_start_handler(message: Message, bot: Bot):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(0.3)
    await message.answer(
        "Привіт! Для того, щоб купити товар введи /products "
    )

@command_router.message(Command("products"))
async def command_products_handler(message: Message):
    await message.answer(
        "Доступні товари (натисніть, щоб додати у кошик):", reply_markup=get_inline()
    )

async def send_products(message: Message):
    await message.answer(
        "Доступні товари (натисніть, щоб додати у кошик):", reply_markup=get_inline()
    )

def get_inline():
    keyboard = [
        [InlineKeyboardButton(text="Buckwheat - 100 UAH", callback_data="Buckwheat_info")],
        [InlineKeyboardButton(text="Milk - 60 UAH", callback_data="Milk_info")],
        [InlineKeyboardButton(text="Bread - 20 UAH", callback_data="Bread_info")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

    return keyboard
