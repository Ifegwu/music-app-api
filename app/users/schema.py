from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    me = graphene.Field(UserType)

    def resolve_user(self, info, id):
        return get_user_model().objects.get(id=id)

    def resolve_me(self, info):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Not Logged in!')

        return user


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email
        )

        user.set_password(password)
        user.save()
        return CreateUser(user=user)


class UserInput(graphene.InputObjectType):
    id = graphene.Int(required=False)
    username = graphene.String(required=False)
    password = graphene.String(required=False)
    email = graphene.String(required=False)


class UpdateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        user_data = UserInput(required=True)

    # @login_required
    def mutate(self, info, user_data=None):
        user = info.context.user

        for k, v in user_data.items():
            if (k == 'password') and (v is not None):
                user.set_password(user_data.password)
            else:
                setattr(user, k, v)

        try:
            user.full_clean()
            user.save()
            return UpdateUser(user=user)

        except Exception as e:
            return UpdateUser(user=user, errors=e)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
