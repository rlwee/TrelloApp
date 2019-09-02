from django.urls import path,include
from trelloapp.views import (Dash,
                             BoardButton,
                             CreateList,
                             BoardView,
                            )

urlpatterns = [

    path('', Dash.as_view(), name='dashboard'),
    path('createboard/', BoardButton.as_view(), name='createboard'),
    path('createlist/', CreateList.as_view(), name = 'createlist'),
    path('board/<pk>/', BoardView.as_view(), name = 'board')

]