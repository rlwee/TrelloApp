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
                             UpdateListView,
                             UpdateCardView,
                             CreateCardView,
                             BoardEdit,
                             BoardViewTrelloBase
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
     
    path('board/<int:board_id>/list/<int:list_id>/update/',UpdateListView.as_view(), name='list_update'),
    
    path('board/<int:board_id>/list/<int:list_id>/card/<int:card_id>/update/',UpdateCardView.as_view(), name='card_update'),

    path('board/<int:board_id>/list/<int:list_id>/card/added/',CreateCardView.as_view(), name='create_card'),
    path('board/edit/<int:board_id>/edited/',BoardEdit.as_view(), name='edit_board'),

]