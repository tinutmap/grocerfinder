from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required, superuser_required
import graphql_jwt


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    @superuser_required
    def mutate(parent, info, username, password, email):
        user = get_user_model()(username=username, email=email)
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user_identity = graphene.Field(UserType)

    @superuser_required
    def resolve_all_users(parent, info):
        return get_user_model().objects.all()

    def resolve_user_identity(parent, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not Logged In')
        return user


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    delete_token_cookie = graphql_jwt.DeleteJSONWebTokenCookie.Field()
    # Long running refresh tokens
    delete_refresh_token_cookie = graphql_jwt.DeleteRefreshTokenCookie.Field()
