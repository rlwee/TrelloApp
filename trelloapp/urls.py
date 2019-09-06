from django.urls import path,include
from trelloapp.views import (Dash,
                             BoardCreateView,
                             BoardView,
                             ListOfBoards,
                             BoardDetailView,
                             EditBoard,
                             DeleteBoard,
                             EditList,
                             MyAjaxView,
                             ListView,
                             CardCreateView,
                             CardList,
                            )

urlpatterns = [
    path('', Dash.as_view(), name='dashboard'),
    path('sample-ajax/', MyAjaxView.as_view(), name='dashboard'),
    path('board/create/', BoardCreateView.as_view(), name='createboard'),
    path('board/detail/<int:board_id>/', BoardView.as_view(), name='board'),
    path('boards/',ListOfBoards.as_view(), name='listofboards'),
    path('board/<int:pk>/',BoardDetailView.as_view(),name='detail'),
    path('board/edit/<int:board_id>/',EditBoard.as_view(), name='editboard'),
    path('board/delete/<int:board_id>/',DeleteBoard.as_view(),name='deleteboard' ),
    path('board/<board_id>/list/edit/<int:pk>/', EditList.as_view(), name = 'editlist'),
    path('board/<int:pk>/lists/',ListView.as_view(), name='listviews'),
    path('board/<int:pk>/list/<int:list_id>/create/card/', CardCreateView.as_view(), name='addcard'),
    path('board/<int:board_id>/list/<int:list_id>/cards/',CardList.as_view(), name='cardviews'),
]