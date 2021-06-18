from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from .models import User


class UserList(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return JsonResponse({})


class UserDetail(View):

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return JsonResponse({})
