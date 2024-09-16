import os
from dotenv import load_dotenv
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, ReplyKeyboardMarkup, ReplyKeyboardRemove
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, ConversationHandler, filters
)
from sqlalchemy.orm import Session
from database import engine, User
from enum import Enum


# Загружаем переменные окружения
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
WEBAPP_URL = os.getenv('WEBAPP_URL')

# Проверяем наличие токена
if not TOKEN:
    raise ValueError("Токен бота не задан. Установите переменную окружения TELEGRAM_TOKEN.")

# Определяем состояния для процесса регистрации
class RegistrationStates(Enum):
    GET_NAME = 1
    GET_GENDER = 2
    GET_AGE = 3
    GET_WEIGHT = 4
    GET_HEIGHT = 5
    GET_ACTIVITY = 6
    GET_GOAL = 7

# Функции для регистрации
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user:
            await update.message.reply_text('Вы уже зарегистрированы!')
            return ConversationHandler.END

    await update.message.reply_text('Начнем регистрацию. Как вас зовут?')
    return RegistrationStates.GET_NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.text
    user_id = update.message.from_user.id
    with Session(engine) as session:
        user = User(user_id=user_id, username=username)
        session.add(user)
        session.commit()

    reply_keyboard = [['Мужской', 'Женский']]
    await update.message.reply_text(
        'Укажите ваш пол:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return RegistrationStates.GET_GENDER

async def get_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gender = update.message.text
    user_id = update.message.from_user.id
    with Session(engine) as session:
        user = session.get(User, user_id)
        user.gender = gender
        session.commit()

    await update.message.reply_text('Укажите ваш возраст:', reply_markup=ReplyKeyboardRemove())
    return RegistrationStates.GET_AGE

async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        age = int(update.message.text)
        user_id = update.message.from_user.id
        with Session(engine) as session:
            user = session.get(User, user_id)
            user.age = age
            session.commit()

        await update.message.reply_text('Укажите ваш вес в кг:')
        return RegistrationStates.GET_WEIGHT
    except ValueError:
        await update.message.reply_text('Пожалуйста, введите числовое значение возраста.')
        return RegistrationStates.GET_AGE

async def get_weight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        weight = float(update.message.text.replace(',', '.'))
        user_id = update.message.from_user.id
        with Session(engine) as session:
            user = session.get(User, user_id)
            user.weight = weight
            session.commit()

        await update.message.reply_text('Укажите ваш рост в см:')
        return RegistrationStates.GET_HEIGHT
    except ValueError:
        await update.message.reply_text('Пожалуйста, введите числовое значение веса.')
        return RegistrationStates.GET_WEIGHT

async def get_height(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        height = float(update.message.text.replace(',', '.'))
        user_id = update.message.from_user.id
        reply_keyboard = [['Мало занимаюсь', 'Средне', 'Много']]
        with Session(engine) as session:
            user = session.get(User, user_id)
            user.height = height
            session.commit()

        await update.message.reply_text(
            'Укажите ваш уровень активности:',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return RegistrationStates.GET_ACTIVITY
    except ValueError:
        await update.message.reply_text('Пожалуйста, введите числовое значение роста.')
        return RegistrationStates.GET_HEIGHT

async def get_activity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    activity_level = update.message.text
    user_id = update.message.from_user.id
    reply_keyboard = [['Худеть', 'Набирать вес', 'Поддерживать вес']]
    with Session(engine) as session:
        user = session.get(User, user_id)
        user.activity_level = activity_level
        session.commit()

    await update.message.reply_text(
        'Укажите вашу цель:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return RegistrationStates.GET_GOAL

async def get_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    goal = update.message.text
    user_id = update.message.from_user.id
    with Session(engine) as session:
        user = session.get(User, user_id)
        user.goal = goal
        calculate_calories(user)
        session.commit()

    await update.message.reply_text(
        f'Регистрация завершена!\nВаша суточная норма калорий: {int(user.calories)} ккал.',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# Функция для расчета калорий
def calculate_calories(user):
    if user.gender == 'Мужской':
        bmr = 88.36 + (13.4 * user.weight) + (4.8 * user.height) - (5.7 * user.age)
    else:
        bmr = 447.6 + (9.2 * user.weight) + (3.1 * user.height) - (4.3 * user.age)

    activity_factor = 1.2 if user.activity_level == 'Мало занимаюсь' else 1.55 if user.activity_level == 'Средне' else 1.725
    goal_factor = 0.85 if user.goal == 'Худеть' else 1.15 if user.goal == 'Набирать вес' else 1.0

    daily_calories = bmr * activity_factor * goal_factor
    user.calories = daily_calories

# Функция для обновления кликов через WebApp
async def webapp_data_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.message.web_app_data.data
    user_id = update.message.from_user.id
    
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user:
            user.clicks += int(data)
            session.commit()

    await update.message.reply_text(f"Ваши клики обновлены: {user.clicks}")

# Функция для запуска игры через WebApp
async def start_game(update, context):
    keyboard = [
        [InlineKeyboardButton("Начать игру", web_app=WebAppInfo(url=WEBAPP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Нажмите кнопку ниже, чтобы начать игру:', reply_markup=reply_markup)


# Функция для кликов
async def click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            await update.message.reply_text('Сначала зарегистрируйтесь командой /register')
            return

        user.clicks = (user.clicks or 0) + 1
        session.commit()

        await update.message.reply_text(f'Вы кликнули на мозг! Всего кликов: {user.clicks}')

# Основная функция для запуска бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('register', register)],
        states={
            RegistrationStates.GET_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            RegistrationStates.GET_GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_gender)],
            RegistrationStates.GET_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            RegistrationStates.GET_WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_weight)],
            RegistrationStates.GET_HEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_height)],
            RegistrationStates.GET_ACTIVITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_activity)],
            RegistrationStates.GET_GOAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_goal)],
        },
        fallbacks=[],
    )

    app.add_handler(CommandHandler('start', start_game))
    app.add_handler(CommandHandler('click', click))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, webapp_data_handler))
    app.add_handler(conv_handler)

    app.run_polling()

if __name__ == '__main__':
    main()
