from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView
from trelloapp.models import Board,TrelloList,Card


# Create your views here.


class Dash(TemplateView):

    template_name = 'trelloapp/dashboard.html'

    def get(self, request, **kwargs):
        return render(request, self.template_name, {})
