from . import item, category


class Query(item.Query, category.Query):
    pass


class Mutation(item.Mutation, category.Mutation):
    pass
