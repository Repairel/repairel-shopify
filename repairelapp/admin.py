from django.contrib import admin
from .models import ShoeItem, ShoeRequest, UserAccount, WishListItem

class ShoeItemAdmin(admin.ModelAdmin):
    list_display = ['title',
                    'rating',
                    'description',
                    'created',
                    'updated',
                    'image',
                    'in_stock']

admin.site.register(ShoeItem, ShoeItemAdmin)


class WishListItemAdmin(admin.ModelAdmin):
    list_display = ['title',
                    'rating',
                    'description',
                    'updated',
                    'image',
                    'in_stock']

admin.site.register(WishListItem, WishListItemAdmin)


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['name',
                    'last_name',
                    'email',
                    'password',
                    'image']

admin.site.register(UserAccount, UserAccountAdmin)


class ShoeRequestAdmin(admin.ModelAdmin):
    list_display = ['name',
                    'description',
                    'author']

admin.site.register(ShoeRequest, ShoeRequestAdmin)