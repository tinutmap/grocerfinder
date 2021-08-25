from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from graphene_django.views import GraphQLView
from .models import Item
# Create your views here.


def index(request):
    submitted = False
    if 'submitted' in request.GET:
        submitted = True
        item = get_object_or_404(Item)

    return render(request, 'aldi/index.html')


class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    pass
