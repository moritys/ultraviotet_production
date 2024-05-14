from django.db import models


class Component(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    critical_quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name
