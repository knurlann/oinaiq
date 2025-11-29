"""
Booking and mock payment handlers.
"""

from __future__ import annotations

from aiogram import F, Router
from aiogram.types import CallbackQuery

from oynaiq_bot.data.matches import get_match_by_id
from oynaiq_bot.keyboards.booking import build_booking_keyboard
from oynaiq_bot.utils.navigator import BookingCallback, PaymentCallback


router = Router(name="booking")


@router.callback_query(BookingCallback.filter(F.action == "deposit"))
async def start_booking(
    callback: CallbackQuery,
    callback_data: BookingCallback,
) -> None:
    """
    Start the booking flow after \"💳 Забронировать место\" click.

    Shows payment confirmation message with mock payment buttons.
    """

    match = get_match_by_id(callback_data.match_id)
    if not match:
        await callback.answer("Матч не найден.", show_alert=True)
        return

    text = (
        f"💳 Забронировать место за {match.deposit} ₸\n"
        "1) Оплати через Kaspi Pay по ссылке ниже.\n"
        "2) Затем нажми «Я оплатил через Kaspi».\n\n"
        "Ссылка для оплаты: "
        '<a href="https://pay.kaspi.kz/pay/df3xuh5c">Kaspi Pay</a>\n\n'
        "Деньги возвращаются при явке или при отмене за 24 часа."
    )
    await callback.message.answer(text, reply_markup=build_booking_keyboard(match))
    await callback.answer()


@router.callback_query(PaymentCallback.filter())
async def handle_mock_payment(
    callback: CallbackQuery,
    callback_data: PaymentCallback,
) -> None:
    """
    Handle mock payment confirmation or cancellation.

    Payment is not actually processed; we simply emulate the success flow.
    """

    match = get_match_by_id(callback_data.match_id)
    if not match:
        await callback.answer("Матч не найден.", show_alert=True)
        return

    if callback_data.action == "pay":
        # Условно увеличиваем количество подтверждённых игроков
        if match.players_current < match.players_total:
            match.players_current += 1
        await callback.answer("Оплата через Kaspi отмечена 💸", show_alert=True)
        await callback.message.answer(
            "🎉 Место забронировано!\n"
            f"📍 Игра: {match.location}, {match.date_human} {match.time_human}\n"
            "🔔 Мы напомним тебе за 2 часа до начала.",
        )
    else:
        await callback.answer("Оплата отменена.", show_alert=True)



