import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import authenticate
from graphql_jwt.utils import jwt_encode, jwt_payload
from graphql_jwt.decorators import login_required
import graphql_jwt
from graphql import GraphQLError
from app.registration.models import User, Subscriptions
from app.registration.send_email import send_confirmation, contact_form
from django.conf import settings
import stripe  


class UserType(DjangoObjectType):
    class Meta:
        model = User

class SubscriptionsType(DjangoObjectType):
    class Meta:
        model = Subscriptions
        

class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    me = graphene.Field(UserType)

    def resolve_subs(self, info):
        return Subscriptions.objects.all()

    def resolve_user(self, info, id):
        # return get_user_model().objects.get(id=id)
        return User.objects.get(id=id)

    # @login_required
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

    def mutate(self, info, **kwargs):
        user = User.objects.create_user(
            email=kwargs.get('email'),
            username=kwargs.get('username')
        )
        user.set_password(kwargs.get('password'))
        user.save()
        print('User Saved!')
        send_confirmation(
            email=user.email,
            username=user.username
        )
        print('Confirmation sent!')
        return CreateUser(
                user=user,
                message="Successfully created user, {}".format(user.username))


class LoginUser(graphene.Mutation):
    user = graphene.Field(UserType)
    message = graphene.String()
    token = graphene.String()
    refresh_token =  graphene.String()
    verification_prompt = graphene.String()

    class Arguments:
        # email = graphene.String()
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        user = authenticate(username=username, password=password)
        error_message = 'Invalid login credentials'
        print(error_message)
        success_message = "You logged in successfully."
        print(success_message)
        verification_error = 'Your email is not verified'
        print(verification_error)
        if user:
            if user.is_verified:
                payload = jwt_payload(user)
                token = jwt_encode(payload)
                refresh_token = graphql_jwt.Refresh.Field()
                print(refresh_token)
                return LoginUser(
                    token=token, 
                    message=success_message,
                    refresh_token=refresh_token
                )

            return LoginUser(message=verification_error)
            print(LoginUser)
        return LoginUser(message=error_message)
        print(LoginUser)


class UserInput(graphene.InputObjectType):
    id = graphene.Int(required=False)
    username = graphene.String(required=False)
    password = graphene.String(required=False)
    email = graphene.String(required=False)


class UpdateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    # message = graphene.String()

    class Arguments:
        user_data = UserInput(required=True)
        
    # @login_required
    def mutate(self, info, user_data=None):
        user = info.context.user
        # success_message = 'Updated succesfully'

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

class PasswordRecovery(graphene.Mutation):
    message = graphene.String()
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        username = graphene.String(required=True)
        # password = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        # email=kwargs.get('email')
        # username=kwargs.get('username')
        # user = User(email=email, username=username)

        user = User(
            email=kwargs.get('email'),
            username=kwargs.get('username')
        )
        
        # user.set_password(kwargs.get('password'))
        # user.save()
        # print('User Saved!')
        send_reset(
            email=user.email,
            username=user.username
        )
        print('Reset sent!')
        return PasswordRecovery(
                user=user,
                message="Email successfully sent to, {}".format(user.username))


class CreateSubscription(graphene.Mutation):
    subscriptions = graphene.Field(SubscriptionsType)

    class Arguments:
        fee = graphene.String(required=False)
        email=graphene.String(required=False)
        music = graphene.String(required=False)
        stripe_id  = graphene.String(required=False)
        subscriber = graphene. String(required=False)
        payment_method_id = graphene.String(required=False)

    def mutate(self, info, **kwargs):
        user = info.context.user
        fee = kwargs.get('fee')
        email = kwargs.get('email')
        music = kwargs.get('music')
        stripe_id  = kwargs.get('stripe_id ')
        subscriber = kwargs.get('subscriber')
        payment_method_id = kwargs.get('payment_method_id')
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        if user.is_anonymous:
            raise GraphQLError('You need to login to add a subscription!')

        extra_msg = '' # add new variable to response message

        # checking if customer with provided email already exists
        customer_data = stripe.Customer.list(email=email).data 

        # if the array is empty it means the email has not been used yet  
        if len(customer_data) == 0:
            # creating customer
            customer = stripe.Customer.create(
                email=email,
                description=music,
                payment_method=payment_method_id,
                invoice_settings={
                    'default_payment_method': payment_method_id
                }
            )
        else:
            customer = customer_data[0]
            extra_msg = "Customer already existed."

        # add these lines
        customer_intent = stripe.PaymentIntent.create(
            customer=customer, 
            payment_method=payment_method_id,  
            currency='ngn', # you can provide any currency you want
            amount=500000,  # it equals 5000.00 NGN
            confirm=True
        ) 

        customer_intent
        customer_intent.amount

        stripe.Subscription.create(
            customer=customer,
            items=[
                {'price': 'price_1I6EAkJF4Y1CLG7ZZPtxzRfK'}, #here paste your price id
            ],
        ) 
        
        try:
            subscriptions = Subscriptions(
                email=email,
                music=music,
                stripe_id=customer.id,
                fee=customer_intent.amount,
                subscriber=user,
            )
            subscriptions.save()
            print(subscriptions)
        except User.DoesNotExist:
            return HttpResponse({'Error': "Internal server error"}, status="500")

        return CreateSubscription(subscriptions=subscriptions)

class CancelSubscription(graphene.Mutation):
    subscriptions = graphene.Field(SubscriptionsType)

    class Arguments:
        email  = graphene.String(required=False)
        stripe_id  = graphene.String(required=False)

    def mutate(self, info, **kwargs):
        user = info.context.user
        email = kwargs.get('email')
        stripe_id  = kwargs.get('stripe_id ')

        stripe.api_key = settings.STRIPE_SECRET_KEY

        subscriptions = Subscriptions.objects.get(email=email)
        print(subscriptions.stripe_id)

        
        if user.is_anonymous:
            raise GraphQLError('You need to login to delete a subscription!')
        else: 
            customer = stripe.Customer.retrieve(id=subscriptions.stripe_id)
 
            print(customer.subscriptions.data[0].id)
            sub_id = customer.subscriptions.data[0].id
            stripe.Subscription.modify(
                sub_id,
                cancel_at_period_end=True,
            )

        return CancelSubscription(subscriptions=subscriptions)

class ContactForm(graphene.Mutation):
    message = graphene.String()
    name = graphene.String()
    email = graphene.String()
    body = graphene.String()

    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        body = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        email = kwargs.get('email')
        name = kwargs.get('name')
        body = kwargs.get('body')
        
        contact_form(
            email=email,
            name=name,
            body=body
        )
        print('Confirmation sent!')
        return ContactForm(
            name=name, 
            email=email, 
            body=body, 
            message="Message sent")

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    login_user = LoginUser.Field()
    update_user = UpdateUser.Field()
    password_recovery = PasswordRecovery.Field()
    create_subscription = CreateSubscription.Field()
    cancel_subscription = CancelSubscription.Field()
    contact_form = ContactForm.Field()

