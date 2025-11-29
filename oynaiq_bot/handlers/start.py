"""
Start and main menu handlers for OynaIQ.bot.

This module defines the /start command and text handlers for the main
reply keyboard buttons.
"""

from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from oynaiq_bot.data.matches import Match, MatchStatus, MOCK_MATCHES, get_matches_by_sport
from oynaiq_bot.keyboards.create_game import (
    build_create_game_sport_keyboard,
    remove_keyboard,
)
from oynaiq_bot.keyboards.find_team import build_sport_choice_keyboard
from oynaiq_bot.keyboards.main_menu import build_main_menu_keyboard
from oynaiq_bot.keyboards.matches_list import build_matches_list_keyboard
from oynaiq_bot.utils.formatter import format_matches_intro
from oynaiq_bot.utils.navigator import SPORTS


router = Router(name="start")


class CreateMatchForm(StatesGroup):
    """
    Finite‑state machine for the \"Создать игру\" flow.

    Steps:
        1. sport  – choose sport.
        2. title  – enter match title.
        3. location – enter location.
        4. datetime – enter date and time.
        5. deposit – enter deposit amount.
    """

    sport = State()
    title = State()
    location = State()
    datetime = State()
    deposit = State()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """
    Handle the /start command.

    Sends the welcome text and shows the main menu keyboard.
    Also supports optional referral payloads of the form ``ref_<username>``.
    """

    args = message.text.split(maxsplit=1)
    referral_info = ""
    if len(args) == 2 and args[1].startswith("ref_"):
        ref_username = args[1][4:]
        referral_info = (
            f"\n\nТы пришёл по приглашению пользователя @{ref_username}. "
            "В будущем здесь можно будет начислять бонусы за приглашения."
        )

    await message.answer(
        "👋 Привет! Это OynaIQ Bot — здесь ты можешь найти игроков для ⚽🏀🏐 игр. "
        "Что хочешь сделать?" + referral_info,
        reply_markup=build_main_menu_keyboard(),
    )


@router.message(Command("Nurlan"))
async def secret_nurlan_from_start(message: Message, state: FSMContext) -> None:
    """
    Secret command handler that works regardless of current FSM state.

    If the user was in the middle of a form (e.g. creating a match),
    the state is cleared and the special message is always returned.
    """

    await state.clear()
    await message.answer("Люблю тебя, пусанай!")


@router.message(F.text == "🧑‍🤝‍🧑 Найти команду")
async def on_find_team_clicked(message: Message) -> None:
    """
    Entry point for the \"Найти команду\" flow from the main menu.

    Shows sport selection inline keyboard.
    """

    await message.answer(
        "Выбери игру, которая тебе интересна 👇",
        reply_markup=build_sport_choice_keyboard(),
    )


@router.message(F.text == "⚡ Создать игру")
async def on_create_game_clicked(message: Message, state: FSMContext) -> None:
    """
    Entry point for the \"Создать игру\" flow.

    Starts a short wizard that asks the user for sport, title, location,
    date/time and deposit. Data is not stored in a real database yet, but
    the collected information is summarized at the end.
    """

    await state.set_state(CreateMatchForm.sport)
    await message.answer(
        "Давай создадим новую игру ⚡\n\n"
        "Сначала выбери вид спорта:",
        reply_markup=build_create_game_sport_keyboard(),
    )


@router.message(CreateMatchForm.sport)
async def create_match_choose_sport(message: Message, state: FSMContext) -> None:
    """
    Handle sport selection during match creation.
    """

    text = message.text or ""
    # Find internal sport code by label
    matched_code = None
    for code, label in SPORTS.items():
        if text == label:
            matched_code = code
            break

    if matched_code is None:
        await message.answer(
            "Пожалуйста, выбери один из вариантов на клавиатуре 🙂",
            reply_markup=build_create_game_sport_keyboard(),
        )
        return

    await state.update_data(sport=matched_code)
    await state.set_state(CreateMatchForm.title)
    await message.answer(
        "Как назовём матч? Например: «Футбол 5×5»",
        reply_markup=remove_keyboard(),
    )


@router.message(CreateMatchForm.title)
async def create_match_set_title(message: Message, state: FSMContext) -> None:
    """
    Save match title and ask for location.
    """

    title = (message.text or "").strip()
    if not title:
        await message.answer("Название не может быть пустым. Попробуй ещё раз.")
        return

    await state.update_data(title=title)
    await state.set_state(CreateMatchForm.location)
    await message.answer("Где играем? Напиши название площадки или адрес.")


@router.message(CreateMatchForm.location)
async def create_match_set_location(message: Message, state: FSMContext) -> None:
    """
    Save location and ask for date/time.
    """

    location = (message.text or "").strip()
    if not location:
        await message.answer("Локация не может быть пустой. Введи, пожалуйста, адрес.")
        return

    await state.update_data(location=location)
    await state.set_state(CreateMatchForm.datetime)
    await message.answer(
        "Когда играем?\n"
        "Например: «сегодня, 19:00» или «завтра в 18:30».",
    )


@router.message(CreateMatchForm.datetime)
async def create_match_set_datetime(message: Message, state: FSMContext) -> None:
    """
    Save human‑readable date/time and ask for deposit.
    """

    datetime_text = (message.text or "").strip()
    if not datetime_text:
        await message.answer("Пожалуйста, укажи дату и время игры.")
        return

    await state.update_data(datetime=datetime_text)
    await state.set_state(CreateMatchForm.deposit)
    await message.answer(
        "Какой будет депозит за игру? Напиши сумму в тенге, например: 200.\n"
        "Если депозита нет — напиши 0.",
    )


@router.message(CreateMatchForm.deposit)
async def create_match_set_deposit(message: Message, state: FSMContext) -> None:
    """
    Save deposit amount and finish the wizard with a summary.
    """

    raw = (message.text or "").replace(" ", "")
    try:
        deposit = int(raw)
        if deposit < 0:
            raise ValueError
    except ValueError:
        await message.answer("Нужно указать неотрицательное число. Попробуй ещё раз 🙂")
        return

    await state.update_data(deposit=deposit)
    data = await state.get_data()
    await state.clear()

    sport_code = data.get("sport", "")
    sport_label = SPORTS.get(sport_code, sport_code)
    title = data.get("title", "Без названия")
    location = data.get("location", "Не указано")
    datetime_text = data.get("datetime", "Не указано")

    # Try to roughly split date and time for formatting
    date_human = datetime_text
    time_human = ""
    for sep in [",", " в "]:
        if sep in datetime_text:
            parts = [p.strip() for p in datetime_text.split(sep, 1)]
            if len(parts) == 2:
                date_human, time_human = parts
            break

    new_id = max((m.id for m in MOCK_MATCHES), default=0) + 1
    players_total = 10
    players_current = 1  # организатор

    free_slots = max(players_total - players_current, 0)
    if free_slots <= 0:
        status = MatchStatus.ACTIVE
    elif free_slots <= 2:
        status = MatchStatus.ALMOST_FULL
    else:
        status = MatchStatus.LOW_PLAYERS

    organizer_username = message.from_user.username or str(message.from_user.id)
    google_maps_url = f"https://maps.google.com/?q={location.replace(' ', '+')}"
    rules = "Правила договоримся на месте 😉"
    refund_policy = (
        "Возврат депозита при отмене за 24+ ч" if deposit > 0 else "Без депозита — просто приходи"
    )

    new_match = Match(
        id=new_id,
        sport=sport_code or "other",
        title=title,
        location=location,
        date_human=date_human,
        time_human=time_human,
        google_maps_url=google_maps_url,
        players_current=players_current,
        players_total=players_total,
        deposit=deposit,
        level="любители",
        organizer_username=organizer_username,
        rules=rules,
        refund_policy=refund_policy,
        status=status,
    )
    MOCK_MATCHES.append(new_match)

    summary = (
        "Игра создана ✅\n\n"
        f"Вид спорта: {sport_label}\n"
        f"Название: {title}\n"
        f"Локация: {location}\n"
        f"Когда: {datetime_text}\n"
        f"Депозит: {deposit} ₸\n\n"
        "Мы добавили игру в общий список — другие игроки теперь могут её найти "
        "в разделе «Найти команду»."
    )

    await message.answer(summary, reply_markup=build_main_menu_keyboard())

    # Показать пользователю, как матч выглядит в общем списке
    if sport_code:
        matches = get_matches_by_sport(sport_code)
        await message.answer(
            format_matches_intro(sport_code),
            reply_markup=build_matches_list_keyboard(sport_code, matches),
        )


@router.message(F.text == "💬 Узнать, как это работает")
async def on_how_it_works_clicked(message: Message) -> None:
    """
    Explain how the service works in a few simple steps.
    """

    text = (
        "Как работает OynaIQ.bot:\n\n"
        "1️⃣ Выбираешь вид спорта и находишь ближайшие матчи.\n"
        "2️⃣ Смотришь детали: время, локацию, уровень, депозит.\n"
        "3️⃣ Подтверждаешь участие или бронируешь место.\n"
        "4️⃣ Приходишь на игру — мы напомним за 2 часа до начала.\n\n"
        "Сейчас данные тестовые, но логика уже как в реальном сервисе 🙂"
    )
    await message.answer(text, reply_markup=build_main_menu_keyboard())



