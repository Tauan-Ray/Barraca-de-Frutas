from django.db import models

class Fruits(models.Model):
    fresh_fruits_options = (
        ('Y', 'Sim'),
        ('N', 'Não'),
    )

    classification_options = (
        ('EX', 'Extra'),
        ('1ST', 'De primeira'),
        ('2ND', 'De segunda'),
        ('3RD', 'De terceira'),
    )

    id = models.AutoField(primary_key=True)
    name =  models.CharField(max_length=100, unique=True)
    classification = models.CharField(max_length=3, choices=classification_options)
    fresh_fruits = models.CharField(max_length=1, choices=fresh_fruits_options)
    stock = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return self.name