'''
Category schema
'''
from graphene_django import DjangoObjectType
import graphene
from aldi.models import Category
from aldi.forms import CategoryForm
from .base import MutationPayLoad, delete_entity, resolve_model_fetch_more, DjangoModelFormMutationLoginRequired
from graphql_jwt.decorators import login_required


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


class CategoryFormCreateMutation(DjangoModelFormMutationLoginRequired, MutationPayLoad):
    class Meta:
        form_class = CategoryForm


class CategoryFormUpdateMutation(DjangoModelFormMutationLoginRequired, MutationPayLoad):
    class Meta:
        form_class = CategoryForm


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
# Query and Mutation


class Query(graphene.ObjectType):
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
    category_create_by_form = CategoryFormCreateMutation.Field()
    category_update_by_form = CategoryFormUpdateMutation.Field()
    delete_category = CategoryDeleteMutation.Field()
