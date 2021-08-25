from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(parent, info, username, password, email):
        user = get_user_model()(username=username, email=email)
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)

    # # without using token argument
    # me = graphene.Field(UserType)
    # with using token argument
    me = graphene.Field(UserType, token=graphene.String())

    def resolve_all_users(parent, info):
        return get_user_model().objects.all()

    @login_required
    def resolve_me(parent, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not Logged In')
        return user


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
