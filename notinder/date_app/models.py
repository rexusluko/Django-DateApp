from django.contrib.auth.models import AbstractUser
from django.db import models


class ZodiacSign(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Знаки зодиака"


class Compatibility(models.Model):
    sign1 = models.ForeignKey('ZodiacSign', on_delete=models.PROTECT, related_name='compatibility_sign1')
    sign2 = models.ForeignKey('ZodiacSign', on_delete=models.PROTECT, related_name='compatibility_sign2')
    weight = models.IntegerField()

    def __str__(self):
        return f"{self.sign1.name} + {self.sign2.name}"

    class Meta:
        verbose_name_plural = "Совместимость"


class CustomUser(AbstractUser):
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=7)
    zodiac_sign = models.ForeignKey('ZodiacSign', on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    photo_path = models.TextField(null=True)

    first_name = None
    last_name = None
    last_login = None


class Like(models.Model):
    sender = models.ForeignKey('CustomUser', on_delete=models.PROTECT, related_name='like_sender')
    receiver = models.ForeignKey('CustomUser', on_delete=models.PROTECT, related_name='like_receiver')
    is_liked = models.BooleanField()

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"

    class Meta:
        verbose_name_plural = "Лайки"



class Match(models.Model):
    friend1 = models.ForeignKey('CustomUser', on_delete=models.PROTECT, related_name='match_friend1')
    friend2 = models.ForeignKey('CustomUser', on_delete=models.PROTECT, related_name='match_friend2')

    def __str__(self):
        return f"{self.friend1.username} + {self.friend2.username}"

    class Meta:
        verbose_name_plural = "Друзья"
