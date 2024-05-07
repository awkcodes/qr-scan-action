from django.db import models

class Offer(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    redeemed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
