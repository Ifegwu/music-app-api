import graphene
import tracks.schema
# import users.schema
from app.registration.schema import Mutation as AuthMutation
from app.registration.schema import Query as UserQuery
import graphql_jwt


class Query(
    UserQuery,
    tracks.schema.Query,
    graphene.ObjectType
):
    pass


class Mutation(
    # users.schema.Mutation,
    AuthMutation,
    tracks.schema.Mutation,
    graphene.ObjectType
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
