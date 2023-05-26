from django.contrib import admin
from .models import Sample
from .models import Guess
from .models import Comment

# Register your models here.
admin.site.register(Sample)
admin.site.register(Guess)
admin.site.register(Comment)