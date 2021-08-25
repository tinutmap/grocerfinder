import graphene
from graphene.types import Decimal
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql_jwt.decorators import login_required
from .models import Item, Category
from .forms import ItemForm, CategoryForm
from django.db import IntegrityError, connection
from graphql import GraphQLError

###############################################################################
# Base Classes and Functions


class MutationPayLoad(graphene.ObjectType):
    ok = graphene.Boolean(required=True)
    errors = graphene.List(graphene.String)
    query = graphene.Field('grocerfinder.schema.Query', required=True)

    def resolve_ok(self, info):
        return len(self.errors or []) == 0

    def resolve_errros(self, info):
        return self.errors or []

    def resolve_query(self, info):
        return {}


def delete_entity(model, id_list):
    id_deleted = []
    errors = []
    id_not_exist = []
    model_name = model._meta.model_name
    for id in id_list:
        try:
            model.objects.get(pk=id).delete()

            # check_constaints() below used to catch IntegrityError exception
            # when category.id=1 -- 'default' category is tried to be deleted
            # when GRAPHENE.'ATOMIC_MUTATIONS': True in settings
            # learned from https://github.com/pytest-dev/pytest-django/issues/754#issuecomment-519987086
            connection.check_constraints()

            id_deleted.append(id)
        except model.DoesNotExist:
            id_not_exist.append(id)
        except IntegrityError:
            errors.append('Integrity Error')
            id_not_exist.append(id)
            # reconnect to database so remaining id(s) in for loop can be deleted
            connection.connect()
        except:
            errors.append('Unknown error')
            id_not_exist.append(id)
            # reconnect to database so remaining id(s) in for loop can be deleted
            connection.connect()

    if id_not_exist:
        errors.append(
            f'{model_name} id(s) {str(id_not_exist)[1:-1]} not exist')

    return id_deleted, errors, id_not_exist


###############################################################################
# Category schema


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id', 'name', 'datetime_updated')

    id = graphene.Int()
    datetime_updated = graphene.DateTime()
    verbose_names = graphene.List(graphene.String)

    # force id to be Int rather than String
    def resolve_id(self, info):
        return self.id

    def resolve_datetime_updated(self, info):
        return self.datetime_updated.replace(microsecond=0)

    def resolve_verbose_names(self, info):
        return ['ID', 'Category Name', 'Datetime Updated']


class CategoryInputType(graphene.InputObjectType):
    name = graphene.String(required=True)

# # Obsoleted by CategoryFormCreateMutation
# class CategoryCreateMutation(MutationPayLoad, graphene.Mutation):
#     class Arguments:
#         input = CategoryInputType()

#     category_instance = graphene.Field(CategoryType)

#     @classmethod
#     def mutate(cls, parent, info, input):
#         errors = []

#         if not errors:
#             category = Category(**input)
#             category.save()
#         return CategoryCreateMutation(errors=errors, category_instance=category)


class CategoryFormCreateMutation(DjangoModelFormMutation, MutationPayLoad):
    class Meta:
        form_class = CategoryForm

    class Input:
        input = CategoryInputType()


class CategoryFormUpdateMutation(DjangoModelFormMutation, MutationPayLoad):
    class Meta:
        form_class = CategoryForm


# class CategoryUpdateMutation(MutationPayLoad, graphene.Mutation):
#     class Arguments:
#         id = graphene.Int()
#         input = CategoryInputType()

#     @classmethod
#     def mutate(cls, parent, info, id, input):
#         errors = []

#         try:
#             category = Category.objects.get(pk=id)
#         except Category.DoesNotExist:
#             errors.append('Category not exist')

#         if not errors:
#             category.__dict__.update(**input)
#             category.save()

#         return CategoryUpdateMutation(errors=errors)


class CategoryDeleteMutation(MutationPayLoad, graphene.Mutation):

    class Arguments:
        id_list = graphene.List(graphene.Int, required=True)

    id_deleted = graphene.List(graphene.Int)
    id_not_exist = graphene.List(graphene.Int)

    @classmethod
    def mutate(cls, parent, info, id_list):
        id_deleted, errors, id_not_exist = delete_entity(Category, id_list)
        return CategoryDeleteMutation(id_deleted=id_deleted,
                                      errors=errors,
                                      id_not_exist=id_not_exist)

###############################################################################
# Item schema


class ItemType(DjangoObjectType):
    price = Decimal()

    class Meta:
        model = Item
        fields = ('name', 'sku', 'upc', 'image', 'category',
                  'price', 'uom', 'pack_qty', 'datetime_updated')

    # force id to be Int rather than String
    id = graphene.Int()
    # name = graphene.String()

    def resolve_id(self, context):
        return self.id

    # def resolve_name(self, context):
    #     return str({'name': self.name, 'isRender': Item.name.field.isRender})


class ItemInputType(graphene.InputObjectType):
    name = graphene.String()
    id = graphene.Int()
    category_id = graphene.Int()

    # Bug: graphene.Decimal still outputs as String in API
    price = graphene.Decimal()
    pack_qty = graphene.Decimal(default="1")

    sku = graphene.String()
    upc = graphene.String()

# # Obsoleted by ItemFromCreateMutation
# class ItemCreateMutation(MutationPayLoad, graphene.Mutation):

#     class Arguments:
#         input = ItemInputType()

#     @classmethod
#     def mutate(cls, parent, info, input):
#         errors = []

#         if not errors:
#             item = Item(**input)
#             item.save()

#         return ItemCreateMutation(errors=errors)


class ItemFormCreateMutation(DjangoModelFormMutation):
    class Meta:
        form_class = ItemForm

    # class Input:
    #     input = ItemInputType()

# # Obsoleted by ItemFormUpdateMutation
# class ItemUpdateMutation(MutationPayLoad, graphene.Mutation):
#     class Arguments:
#         id = graphene.Int(required=True)
#         input = ItemInputType()

#     item_instance = graphene.Field(ItemType)

#     @classmethod
#     def mutate(cls, parent, info, id, input):
#         errors = []
#         try:
#             item = Item.objects.get(pk=id)
#         except Item.DoesNotExist:
#             errors.append('Item not exist')

#         try:
#             Category.objects.get(pk=input.category_id)
#         except Category.DoesNotExist:
#             errors.append('Category not exist')

#         if not errors:
#             item.__dict__.update(**input)
#             item.save()

#         return ItemUpdateMutation(errors=errors, item_instance=item)


class ItemFormUpdateMutation(DjangoModelFormMutation, MutationPayLoad):
    class Meta:
        form_class = ItemForm

    # class Input:
    #     input = ItemInputType()


class ItemDeleteMutation(MutationPayLoad, graphene.Mutation):
    # Delete an array of Item
    class Arguments:
        id_list = graphene.List(graphene.Int, required=True)

    id_deleted = graphene.List(graphene.Int)
    id_not_exist = graphene.List(graphene.Int)

    @classmethod
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

    # Category
    all_categories = graphene.List(CategoryType)
    categories_contains_name = graphene.List(
        CategoryType, name=graphene.String(required=True))
    category_by_id = graphene.Field(
        CategoryType, id=graphene.Int(required=True))

    def resolve_all_items(parent, info):
        return Item.objects.all().order_by('-id')

    def resolve_item_by_id(parent, info, id):

        try:
            item = Item.objects.get(pk=id)
        except Item.DoesNotExist:
            item = {
                "name": None,
                "category": {
                    "id": None,
                    "name": None
                },
                "sku": None,
                "upc": None,
                "price": None,
                "pack_qty": None
            }
        return item

    def resolve_all_categories(parent, info):
        return Category.objects.all().order_by('-datetime_updated')

    def resolve_categories_contains_name(parent, info, name):
        try:
            if name == '':
                return Category.objects.all()
            else:
                return Category.objects.filter(name__contains=name)
        except Category.DoesNotExist:
            return None

    def resolve_category_by_id(parent, info, id):
        try:
            return Category.objects.get(pk=id)
        except Category.DoesNotExist:
            return None


class Mutation(graphene.ObjectType):
    # category
    # create_category = CategoryCreateMutation.Field()
    category_create_by_form = CategoryFormCreateMutation.Field()
    # update_category = CategoryUpdateMutation.Field()
    category_update_by_form = CategoryFormUpdateMutation.Field()
    delete_category = CategoryDeleteMutation.Field()

    # item
    # create_item = ItemCreateMutation.Field()
    item_create_by_form = ItemFormCreateMutation.Field()
    # update_item = ItemUpdateMutation.Field()
    item_update_by_form = ItemFormUpdateMutation.Field()
    delete_item = ItemDeleteMutation.Field()


'''
#Trying to make a superclass for Mutation but seems impossible
class MutateCreate(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        #model_name = graphene.String(required=True)

    def __init__(self, Type, model_name):
        # super().__init__(*args, **kwargs)
        self.obj = graphene.Field(Type)
        self.model_name = model_name

    ok = graphene.Boolean()
    obj1 = graphene.Field(ItemType)
    #model_name = Item

    # @classmethod
    def mutate(root, info, self, name):
        obj_ = self.model_name(name=name)
        ok = True
        obj_.save()
        return CategoryMutateCreate(obj1=obj_, ok=ok)
'''
