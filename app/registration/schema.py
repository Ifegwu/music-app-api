import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import authenticate
from graphql_jwt.utils import jwt_encode, jwt_payload
from graphql import GraphQLError
from registration.models import User
from registration.send_email import send_confirmation


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    me = graphene.Field(UserType)

    def resolve_user(self, info, id):
        # return get_user_model().objects.get(id=id)
        return User.objects.get(id=id)

    def resolve_me(self, info):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Not Logged in!')

        return user


class CreateUser(graphene.Mutation):
    message = graphene.String()
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = User.objects.create_user(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        send_confirmation(
            mail=user.email,
            username=user.username
        )
        return CreateUser(
                user=user,
                message="Successfully created user, {}".format(user.username))


class LoginUser(graphene.Mutation):
    user = graphene.Field(UserType)
    message = graphene.String()
    token = graphene.String()
    verification_prompt = graphene.String()

    class Arguments:
        email = graphene.String()
        password = graphene.String()

    def mutate(self, info, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        user = authenticate(username=email, password=password)
        error_message = 'Invalid login credentials'
        success_message = "You logged in successfully."
        verification_error = 'Your email is not verified'
        if user:
            if user.is_verified:
                payload = jwt_payload(user)
                token = jwt_encode(payload)
                return LoginUser(token=token, message=success_message)

            return LoginUser(message=verification_error)
        return LoginUser(message=error_message)


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
    login_user = LoginUser.Field()
    update_user = UpdateUser.Field()
