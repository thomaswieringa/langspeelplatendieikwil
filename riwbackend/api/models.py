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
    image_url = models.CharField(max_length=100)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{} - {}".format(self.title, self.artist)

