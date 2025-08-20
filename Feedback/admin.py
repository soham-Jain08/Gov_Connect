from django.contrib import admin
from .models import Feedback, UserAccount 

# Register your models here.
admin.site.register(Feedback)
admin.site.register(UserAccount)