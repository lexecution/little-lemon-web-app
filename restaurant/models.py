from django.core.validators import MinValueValidator
from django.db import models


class Menu(models.Model):
    """A dish on the Little Lemon menu."""

    title = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    inventory = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.title} : {str(self.price)}'


class Booking(models.Model):
    """A table reservation."""

    name = models.CharField(max_length=255)
    no_of_guests = models.IntegerField(validators=[MinValueValidator(1)])
    booking_date = models.DateTimeField()

    class Meta:
        ordering = ['booking_date', 'id']

    def __str__(self):
        return f'{self.name} ({self.no_of_guests}) on {self.booking_date:%Y-%m-%d %H:%M}'
