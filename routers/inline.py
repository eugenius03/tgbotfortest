from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from pay.payments import payment
from db.orm import AsyncORM
import asyncio
from .Cart import cart, Cart
from .commands import get_inline

inline_router = Router()

@inline_router.callback_query(F.data.in_({"Buckwheat", "Milk", "Bread"}))
async def inline_handler(call: CallbackQuery):
    await call.answer()
    price = {
        "Buckwheat": 100,
        "Milk": 60,
        "Bread": 20
    }
    product = call.data
    total = price[call.data]
    if cart.get(call.from_user.id):
        cart[call.from_user.id].add_item(product, total)
    else:
        cart[call.from_user.id] = Cart(product, total)
    await call.message.answer(
        f"Товар {product} додано у кошик.\n"
        f"\nВаш кошик:\n{cart[call.from_user.id].get_items()}"
        f"\nНа суму: {cart[call.from_user.id].get_total()} грн",
        reply_markup = get_keyboard()
        )
    
def get_keyboard():
    keyboard = [
        [KeyboardButton(text="💵 До сплати")],
        [KeyboardButton(text="🛒 Очистити кошик"), KeyboardButton(text="📦 Товари")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    return keyboard

@inline_router.callback_query(F.data == "back")
async def buck_info(call: CallbackQuery):
    await call.answer()
    await call.message.delete()
    await call.message.answer(
        "Доступні товари (натисніть, щоб додати у кошик):", reply_markup=get_inline()
    )


@inline_router.callback_query(F.data.contains("_info"))
async def buck_info(call: CallbackQuery):
    await call.answer()
    await call.message.delete()
    desc = {
        "Buckwheat_info": {"text": "Buckwheat - 100 UAH", "data" : "Buckwheat", "link": "https://photobooth.cdn.sports.ru/preset/news/e/87/1bb5c8ae94acab67ce33a43775356.jpeg"},
        "Bread_info": {"text": "Bread - 20 UAH", "data" : "Bread", "link": "https://shelfcooking.com/wp-content/uploads/2020/07/Rustic-Bread.jpg"},
        "Milk_info": {"text": "Milk - 60 UAH", "data" : "Milk", "link": "https://ih1.redbubble.net/image.3626199979.2902/flat,750x,075,f-pad,750x1000,f8f8f8.jpg"},

    }
    desc = desc[call.data]
    keyboard = [
        [InlineKeyboardButton(text=desc["text"], callback_data=desc["data"])],
        [InlineKeyboardButton(text="Back", callback_data="back")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await call.message.answer_photo(
        photo=desc["link"],
        caption="Description", reply_markup=keyboard)
    