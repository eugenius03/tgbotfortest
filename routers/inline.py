from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pay.payments import payment
from db.orm import AsyncORM
import asyncio

inline_router = Router()

@inline_router.callback_query(F.data.in_({"Buckwheat", "Milk", "Bread"}))
async def inline_handler(call: CallbackQuery):
    price = {
        "Buckwheat": 100,
        "Milk": 60,
        "Bread": 20
    }
    product = call.data
    total = price[call.data]
    order_id = await AsyncORM.create_order(user_id=call.from_user.id, product=product, total=total, status="created")
    url = await payment.generate_url(order_id=order_id, amount = total, description=product)
    msg = await call.message.answer(url)
    await payday(order_id, product, total, call, msg, url)
    


async def payday(order_id, product, total, call, msg, url):
    response = payment.get_order_status(order_id)
    time=0
    while(response == False or time < 180):
        await asyncio.sleep(5)
        response = payment.get_order_status(order_id)
        time+=5

    if response.get("status") == "success":
        await call.message.answer(f"Оплата пройшла успішно! Ваше замовлення: {product} на суму {total} грн")
        await AsyncORM.edit_status(order_id, "Done")
    elif response.get("status") == "try_again":
        await call.message.answer(f"Помилка при оплаті. Спробуйте ще раз")
        time=0
        while(response.get("status") == "try_again" or time < 180):
            await asyncio.sleep(5)
            response = payment.get_order_status(order_id)
            time+=5
        if response.get("status") == "success":
            await call.message.answer(f"Оплата пройшла успішно! Ваше замовлення: {product} на суму {total} грн")
            await AsyncORM.edit_status(order_id, "Done")
