from django.urls import path,include
from trelloapp.views import (Dash,
                             BoardListView,
                             BoardView,
                             ListOfBoards,
                            )

urlpatterns = [

    path('', Dash.as_view(), name='dashboard'),
    path('board/create', BoardListView.as_view(), name='createboard'),
    path('board/<pk>/', BoardView.as_view(), name = 'board'),
    path('boards/',ListOfBoards.as_view(), name='listofboards')

]