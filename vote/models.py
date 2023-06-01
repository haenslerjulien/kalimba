from django.db import models
from django.contrib.auth.models import User
from main.models import Guess
from django_mysql.models import EnumField


class VoteType(models.TextChoices):
    UP = "Upvote"
    DOWN = "Downvote"

# Create your models here.
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votes", null=True)
    guess = models.ForeignKey(Guess, on_delete=models.CASCADE, related_name="votes", null=True)
    type = EnumField(choices=VoteType.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'guess'], name='unique_vote_user_guess'),
        ]