from django.db.models.base import Model
from django.forms import ModelForm
from .models import Item, Category


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ('id', 'name', 'sku', 'upc', 'category',
                  'price', 'pack_qty')


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('id', 'name')
