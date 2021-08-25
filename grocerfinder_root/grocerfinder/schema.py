import graphene
import aldi.schema
import users.schema
import graphql_jwt


class Query(users.schema.Query, aldi.schema.Query, graphene.ObjectType):
    pass


class Mutation(users.schema.Mutation, aldi.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    delete_token_cookie = graphql_jwt.DeleteJSONWebTokenCookie.Field()
    # Long running refresh tokens
    delete_refresh_token_cookie = graphql_jwt.DeleteRefreshTokenCookie.Field()


schema = graphene.Schema(query=Query, mutation=Mutation, auto_camelcase=False)
