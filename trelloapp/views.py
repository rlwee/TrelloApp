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
        id = kwargs.get('pk')
        board = get_object_or_404(Board, pk=id)
        boardlist = TrelloList.objects.filter(board=board)
        context = {
            'board':board,
            'boardlist':boardlist,
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
        #boards = Board.objects.all()
        return render(request, self.template_name,{'owner':owner})


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
        id = kwargs.get('pk')
        boards = get_object_or_404(Board, pk=id)
        form = self.form(instance=boards)
        if not request.user.is_authenticated:
            return redirect('listofboards')
        return render(request,self.template_name,{'form':form,'boards':boards})

    def post(self,request,**kwargs):
        id = kwargs.get('pk')
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
        id = kwargs.get('pk')
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
        boards = get_object_or_404(Board, pk=id)
        lists = TrelloList.objects.get(pk=id)
        form = self.form(request.POST, instance=lists)
        if form.is_valid():
            listss = form.save(commit=False)
            listss.board = lists
            listss.save()
            return redirect('board', pk=id)
        return render(request, self.template_name, {'lists':lists,'form':form})