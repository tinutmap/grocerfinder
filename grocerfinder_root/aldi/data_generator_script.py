from aldi.models import Category
from aldi.models import Item
from aldi.models import Uom
import datetime

for new_category in range(1, 2):
    new_category = str(new_category)
    Category(name=new_category).save()

Uom(id=0, symbol='ea', name='each').save()

uom = Uom.objects.get(pk=0)

for new_item in range(1, 20):
    new_item = str(new_item)
    Item(name=new_item, sku=new_item,
         upc=new_item, price=0, pack_qty=0, uom=uom,
         datetime_updated=datetime.datetime.now()
         ).save()

# Item.objects.get(pk=74).delete()
