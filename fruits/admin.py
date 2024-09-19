from django.contrib import admin
from fruits.models import Fruits


class FruitsAdmin(admin.ModelAdmin):
    list_display = ('name', 'classification', 'fresh_fruits', 'stock', 'price')
    search_fields = ('name',)


admin.site.register(Fruits, FruitsAdmin)