from django.db import models
from django.core.exceptions import ValidationError
from graphene.types import decimal
from . import apps

# Create your models here.


class Category(models.Model):
    name = models.CharField(null=False, max_length=50)
    datetime_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Uom(models.Model):
    "Unit of Measurement"
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50, null=False)
    datetime_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.symbol

    class Meta:
        ordering = ['name']


class Item(models.Model):

    def validate_value_not_negative(value):
        if value < 0:
            raise ValidationError("Value must be >= 0")

    name = models.TextField(null=False, max_length=255)
    name.isRender = True
    sku = models.CharField(max_length=20, unique=True, verbose_name="SKU")
    upc = models.CharField(max_length=20, unique=True, verbose_name="UPC")
    image = models.ImageField(null=True)
    category = models.ForeignKey(
        Category, related_name='items', default=1, on_delete=models.SET_DEFAULT)
    price = models.DecimalField(max_digits=20, decimal_places=2, validators=[
                                validate_value_not_negative])
    uom = models.ForeignKey(Uom, default=0, on_delete=models.SET_DEFAULT,
                            verbose_name='unit of measurement')
    pack_qty = models.DecimalField(max_digits=20, decimal_places=4, validators=[
                                   validate_value_not_negative])
    datetime_updated = models.DateTimeField(auto_now_add=True)

    # price history from ItemHistory__price here?

    def __str__(self):
        return self.name

    def price_per_unit(self):
        if self.pack_qty > 0:
            return self.price/self.pack_qty
        else:
            return 0

    class Meta:
        ordering = ['name']
        verbose_name = "Item"
        verbose_name_plural = "Items"


class ItemHistory(models.Model):
    item = models.ForeignKey("Item", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    # price may be default value as of last reported.
    datetime_report = models.DateTimeField(
        verbose_name='Report Time', auto_now_add=True)
    # todo: report_user: who reports the price
    # todo: store: which store report comes from

    def __str__(self):
        return self.item.name

    class Meta:
        ordering = ['-datetime_report']
        verbose_name = "Item History"
        verbose_name_plural = "Item History"
        db_table = 'aldi_item_history'
