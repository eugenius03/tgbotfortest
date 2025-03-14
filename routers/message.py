from aiogram import Router, F
from aiogram.types import Message
from pay.payments import payment
from db.orm import AsyncORM
import asyncio
from .Cart import cart
from .commands import send_products

message_router = Router()


@message_router.message(F.text == "💵 До сплати")
async def payday_handler(message: Message):
    user_id = message.from_user.id
    if cart.get(user_id):
        total = cart[user_id].get_total()
        order_id = await AsyncORM.create_order(user_id, cart[user_id].save_items(), total, "created")
        url = await payment.generate_url(order_id, amount = total, description=cart[user_id].get_items())
        msg = await message.reply(url)
        await payday(order_id, msg, user_id)
    else:
        await message.reply("Кошик порожній!")


async def payday(order_id, msg, user_id):
    response = payment.get_order_status(order_id)
    time=0
    while(response == False and time < 180):
        await asyncio.sleep(5)
        response = payment.get_order_status(order_id)
        time+=5

    if response.get("status") == "success":
        await msg.reply(text = f"Оплата пройшла успішно!")
        await AsyncORM.edit_status(order_id, "Done")
        del cart[user_id]
    elif response.get("status") == "try_again":
        await msg.reply(text =f"Помилка при оплаті. Спробуйте ще раз")
        time=0
        while(response.get("status") == "try_again" and time < 180):
            await asyncio.sleep(5)
            response = payment.get_order_status(order_id)
            time+=5
        if response.get("status") == "success":
            await msg.reply(text = f"Оплата пройшла успішно!")
            await AsyncORM.edit_status(order_id, "Done")
            del cart[user_id]

@message_router.message(F.text == "🛒 Очистити кошик")
async def cart_handler(message: Message):
    user_id = message.from_user.id
    if cart.get(user_id):
        del cart[user_id]
        await message.reply("Кошик очищено!")
    else:
        await message.reply("Кошик порожній!")

@message_router.message(F.text == "📦 Товари")
async def products_handler(message: Message):
    await send_products(message)