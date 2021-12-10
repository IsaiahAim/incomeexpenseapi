from django.db import models
from user.models import  User

# Create your models here.

CATEGORY_OPTIONS = [
    ('ONLINE_SERVICES', 'ONLINE_SERVICES'),
    ('TRAVEL', 'TRAVEL'),
    ('FOOD', 'FOOD'),
    ('RENT', 'RENT'),
    ('OTHERS', 'OTHERS')

]


class Expense(models.Model):
    category = models.CharField(choices=CATEGORY_OPTIONS, max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.id}:{self.description}'
