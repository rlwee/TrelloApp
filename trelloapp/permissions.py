from trelloapp.models import Board, BoardInvite, BoardMembers
from django.contrib.auth import login,logout,authenticate
from django.http import Http404
from django.shortcuts import render,redirect,get_object_or_404
from trelloapp.models import Board


class BoardPermissionMixin():
    #import pdb; pdb.set_trace()
    
    def dispatch(self, *args, **kwargs):
        board_id = kwargs.get('board_id')
        boardOwner = get_object_or_404(Board, id=board_id)
        
        if self.request.user != boardOwner.owner:
            raise Http404
        
        return super().dispatch(*args, **kwargs)
        

        

