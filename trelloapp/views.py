from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic.base import TemplateView
from trelloapp.models import Board,TrelloList,Card
from django.contrib.auth.models import User
from .forms import PostForm,TrelloListForm


# Create your views here.


class Dash(TemplateView):

    template_name = 'trelloapp/dashboard.html'



class BoardListView(TemplateView):

    template_name = 'trelloapp/createboard.html'

    def get(self, request, **kwargs):

        form = PostForm()
        boards = Board.objects.filter(owner=request.user)
        return render(request, self.template_name, {'form':form, 'boards':boards})

    def post(self, request, ** kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()
            return redirect('listofboards')
        return render(request, self.template_name,{'form':form})


class BoardView(TemplateView):

    template_name = 'trelloapp/currentboard.html'
    form = TrelloListForm

    def get(self, request, **kwargs):
        id = kwargs.get('pk')
        board = get_object_or_404(Board, pk=id)
        boardlist = TrelloList.objects.filter(board=board)
        boardcard = Card.objects.filter(trello_list=board)
        context = {
            'board':board,
            'boardlist':boardlist,
            'boardcard':boardcard,
            'form': self.form()
        }
        return render(request, self.template_name, context)
    
    def post(self,request,**kwargs):
        
        id = kwargs.get('pk')
        board = get_object_or_404(Board, pk=id)
        form = self.form(request.POST)
        if form.is_valid():
            tlist = form.save(commit=False)
            tlist.board = board
            tlist.save()
            return redirect('board', pk=id)
        return render(request, self.template_name, {'form': form})



class ListOfBoards(TemplateView):
    """ Board list page
    """
    template_name = 'trelloapp/boards.html'

    def get(self,request,**kwargs):
        owner = Board.objects.filter(owner=request.user)
        boards = Board.objects.all()
        return render(request, self.template_name,{'boards':boards,'owner':owner})


class CreateCard(TemplateView):
    pass


