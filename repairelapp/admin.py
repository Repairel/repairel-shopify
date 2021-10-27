from django.contrib import admin
from .models import ShoeItem

class ShoeItemAdmin(admin.ModelAdmin):
    list_display = ['title',
                    'rating',
                    'description',
                    'updated',
                    'image',
                    'in_stock']

admin.site.register(ShoeItem, ShoeItemAdmin)