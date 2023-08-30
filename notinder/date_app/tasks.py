from celery import shared_task
from .models import Like, Match, CustomUser

@shared_task
def create_like(sender_id, receiver_id):
    sender = CustomUser.objects.get(id=sender_id)
    receiver = CustomUser.objects.get(id=receiver_id)
    like = Like.objects.create(sender=sender, receiver=receiver, is_liked=True)
    if Like.objects.filter(sender=receiver, receiver=sender, is_liked=True).exists():
        Match.objects.create(friend1=sender, friend2=receiver)

@shared_task
def create_dislike(sender_id, receiver_id):
    sender = CustomUser.objects.get(id=sender_id)
    receiver = CustomUser.objects.get(id=receiver_id)
    dislike = Like.objects.create(sender=sender, receiver=receiver, is_liked=False)