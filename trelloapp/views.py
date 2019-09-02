from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic.base import TemplateView
from trelloapp.models import Board,TrelloList,Card
from django.contrib.auth.models import User
from .forms import PostForm,PostList


# Create your views here.


class Dash(TemplateView):

    template_name = 'trelloapp/dashboard.html'

    def get(self, request, **kwargs):
        #board = Board.objects.all()
        return render(request, self.template_name, {})

    def post(self, request, **kwargs):
        return redirect('createboard')


class BoardButton(TemplateView):

    template_name = 'trelloapp/createboard.html'

    def get(self, request, **kwargs):
        form = PostForm()
        
        boards = Board.objects.all()
        return render(request, self.template_name, {'form':form, 'boards':boards})

    def post(self, request, ** kwargs):
        form = PostForm(request.POST)

        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()
            return redirect('dashboard')
        return render(request, self.template_name,{'form':form})


class CreateList(TemplateView):

    template_name = 'trelloapp/createlist.html'

    def get(self,request, **kwargs):
        board = Board.objects.all()
        trellolist = PostList()

        return render(request, self.template_name,{'trellolist':trellolist})

    def post(self,request, **kwargs):
        board = Board.objects.all()
        trellolist = PostList(request.POST)
        if trellolist.is_valid():
            tlist = trellolist.save(commit=False)
            tlist.board.owner = request.user
            tlist.save()
            return redirect('dashboard')
        return render(request, self.template_name,{'trellolist':trellolist})

class BoardView(TemplateView):

    template_name = 'trelloapp/currentboard.html'

    def get(self,request,**kwargs):
        id = kwargs.get('pk')
        board = get_object_or_404(Board, pk=id)
        boardlist = TrelloList.objects.filter(board=board)
        return render(request, self.template_name, {'board':board,'boardlist':boardlist})




