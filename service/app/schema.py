import graphene
from graphene_django.types import DjangoObjectType
from .models import User


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
        title = graphene.String(required=True)
        year = graphene.Int(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, title, year):
        user = User.objects.create(title=title, year=year)
        return UserCreateMutation(user=user)


class UserUpdateMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        year = graphene.Int(required=True)
        id = graphene.ID(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, id, title, year):
        user = User.objects.get(pk=id)
        if title is not None:
            user.title = title
        if year is not None:
            user.year = year
        user.save()
        return UserUpdateMutation(user=user)


class UserDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, id):
        user = User.objects.get(pk=id)
        user.delete()
        return UserDeleteMutation(user=None)


class Mutation:
    create_user = UserCreateMutation.Field()
    update_user = UserUpdateMutation.Field()
    delete_user = UserDeleteMutation.Field()


schema = graphene.Schema(query=Query)
