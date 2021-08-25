from django.contrib import admin
from aldi.models import Category, Item, Uom, ItemHistory

# Register your models here.

admin.site.register(Category)

admin.site.register(Uom)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price_per_unit')


admin.site.register(Item, ItemAdmin)

admin.site.register(ItemHistory)
