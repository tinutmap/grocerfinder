'''
Base Classes and Functions for graphene schemas
'''
import graphene
from django.db import IntegrityError, connection
import decimal
import datetime
from django.db.models import Min
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql_jwt.decorators import login_required


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


class DjangoModelFormMutationLoginRequired(DjangoModelFormMutation):
    class Meta:
        abstract = True

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        return super().mutate_and_get_payload(
            root=root, info=info, **input)
