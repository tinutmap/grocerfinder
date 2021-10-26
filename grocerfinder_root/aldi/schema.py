from django.db.models import Min
import graphene
import decimal
import datetime
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


def resolve_model_fetch_more(model, cursor, cursor_id, page_size, sort_by_field):
    # Option 1: manually coded Paginator
    try:
        # cast cursor to correct format for comparison. Default is string
        sort_by_field_type = model._meta.get_field(
            sort_by_field).description
        if sort_by_field_type == 'Integer':
            cursor = int(cursor)
        elif sort_by_field_type == 'Decimal number':
            cursor = decimal.Decimal(cursor)
        elif sort_by_field_type == 'Date (with time)':
            try:
                cursor = datetime.datetime(cursor)
             # if datetime conversion fails. e.g. cursor = '0' then get the entry with min datetime_updated
            except:
                cursor = model.objects.all().aggregate(Min(sort_by_field))
                cursor = cursor[sort_by_field+'__min']

        # use 'id' in addition to sort_by_field. It is the aggregate
        # criterion in case cursor is not unique to prevent duplicate
        model_all = model.objects.all().order_by(sort_by_field, 'id')

        # convert QuerySet to list of dict with only interested field and 'id' field
        # for next cursor index finding
        # to-do: using list() may not be optimal for memory
        model_all_dict = list(model_all.values(sort_by_field, 'id'))
        try:
            next_cursor_index = model_all_dict.index({
                sort_by_field: cursor,
                "id": cursor_id
            }) + 1
        except ValueError:  # when index return no value due to deleted or no matching
            next_cursor_index = 0
            while (
                model_all_dict[next_cursor_index][sort_by_field] <= cursor
            ) and (
                model_all_dict[next_cursor_index]['id'] <= cursor_id
            ):
                next_cursor_index += 1
        return model_all[next_cursor_index:next_cursor_index+page_size:1]
    except:
        return None
    # Option 2: https://docs.djangoproject.com/en/3.2/ref/paginator/#django.core.paginator.Paginator

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

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        return super().mutate_and_get_payload(
            root=root, info=info, **input)


class CategoryFormUpdateMutation(DjangoModelFormMutation, MutationPayLoad):
    class Meta:
        form_class = CategoryForm

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        return super().mutate_and_get_payload(
            root=root, info=info, **input)


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
    @login_required
    def mutate(cls, parent, info, id_list):
        id_deleted, errors, id_not_exist = delete_entity(Category, id_list)
        return CategoryDeleteMutation(id_deleted=id_deleted,
                                      errors=errors,
                                      id_not_exist=id_not_exist)

###############################################################################
# Item schema


class ItemType(DjangoObjectType):

    class Meta:
        model = Item
        fields = ('name', 'sku', 'upc', 'image', 'category',
                  'price', 'uom', 'pack_qty', 'datetime_updated')

    # force id to be Int rather than String
    id = graphene.Int()
    # name = graphene.String()
    price = graphene.Decimal()

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

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        return super().mutate_and_get_payload(
            root=root, info=info, **input)

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

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        return super().mutate_and_get_payload(
            root=root, info=info, **input)


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
    item_fetch_more = graphene.List(
        ItemType,
        cursor=graphene.String(required=True),
        cursor_id=graphene.Int(required=True),
        page_size=graphene.Int(required=True),
        sort_by_field=graphene.String(required=True, default_value='id')
    )

    # Category
    all_categories = graphene.List(CategoryType)
    categories_contains_name = graphene.List(
        CategoryType, name=graphene.String(required=True))
    category_by_id = graphene.Field(
        CategoryType, id=graphene.Int(required=True))
    category_fetch_more = graphene.List(
        CategoryType,
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
        # # Option 1: manually coded Paginator
        # try:
        #     # cast cursor to correct format for comparison. Default is string
        #     sort_by_field_type = Item._meta.get_field(
        #         sort_by_field).description
        #     if sort_by_field_type == 'Integer':
        #         cursor = int(cursor)
        #     elif sort_by_field_type == 'Decimal number':
        #         cursor = decimal.Decimal(cursor)

        #     # use 'id' in addition to sort_by_field. It is the aggregate
        #     # criterion in case cursor is not unique to prevent duplicate
        #     item_all = Item.objects.all().order_by(sort_by_field, 'id')

        #     # convert QuerySet to list of dict with only interested field and 'id' field
        #     # for next cursor index finding
        #     # to-do: using list() may not be optimal for memory
        #     item_all_dict = list(item_all.values(sort_by_field, 'id'))
        #     try:
        #         next_cursor_index = item_all_dict.index({
        #             sort_by_field: cursor,
        #             "id": cursor_id
        #         }) + 1
        #     except ValueError:  # when index return no value due to deleted or no matching
        #         next_cursor_index = 0
        #         while (
        #             item_all_dict[next_cursor_index][sort_by_field] <= cursor
        #         ) and (
        #             item_all_dict[next_cursor_index]['id'] <= cursor_id
        #         ):
        #             next_cursor_index += 1
        #     return item_all[next_cursor_index:next_cursor_index+page_size:1]
        # except:
        #     return None
        # # Option 2: https://docs.djangoproject.com/en/3.2/ref/paginator/#django.core.paginator.Paginator
        return resolve_model_fetch_more(Item, cursor, cursor_id, page_size, sort_by_field)

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

    def resolve_category_fetch_more(parent, info, cursor, cursor_id, page_size, sort_by_field):
        return resolve_model_fetch_more(Category, cursor, cursor_id, page_size, sort_by_field)


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
# Trying to make a superclass for Mutation but seems impossible
class MutateCreate(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        # model_name = graphene.String(required=True)

    def __init__(self, Type, model_name):
        # super().__init__(*args, **kwargs)
        self.obj = graphene.Field(Type)
        self.model_name = model_name

    ok = graphene.Boolean()
    obj1 = graphene.Field(ItemType)
    # model_name = Item

    # @classmethod
    def mutate(root, info, self, name):
        obj_ = self.model_name(name=name)
        ok = True
        obj_.save()
        return CategoryMutateCreate(obj1=obj_, ok=ok)
'''
