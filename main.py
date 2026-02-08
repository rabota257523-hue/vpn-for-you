vpn_bot/
├── main.py
├── requirements.txt
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🔐 Токен берётся из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# ====== КНОПКИ ГЛАВНОГО МЕНЮ ======
main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton("🛒 Купить VPN", callback_data="buy_vpn")],
    [InlineKeyboardButton("🔑 Мой VPN", callback_data="my_vpn")]
])

# ====== /start ======
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать в VPN-бот!\n\n"
        "Выберите действие:",
        reply_markup=main_menu
    )

# ====== КУПИТЬ VPN ======
@dp.callback_query_handler(lambda c: c.data == "buy_vpn")
async def buy_vpn(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("🗓 1 месяц — 70₽", callback_data="buy_1")],
        [InlineKeyboardButton("🗓 2 месяца — 150₽", callback_data="buy_2")],
        [InlineKeyboardButton("🗓 3 месяца — 220₽", callback_data="buy_3")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back")]
    ])

    await callback.message.edit_text(
        "💳 Выберите тариф VPN:",
        reply_markup=keyboard
    )

# ====== ОБРАБОТКА ТАРИФОВ (ПОКА ЗАГЛУШКА) ======
@dp.callback_query_handler(lambda c: c.data.startswith("buy_"))
async def buy_tariff(callback: types.CallbackQuery):
    await callback.answer(
        "💳 Оплата скоро будет подключена.\n"
        "После оплаты VPN-ключ придёт автоматически 👌",
        show_alert=True
    )

# ====== МОЙ VPN ======
@dp.callback_query_handler(lambda c: c.data == "my_vpn")
async def my_vpn(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🔑 Ваш VPN:\n\n"
        "❌ Активного VPN нет\n\n"
        "Нажмите «Купить VPN», чтобы получить доступ.",
        reply_markup=main_menu
    )

# ====== НАЗАД ======
@dp.callback_query_handler(lambda c: c.data == "back")
async def back(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Главное меню:",
        reply_markup=main_menu
    )

# ====== ЗАПУСК ======
if __name__ == "__main__":
    executor.start_polling(dp)
