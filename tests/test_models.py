from datetime import datetime, timezone

from django.core.exceptions import ValidationError
from django.test import TestCase

from restaurant.models import Booking, Menu


class MenuTest(TestCase):
    def test_get_item(self):
        item = Menu.objects.create(title='IceCream', price=80, inventory=100)
        self.assertEqual(str(item), 'IceCream : 80')

    def test_negative_price_is_rejected(self):
        item = Menu(title='Free lunch', price=-1, inventory=1)
        with self.assertRaises(ValidationError):
            item.full_clean()


class BookingTest(TestCase):
    def test_str_and_persistence(self):
        when = datetime(2026, 12, 24, 19, 30, tzinfo=timezone.utc)
        booking = Booking.objects.create(
            name='Adrian', no_of_guests=4, booking_date=when
        )
        booking.refresh_from_db()
        self.assertEqual(str(booking), 'Adrian (4) on 2026-12-24 19:30')
        self.assertEqual(Booking.objects.count(), 1)

    def test_zero_guests_is_rejected(self):
        when = datetime(2026, 12, 24, 19, 30, tzinfo=timezone.utc)
        booking = Booking(name='Mario', no_of_guests=0, booking_date=when)
        with self.assertRaises(ValidationError):
            booking.full_clean()
