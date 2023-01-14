from django.contrib.auth.models import User
from django.db import models


class Master(models.Model):
    """
    Model for the master of a record. Mirrors Discogs master database.
    """
    master_id = models.IntegerField()
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    year = models.IntegerField()
    discogs_url = models.CharField(max_length=100)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{} - {}".format(self.title, self.artist)


class Offer(models.Model):
    """
    Model for a record offer.
    """
    master = models.ForeignKey(Master, on_delete=models.DO_NOTHING)
    url = models.CharField(max_length=1000)
    title = models.CharField(max_length=1000)
    seller = models.CharField(max_length=1000)
    seller_url = models.CharField(max_length=1000)
    media_condition = models.CharField(max_length=100)
    sleeve_condition = models.CharField(max_length=100)
    price = models.FloatField()
    shipping = models.FloatField()
    currency = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    image_url = models.CharField(max_length=100)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title
