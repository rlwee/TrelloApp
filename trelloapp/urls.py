from django.urls import path,include
from trelloapp.views import Dash

urlpatterns = [

    path('', Dash.as_view(), name='dashboard')

]