import json


from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic.base import TemplateView, View
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse

from trelloapp.models import Board,TrelloList,Card
from .forms import PostForm,TrelloListForm,TrelloCardForm

# Create your views here.


class Dash(TemplateView):

    template_name = 'trelloapp/dashboard.html'

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return render(request, self.template_name, {})
        else:
            return redirect('login')


class BoardCreateView(TemplateView):

    template_name = 'trelloapp/createboard.html'
    form = PostForm

    def get(self, request, **kwargs):

        form = self.form()
       # boards = Board.objects.filter(owner=request.user)
        return render(request, self.template_name, {'form':form,})

    def post(self, request, ** kwargs):
        form = self.form(request.POST)
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
        id = kwargs.get('board_id')
        board = get_object_or_404(Board, pk=id)
        boardlist = TrelloList.objects.filter(board=board)
        form = self.form()
        context = {
            'board':board,
            'boardlist':boardlist,
            'form':form
        }
        return render(request, self.template_name, context)
    
    def post(self,request,**kwargs):
      
        id = kwargs.get('board_id')
        board = get_object_or_404(Board, pk=id)
        form = self.form(request.POST)
        if form.is_valid():
            tlist = form.save(commit=False)
            tlist.board = board
            tlist.save()
            return redirect('board', board_id=board.id)
        return render(request, self.template_name, {'form':form,'board':board})



class ListOfBoards(TemplateView):   
    """ Board list page
    """
    template_name = 'trelloapp/boards.html'

    def get(self,request,**kwargs):
        boards = Board.objects.filter(owner=request.user)
        #owner = Board.objects.all()
        return render(request, self.template_name,{'boards':boards})


class BoardDetailView(TemplateView):
    """To Edit or Deleting a board
    """
    template_name = 'trelloapp/boarddetail.html'
    
    def get(self,request, **kwargs):
        id = kwargs.get('pk')
        boards = get_object_or_404(Board, pk=id)
        return render(request,self.template_name,{'boards':boards})

class EditBoard(TemplateView):

    template_name = 'trelloapp/boardedit.html'
    form = PostForm

    def get(self,request, **kwargs):
        id = kwargs.get('board_id')
        boards = get_object_or_404(Board, pk=id)
        form = self.form(instance=boards)
        if not request.user.is_authenticated:
            return redirect('listofboards')
        return render(request,self.template_name,{'form':form,'boards':boards})

    def post(self,request,**kwargs):
        id = kwargs.get('board_id')
        boards = get_object_or_404(Board, pk=id)
        form = self.form(request.POST, instance=boards)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()
            return redirect('detail', pk=board.pk)
        return render(request, self.template_name, {'form':form,'boards':boards})


class DeleteBoard(TemplateView):

    template_name = 'trelloapp/boards.html'

    def get(self,request,**kwargs):
        id = kwargs.get('board_id')
        boards = Board.objects.get(pk=id, owner=request.user)
        if request.user.is_authenticated:
            boards.delete()
            return redirect('listofboards')

class EditList(TemplateView):

    template_name = 'trelloapp/editlist.html'
    form = TrelloListForm

    def get(self,request, **kwargs):
        id = kwargs.get('pk')
        # board = Board.objects.get(pk=id)
        lists = TrelloList.objects.get(pk=id)
        form = self.form(instance=lists)
        return render(request, self.template_name, {'lists':lists,'form':form})

    def post(self,request, **kwargs):
        id = kwargs.get('pk')
        board_id = kwargs.get('board_id')
        boards = get_object_or_404(Board, pk=board_id)
        lists = TrelloList.objects.get(pk=id)
        form = self.form(request.POST, instance=lists)
        if form.is_valid():
            listss = form.save(commit=False)
            listss.board = boards
            listss.save()
            return redirect('board', pk=board_id)
        return render(request, self.template_name, {'form':form})


class MyAjaxView(TemplateView):
    """ Render boards template through ajax
    """

    template_name = 'trelloapp/ajax.html'


class ListView(TemplateView):
    """ Retrieve all List in a Board
    """
    template_name = 'trelloapp/lists.html'

    def get(self,request,**kwargs):
        id = kwargs.get('pk')
        board = get_object_or_404(Board, pk=id)
        lists = TrelloList.objects.filter(board=board)
        return render(request, self.template_name, {'board': board, 'lists':lists})

class CardCreateView(TemplateView):

    template_name = 'trelloapp/addcard.html'
    form = TrelloCardForm

    def get(self, request, **kwargs):
        #import pdb; pdb.set_trace()
        id = kwargs.get('list_id')
        lists = get_object_or_404(TrelloList, pk=id)
        card = Card.objects.filter(trello_list=lists)
        form = self.form()
        context = {
            'lists':lists,
            'card':card,
            'form':form,
        }
        return render(request, self.template_name, context)

    def post(self,request,**kwargs):
        board_id = kwargs.get('pk')
        list_id = kwargs.get('list_id')
        lists = get_object_or_404(TrelloList, pk=list_id)
        card = Card.objects.filter(trello_list=lists)
        form = self.form(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.trello_list = lists
            card.save()
            return redirect('cardviews', board_id=board_id, list_id=list_id)
        return render(request, self.template_name, {'form':form})


class CardList(TemplateView):

    template_name = 'trelloapp/cards.html'

    def get(self,request,**kwargs):
        board_id = kwargs.get('board_id')
        list_id = kwargs.get('list_id')
        board_list = get_object_or_404(TrelloList, pk=list_id)
        cards = Card.objects.filter(trello_list=board_list)
        context = {
            'cards':cards,
            'board_id': board_id,
            'list_id': list_id,
        }
        return render(request, self.template_name, context)
        
        #return JsonResponse(context)

class UpdateListView(View):

    def get(self, request, **kwargs):
        board_id = kwargs.get('board_id')
        list_id = kwargs.get('list_id')
        blist = get_object_or_404(TrelloList, id=list_id, board__id=board_id)
        blist.title =  request.GET.get('title')
        blist.save()
        return JsonResponse({'title': blist.title})

class UpdateCardView(View):

    def get(self, request, **kwargs):
        board_id = kwargs.get('board_id')
        list_id = kwargs.get('list_id')
        card_id = kwargs.get('card_id')
        bcard = get_object_or_404(Card, id=card_id, trello_list__id=list_id)
        bcard.title = request.GET.get('title')
        bcard.save()
        return JsonResponse({'title':bcard.title})