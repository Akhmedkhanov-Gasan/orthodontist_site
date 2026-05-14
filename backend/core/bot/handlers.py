from django.conf import settings

from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ContextTypes

from core.bot.keyboards import (
    BUTTON_APPOINTMENT,
    BUTTON_CONTACTS,
    BUTTON_INFO,
    BUTTON_REGISTER,
    build_main_keyboard,
    build_phone_keyboard,
)
from core.bot.services import (
    create_appointment_for_patient,
    create_or_update_patient_from_telegram,
    format_new_patient_admin_message,
    get_patient_by_telegram_id,
    parse_appointment_date,
)
from core.bot.state import (
    WAITING_FOR_APPOINTMENT_DATE,
    WAITING_FOR_NAME,
    WAITING_FOR_PHONE,
    clear_registration,
    clear_user_state,
    get_registration_name,
    get_user_state,
    set_registration_name,
    set_user_state,
)
from core.bot.validators import normalize_phone


@sync_to_async
def set_user_state_async(user_id, state):
    set_user_state(user_id, state)


@sync_to_async
def get_user_state_async(user_id):
    return get_user_state(user_id)


@sync_to_async
def set_registration_name_async(user_id, name):
    set_registration_name(user_id, name)


@sync_to_async
def clear_registration_async(user_id):
    clear_registration(user_id)


@sync_to_async
def get_registration_name_async(user_id):
    return get_registration_name(user_id)


@sync_to_async
def create_or_update_patient_from_telegram_async(
    *,
    telegram_id,
    telegram_username,
    full_name,
    phone,
):
    return create_or_update_patient_from_telegram(
        telegram_id=telegram_id,
        telegram_username=telegram_username,
        full_name=full_name,
        phone=phone,
    )


@sync_to_async
def clear_user_state_async(user_id):
    clear_user_state(user_id)


@sync_to_async
def get_patient_by_telegram_id_async(telegram_id):
    return get_patient_by_telegram_id(telegram_id)


@sync_to_async
def create_appointment_for_patient_async(*, patient, preferred_date):
    return create_appointment_for_patient(
        patient=patient,
        preferred_date=preferred_date,
    )


@sync_to_async
def parse_appointment_date_async(value):
    return parse_appointment_date(value)

# Commands

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте! Это бот ортодонтического кабинета.\n\n"
        "Здесь можно зарегистрироваться, записаться на приём, "
        "получить контакты или справочную информацию.",
        reply_markup=build_main_keyboard(),
    )

async def show_contacts(update: Update):
    await update.message.reply_text(
        "Контакты клиники:\n\n"
        "Телефон: +7 999 999-99-99\n"
        "Адрес: укажите адрес клиники\n"
        "Время работы: укажите график работы",
        reply_markup=build_main_keyboard(),
    )


async def show_info(update: Update):
    await update.message.reply_text(
        "Раздел с информацией скоро появится.",
        reply_markup=build_main_keyboard(),
    )


async def start_appointment(update: Update):
    user_id = update.effective_user.id
    patient = await get_patient_by_telegram_id_async(user_id)

    if not patient:
        await update.message.reply_text(
            "Сначала зарегистрируйтесь, пожалуйста. Нажмите кнопку “Зарегистрироваться”.",
            reply_markup=build_main_keyboard(),
        )
        return

    await set_user_state_async(user_id, WAITING_FOR_APPOINTMENT_DATE)

    await update.message.reply_text(
        "Введите желаемую дату приёма в формате ДД.ММ.ГГГГ.\n"
        "Например: 25.05.2026",
        reply_markup=build_main_keyboard(),
    )


async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user_id = update.effective_user.id

    if text == BUTTON_REGISTER:
        await set_user_state_async(user_id, WAITING_FOR_NAME)
        await update.message.reply_text("Напишите, пожалуйста, ваше имя.")
        return

    if text == BUTTON_CONTACTS:
        await show_contacts(update)
        return

    if text == BUTTON_INFO:
        await show_info(update)
        return

    if text == BUTTON_APPOINTMENT:
        await start_appointment(update)
        return

    state = await get_user_state_async(user_id)

    if state == WAITING_FOR_NAME:
        await set_registration_name_async(user_id, text)
        await set_user_state_async(user_id, WAITING_FOR_PHONE)
        await update.message.reply_text(
            "Спасибо. Теперь отправьте, пожалуйста, номер телефона.",
            reply_markup=build_phone_keyboard(),
        )
        return

    if state == WAITING_FOR_PHONE:
        phone = normalize_phone(text)

        if not phone:
            await update.message.reply_text(
                "Пожалуйста, введите телефон в формате +79999999999 "
                "или нажмите кнопку “Поделиться контактом”.",
                reply_markup=build_phone_keyboard(),
            )
            return

        await finish_registration(update, context, phone)
        return

    if state == WAITING_FOR_APPOINTMENT_DATE:
        preferred_date, date_error = await parse_appointment_date_async(text)

        if date_error == "invalid_format":
            await update.message.reply_text(
                "Не получилось распознать дату. Введите корректную дату в формате ДД.ММ.ГГГГ.\n"
                "Например: 25.05.2026",
                reply_markup=build_main_keyboard(),
            )
            return

        if date_error == "past_date":
            await update.message.reply_text(
                "Дата приёма не может быть в прошлом. Введите корректную дату в формате ДД.ММ.ГГГГ.\n"
                "Например: 25.05.2026",
                reply_markup=build_main_keyboard(),
            )
            return

        patient = await get_patient_by_telegram_id_async(user_id)

        if not patient:
            await clear_user_state_async(user_id)
            await update.message.reply_text(
                "Не нашёл вашу регистрацию. Сначала зарегистрируйтесь, пожалуйста.",
                reply_markup=build_main_keyboard(),
            )
            return

        appointment = await create_appointment_for_patient_async(
            patient=patient,
            preferred_date=preferred_date,
        )

        await clear_user_state_async(user_id)

        await update.message.reply_text(
            "Спасибо, заявка на приём создана. Администратор свяжется с вами для подтверждения.",
            reply_markup=build_main_keyboard(),
        )

        admin_chat_id = getattr(settings, "TELEGRAM_ADMIN_CHAT_ID", "")

        if admin_chat_id:
            await context.bot.send_message(
                chat_id=admin_chat_id,
                text=(
                    "Новая заявка на приём\n\n"
                    f"Пациент: {patient.full_name}\n"
                    f"Телефон: {patient.phone}\n"
                    f"Дата: {appointment.preferred_date:%d.%m.%Y}\n"
                    f"Telegram ID: {patient.telegram_id}"
                ),
            )

        return


    await update.message.reply_text(
        "Выберите нужный пункт ниже или отправьте /start.",
        reply_markup=build_main_keyboard(),
    )


async def contact_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state = await get_user_state_async(user_id)

    if state != WAITING_FOR_PHONE:
        await update.message.reply_text(
            "Выберите нужный пункт ниже или отправьте /start.",
            reply_markup=build_main_keyboard(),
        )
        return

    contact = update.message.contact

    if contact.user_id and contact.user_id != user_id:
        await update.message.reply_text("Пожалуйста, отправьте свой контакт.")
        return

    phone = normalize_phone(contact.phone_number)

    if not phone:
        await update.message.reply_text(
            "Не получилось распознать номер телефона. "
            "Введите его вручную в формате +79999999999.",
            reply_markup=build_phone_keyboard(),
        )
        return

    await finish_registration(update, context, phone)


async def finish_registration(update: Update, context: ContextTypes.DEFAULT_TYPE, phone: str):
    user_id = update.effective_user.id
    username = update.effective_user.username

    full_name = await get_registration_name_async(user_id)

    if not full_name:
        await clear_registration_async(user_id)
        await update.message.reply_text(
            "Регистрация устарела. Начните заново через /start.",
            reply_markup=build_main_keyboard(),
        )
        return

    patient, created = await create_or_update_patient_from_telegram_async(
        telegram_id=user_id,
        telegram_username=username,
        full_name=full_name,
        phone=phone,
    )

    await clear_registration_async(user_id)

    admin_chat_id = getattr(settings, "TELEGRAM_ADMIN_CHAT_ID", "")

    if admin_chat_id:
        await context.bot.send_message(
            chat_id=admin_chat_id,
            text=format_new_patient_admin_message(patient, created),
        )

    await update.message.reply_text(
        "Спасибо, мы получили ваши данные.",
        reply_markup=build_main_keyboard(),
    )


async def register_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await set_user_state_async(user_id, WAITING_FOR_NAME)
    await update.message.reply_text("Напишите, пожалуйста, ваше имя.")


async def appointment_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_appointment(update)


async def contacts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_contacts(update)


async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_info(update)
