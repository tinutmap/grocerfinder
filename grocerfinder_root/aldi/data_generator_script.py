from aldi.models import Item
for new_item in range(3,20):
    id = new_item
    new_item=str(new_item)
    Item(id=id,name=new_item,sku=new_item, upc=new_item,price=0, pack_qty=0).save()

Item.objects.get(pk=74).delete()


from aldi.models import Category
for new_category in range(2,20):
    id = new_category
    new_category=str(new_category)
    Category(id=id,name=new_category).save()