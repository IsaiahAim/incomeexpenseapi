from django.db import models
from user.models import  User

# Create your models here.

SOURCE_OPTIONS = [
    ('SALARY', 'SALARY'),
    ('BUSINESS', 'BUSINESS'),
    ('SIDE-HUSTLE', 'SIDE-HUSTLE'),
    ('OTHERS', 'OTHERS')

]


class Income(models.Model):
    source = models.CharField(choices=SOURCE_OPTIONS, max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)

    class Meta:
        ordering:['-date']

    def __str__(self):
        return f"{self.owner}'s Income"
