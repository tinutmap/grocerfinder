import graphene
import aldi.schema
import users.schema


class Query(users.schema.Query, aldi.schema.Query, graphene.ObjectType):
    pass


class Mutation(users.schema.Mutation, aldi.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation, auto_camelcase=False)
