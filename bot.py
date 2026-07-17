import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
MANAGER_USERNAME = "routs_com"  # без @
INSTAGRAM = "your.routs"
TG_CHANNEL = "routscom"
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")  # личный chat_id для уведомлений

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ---------- ТЕКСТЫ ----------

WELCOME_TEXT = (
    "Привет! 👋\n\n"
    "Пока одни боятся сокращений, другие уже разобрались, как работать с "
    "ИИ, и обошли конкурентов на старте. Курс ROUTS для тех, кто хочет, "
    "чтобы их карьера оставалась актуальной.\n\n"
    "Выбери, что тебя интересует:"
)

PROGRAM_TEXT = (
    "<b>ПРОГРАММА КУРСА</b>\n\n"
    "Этот курс — азы и фундамент. Самое важное, что нужно знать про рынок "
    "труда и актуальные инструменты: куда двигаются профессии, какие есть "
    "инструменты ИИ и как ими пользоваться.\n\n"
    "<b>Урок 1. Как меняется рынок труда в 2026 году</b>\n"
    "Общие тенденции: что происходит и почему это касается каждого.\n\n"
    "<b>Урок 2. Профессии: было / стало / исчезнет</b>\n"
    "Разбираем на конкретных примерах, какие роли уже изменились, какие "
    "появились и какие скоро уйдут.\n\n"
    "<b>Урок 3. Кто нужен сейчас</b>\n"
    "Какие специалисты востребованы и как адаптировать твою профессию.\n\n"
    "<b>Уроки 4–5. Практика: инструменты в деле</b>\n"
    "Два практических урока о том, как работает современный ИИ-инструментарий — "
    "от первых запросов до применения в реальных задачах.\n\n"
    "<b>Урок 6. Как мыслить в эпоху неопределённости</b>\n"
    "Что делать с тревогой, когда правила игры меняются быстрее, чем ты "
    "успеваешь читать новости.\n\n"
    "———\n\n"
    f"Жми подписку в удобной для тебя соцсети — Instagram "
    f"(instagram.com/{INSTAGRAM}) или наш Telegram-канал @{TG_CHANNEL} — "
    "чтобы не пропустить продолжение.\n\n"
    "Вторая ступень обучения — <b>«Стать лидером в своей сфере»</b> — будет "
    "доступна только тем, кто прошёл первую. Одно без другого не работает: "
    "сначала научимся мыслить в новых реалиях и расти, а во втором блоке — "
    "будем масштабироваться."
)

RESULTS_TEXT = (
    "<b>После курса у вас на руках:</b>\n\n"
    "— Честная оценка, что будет с вашей профессией, и план, куда двигаться\n\n"
    "— Понимание, какие роли растут и как под них пересобрать свой опыт\n\n"
    "— Рабочие ИИ-инструменты, которые вы уже попробовали на своих задачах, "
    "а не посмотрели со стороны\n\n"
    "— Настроенный личный ИИ-ассистент под ваши задачи\n\n"
    "— Спокойная голова: понятно, что происходит и что делать дальше\n\n"
    "Всё на простом языке, без технического образования и подготовки."
)

BUY_TEXT = (
    "Стоимость курса — <b>$49</b>.\n"
    "Оплатить можно в любой удобной валюте — выбери ниже:"
)

REQUISITES = {
    "usd": "Реквизиты 1",
    "eur": "Реквизиты 2",
    "rub": "Реквизиты 3",
    "uah": "Реквизиты 4",
}

CURRENCY_LABELS = {
    "usd": "🇺🇸 USD",
    "eur": "🇪🇺 EUR",
    "rub": "🇷🇺 RUB",
    "uah": "🇺🇦 UAH",
}

OTHER_CURRENCY_TEXT = (
    f"Напишите менеджеру — подберём удобный способ оплаты для вашей валюты: "
    f"@{MANAGER_USERNAME}"
)

CONTACT_TEXT = (
    "Мы на связи:\n\n"
    f"📸 Instagram: instagram.com/{INSTAGRAM}\n"
    f"📢 Telegram-канал: @{TG_CHANNEL}\n"
    f"✉️ Менеджер: @{MANAGER_USERNAME}"
)

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
        [InlineKeyboardButton(text="🎯 Что я получу?", callback_data="results")],
        [InlineKeyboardButton(text="✉️ Связаться с нами", callback_data="contact")],
    ])

def currency_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=CURRENCY_LABELS["usd"], callback_data="cur_usd")],
        [InlineKeyboardButton(text=CURRENCY_LABELS["eur"], callback_data="cur_eur")],
        [InlineKeyboardButton(text=CURRENCY_LABELS["rub"], callback_data="cur_rub")],
        [InlineKeyboardButton(text=CURRENCY_LABELS["uah"], callback_data="cur_uah")],
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

@dp.callback_query(F.data == "results")
async def results_handler(callback: CallbackQuery):
    await callback.message.edit_text(RESULTS_TEXT, reply_markup=back_kb(), parse_mode="HTML")
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
    code = callback.data.split("_", 1)[1]  # usd / eur / rub / uah
    if code not in REQUISITES:
        await callback.answer()
        return
    text = (
        f"Оплата в {CURRENCY_LABELS[code]}:\n\n"
        f"{REQUISITES[code]}\n\n"
        f"После оплаты пришлите скриншот менеджеру @{MANAGER_USERNAME}, "
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
