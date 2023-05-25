from django.db import models
from django_mysql.models import SizedTextField
from django.contrib.auth.models import User

# SAMPLE 
# A sample is an audio clip posted by a user. It can be guessed by other users.

class Sample(models.Model):
    text = SizedTextField(size_class=1, null=True, blank=True) #255 Max
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="samples", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

# GUESS 
# A guess is the response from a user to a sample. It can be approved, commented, upvoted
class Guess(models.Model):
    text = SizedTextField(size_class=1, null=True, blank=True) #255 Max
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="guesses", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

# COMMENT
# A comment is an answer to a guess
class Comment(models.Model):
    text = SizedTextField(size_class=1, null=True, blank=True) #255 Max
    guess = models.ForeignKey(Guess, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)