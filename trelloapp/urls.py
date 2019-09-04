from django.urls import path,include
from trelloapp.views import (Dash,
                             BoardListView,
                             BoardView,
                             ListOfBoards,
                             BoardDetailView,
                             EditBoard,
                             DeleteBoard,
                             EditList
                            )

urlpatterns = [

    path('', Dash.as_view(), name='dashboard'),
    path('board/create', BoardListView.as_view(), name='createboard'),
    path('board/<pk>/', BoardView.as_view(), name = 'board'),
    path('boards/',ListOfBoards.as_view(), name='listofboards'),
    path('board/detail/<pk>',BoardDetailView.as_view(),name='detail'),
    path('board/edit/<pk>',EditBoard.as_view(), name='editboard'),
    path('board/delete/<pk>',DeleteBoard.as_view(),name='deleteboard' ),
    path('board/List/Edit/<pk>/', EditList.as_view(), name = 'editlist'),

]