import graphene
from graphene_django.types import DjangoObjectType
from django.core.exceptions import ValidationError
from .models import User
from .forms import UserForm


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, username=graphene.String())

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self, info, **kwargs):
        username = kwargs.get("username")
        return User.objects.get_or_none(username=username)


class UserCreateMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        password = graphene.String(required=True)
        avatar = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, username, first_name, last_name, password, avatar):
        data = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "avatar": avatar,
        }

        form = UserForm(data)

        if not form.is_valid():
            raise ValidationError(form.errors)

        user = User.objects.create(
            username=form.cleaned_data["username"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            password=form.cleaned_data["password"],
            avatar=form.cleaned_data["avatar"],
        )
        return UserCreateMutation(user=user)


class UserUpdateMutation(graphene.Mutation):
    class Arguments:
        username = graphene.ID(required=True)
        first_name = graphene.String()
        last_name = graphene.String()
        password = graphene.String()
        avatar = graphene.String()

    user = graphene.Field(UserType)

    def mutate(self, info, username, first_name, last_name, password, avatar):
        data = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "avatar": avatar,
        }

        form = UserForm(data)

        if not form.is_valid():
            raise ValidationError(form.errors)

        user = User.objects.get(pk=username)
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.avatar = form.cleaned_data['avatar']
        user.password = form.cleaned_data['password']
        user.save()
        return UserUpdateMutation(user=user)


class UserDeleteMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, username):
        user = User.objects.get_or_none(username=username)
        if user:
            user.delete()
        return UserDeleteMutation(user=user)


class Mutation:
    create_user = UserCreateMutation.Field()
    update_user = UserUpdateMutation.Field()
    delete_user = UserDeleteMutation.Field()


schema = graphene.Schema(query=Query)
