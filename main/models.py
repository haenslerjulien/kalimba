from django.db import models
from django_mysql.models import SizedTextField
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# SAMPLE 
# A sample is an audio clip posted by a user. It can be guessed by other users.

class Sample(models.Model):
    text = SizedTextField(size_class=1, null=True, blank=True) #255 Max
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="samples", null=True)
    file = models.FileField(blank=True, default="", upload_to="samples/", 
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav'])])
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = True

    def __str__(self):
        return self.text

# GUESS 
# A guess is the response from a user to a sample. It can be approved, commented, upvoted
class Guess(models.Model):
    text = SizedTextField(size_class=1, null=True, blank=True) #255 Max
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name="guesses")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="guesses", null=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    approved = models.BooleanField(default=False) # Has the guess been confirmed by the sample's author
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

# COMMENT
# A comment is an answer to a guess
class Comment(models.Model):
    text = SizedTextField(size_class=1, null=True, blank=True) #255 Max
    guess = models.ForeignKey(Guess, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)