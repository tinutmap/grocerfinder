'''
Item schema
'''
from graphene_django import DjangoObjectType
import graphene
from aldi.models import Item
from aldi.forms import ItemForm
from .base import MutationPayLoad, delete_entity, resolve_model_fetch_more, DjangoModelFormMutationLoginRequired
from graphql_jwt.decorators import login_required


class ItemType(DjangoObjectType):
    class Meta:
        model = Item
        fields = ('name', 'sku', 'upc', 'image', 'category',
                  'price', 'uom', 'pack_qty', 'datetime_updated')

    # force id to be Int rather than String
    id = graphene.Int()
    price = graphene.Decimal()

    def resolve_id(self, context):
        return self.id


class ItemFormCreateMutation(DjangoModelFormMutationLoginRequired):
    class Meta:
        form_class = ItemForm


class ItemFormUpdateMutation(DjangoModelFormMutationLoginRequired, MutationPayLoad):
    class Meta:
        form_class = ItemForm


class ItemDeleteMutation(MutationPayLoad, graphene.Mutation):
    class Arguments:
        id_list = graphene.List(graphene.Int, required=True)

    id_deleted = graphene.List(graphene.Int)
    id_not_exist = graphene.List(graphene.Int)

    @classmethod
    @login_required
    def mutate(cls, parent, info, id_list):
        id_deleted, errors, id_not_exist = delete_entity(Item, id_list)
        return ItemDeleteMutation(id_deleted=id_deleted,
                                  errors=errors,
                                  id_not_exist=id_not_exist)


###############################################################################
# Query and Mutation


class Query(graphene.ObjectType):
    # Item
    all_items = graphene.List(ItemType)
    item_by_id = graphene.Field(ItemType, id=graphene.Int(required=True))
    item_fetch_more = graphene.List(
        ItemType,
        cursor=graphene.String(required=True),
        cursor_id=graphene.Int(required=True),
        page_size=graphene.Int(required=True),
        sort_by_field=graphene.String(required=True, default_value='id')
    )

    def resolve_all_items(parent, info):
        return Item.objects.all().order_by('-id')

    def resolve_item_by_id(parent, info, id):
        try:
            return Item.objects.get(pk=id)
        except Item.DoesNotExist:
            return None

    def resolve_item_fetch_more(parent, info, cursor, cursor_id, page_size, sort_by_field):
        return resolve_model_fetch_more(Item, cursor, cursor_id, page_size, sort_by_field)


class Mutation(graphene.ObjectType):
    item_create_by_form = ItemFormCreateMutation.Field()
    item_update_by_form = ItemFormUpdateMutation.Field()
    delete_item = ItemDeleteMutation.Field()
