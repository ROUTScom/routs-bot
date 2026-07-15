
import asyncio
import logging
import os
 
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
 
logging.basicConfig(level=logging.INFO)
 
BOT_TOKEN = os.getenv("BOT_TOKEN")
MANAGER_USERNAME = "routs_com"  # без @
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")  # личный chat_id для уведомлений
 
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
 
# ---------- ТЕКСТЫ ----------
 
WELCOME_TEXT = (
    "Привет! 👋\n\n"
    "Пока одни боятся сокращений, другие уже разобрались, как работать с "
    "ИИ, и обошли конкурентов на старте. Курс ROUTS для тех, кто не хочет "
    "остаться позади.\n\n"
    "Выбери, что тебя интересует:"
)
 
PROGRAM_TEXT = (
    "<b>ПРОГРАММА КУРСА</b>\n\n"
    "<b>Урок 1. Как меняется рынок труда</b>\n"
    "Твою профессию уже сокращают. Узнай, ты следующий?\n\n"
    "<b>Урок 2. Профессии будущего: куда смотреть</b>\n"
    "Пока одни пугаются заголовков про ИИ и увольнения, другие уже пересобрали "
    "резюме под растущие направления. Показываем, куда двигается рынок и какие "
    "роли только набирают вес.\n\n"
    "<b>Урок 3. Реальные инструменты — первое знакомство</b>\n"
    "Знакомимся с ИИ-инструментами, которыми уже пользуются те, кто на шаг впереди.\n\n"
    "<b>Урок 4. Практика: от первого запроса до личного ассистента</b>\n"
    "От простого «привет, ChatGPT» до рабочего ИИ-ассистента, который закрывает "
    "конкретные задачи, а не просто поддерживает разговор.\n\n"
    "<b>Урок 5. Автоматизируем бизнес-процессы на реальном примере</b>\n"
    "На живом кейсе показываем, как ИИ забирает рутину на себя и освобождает "
    "часы в неделю. Это уже не теория, а рабочая связка, которую можно повторить у себя.\n\n"
    "<b>Урок 6. Бонусный урок — Как мыслить в эпоху неопределённости</b>\n"
    "Что делать с тревогой, когда правила игры меняются быстрее, чем ты успеваешь "
    "читать новости."
)
 
BUY_TEXT = (
    "Стоимость курса — <b>$49</b>.\n"
    "Оплатить можно в любой удобной валюте — выбери ниже:"
)
 
REQUISITES = {
    "usd": "Реквизиты 1",
    "eur": "Реквизиты 2",
    "rub": "Реквизиты 3",
}
 
CURRENCY_LABELS = {
    "usd": "🇺🇸 USD",
    "eur": "🇪🇺 EUR",
    "rub": "🇷🇺 RUB",
}
 
OTHER_CURRENCY_TEXT = (
    f"Напишите менеджеру — подберём удобный способ оплаты для вашей валюты: "
    f"@{MANAGER_USERNAME}"
)
 
CONTACT_TEXT = f"Свяжитесь с нами напрямую: @{MANAGER_USERNAME}"
 
FALLBACK_TEXT = (
    "Я просто бот 🤖 Но если хочется поговорить с человеком — напишите "
    f"нашим менеджерам: @{MANAGER_USERNAME}\n\n"
    "А здесь можно выбрать, что интересует:"
)
 
# ---------- КЛАВИАТУРЫ ----------
 
def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Купить курс", callback_data="buy")],
        [InlineKeyboardButton(text="📋 Программа", callback_data="program")],
        [InlineKeyboardButton(text="✉️ Связаться с нами", callback_data="contact")],
    ])
 
def currency_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=CURRENCY_LABELS["usd"], callback_data="cur_usd")],
        [InlineKeyboardButton(text=CURRENCY_LABELS["eur"], callback_data="cur_eur")],
        [InlineKeyboardButton(text=CURRENCY_LABELS["rub"], callback_data="cur_rub")],
        [InlineKeyboardButton(text="🌍 Другая валюта", callback_data="cur_other")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_main")],
    ])
 
def back_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_main")],
    ])
 
# ---------- ХЕНДЛЕРЫ ----------
 
@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_kb())
 
@dp.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):
    await callback.message.edit_text(WELCOME_TEXT, reply_markup=main_menu_kb())
    await callback.answer()
 
@dp.callback_query(F.data == "program")
async def program_handler(callback: CallbackQuery):
    await callback.message.edit_text(PROGRAM_TEXT, reply_markup=back_kb(), parse_mode="HTML")
    await callback.answer()
 
@dp.callback_query(F.data == "contact")
async def contact_handler(callback: CallbackQuery):
    await callback.message.edit_text(CONTACT_TEXT, reply_markup=back_kb())
    await callback.answer()
 
@dp.callback_query(F.data == "buy")
async def buy_handler(callback: CallbackQuery):
    await callback.message.edit_text(BUY_TEXT, reply_markup=currency_kb(), parse_mode="HTML")
    await callback.answer()
 
@dp.callback_query(F.data == "cur_other")
async def other_currency_handler(callback: CallbackQuery):
    await callback.message.edit_text(OTHER_CURRENCY_TEXT, reply_markup=back_kb())
    await callback.answer()
 
@dp.callback_query(F.data.startswith("cur_"))
async def currency_handler(callback: CallbackQuery):
    code = callback.data.split("_", 1)[1]  # usd / eur / rub
    if code not in REQUISITES:
        await callback.answer()
        return
    text = (
        f"Оплата в {CURRENCY_LABELS[code]}:\n\n"
        f"{REQUISITES[code]}\n\n"
        f"После оплаты пришлите скриншот сюда или менеджеру @{MANAGER_USERNAME}, "
        f"и мы откроем доступ к курсу."
    )
    await callback.message.edit_text(text, reply_markup=back_kb())
    await callback.answer()
 
@dp.message()
async def fallback_handler(message: Message):
    # Отвечаем человеку
    await message.answer(FALLBACK_TEXT, reply_markup=main_menu_kb())
 
    # Пересылаем менеджеру, если задан ADMIN_CHAT_ID
    if ADMIN_CHAT_ID:
        user = message.from_user
        username_part = f"@{user.username}" if user.username else "без username"
        notify_text = (
            f"📩 Новое сообщение в боте\n"
            f"От: {user.full_name} ({username_part})\n"
            f"ID: {user.id}\n\n"
            f"Текст: {message.text}"
        )
        try:
            await bot.send_message(chat_id=ADMIN_CHAT_ID, text=notify_text)
        except Exception as e:
            logging.warning(f"Не удалось отправить уведомление менеджеру: {e}")
 
# ---------- ЗАПУСК ----------
 
async def main():
    await dp.start_polling(bot)
 
if __name__ == "__main__":
    asyncio.run(main())
 
