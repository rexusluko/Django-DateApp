from django.contrib import admin

from .models import CustomUser, ZodiacSign, Compatibility, Like, Match

admin.site.register(CustomUser)
admin.site.register(ZodiacSign)
admin.site.register(Compatibility)
admin.site.register(Like)
admin.site.register(Match)
