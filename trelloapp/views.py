import json
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from trelloapp.models import Board,TrelloList,Card,BoardMembers,BoardInvite
from .forms import PostForm,TrelloListForm,TrelloCardForm,MemberInviteForm
from django.core.mail import send_mail
from django.conf import settings
from django.template import loader
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

# Create your views here.


class Dash(TemplateView):

    template_name = 'trelloapp/dashboard.html'

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return render(request, self.template_name, {})
        else:
            return redirect('login')

class Base(TemplateView):

    template_name = 'trelloapp/trellobase.html'
    #import pdb; pdb.set_trace()
    def get(self,request,**kwargs):
        boards = Board.objects.filter(owner=request.user)
        #owner = Board.objects.all()
        return render(request, self.template_name,{'boards':boards})


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
        return render(request, self.template_name,{'form':form,'board':board})


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




class ListCreate(View):

    form = TrelloListForm

    def post(self, request, **kwargs):
        board_id = kwargs.get('pk')
        board = get_object_or_404(Board, pk=board_id)
        form = self.form(request.POST)

        if form.is_valid():
            lists = form.save(commit=False)
            lists.board = board
            lists.save()
            return JsonResponse({'title':lists.title})
        return JsonResponse({}, status=400)



class BoardViewTrelloBase(TemplateView):

    template_name = 'trelloapp/trellobase.html'
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
    Dash



class ListOfBoards(TemplateView):   
    """ Board list page
    """
    template_name = 'trelloapp/boards.html'

    def get(self,request,**kwargs):
        boards = Board.objects.filter(owner=request.user)
        #import pdb; pdb.set_trace()
        invitedBoards = BoardInvite.objects.filter(email=request.user.email)
        return render(request, self.template_name,{'boards':boards,'board':invitedBoards})


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

    def get(self,request,**kwargs):
        id = kwargs.get('board_id')
        boards = Board.objects.get(pk=id, owner=request.user)
        if request.user.is_authenticated:
            boards.delete()
            return redirect('listofboards')

class DeleteBoardNew(TemplateView):
    pass



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
        # import pdb; pdb.set_trace()
        id = kwargs.get('list_id')
        board_id = kwargs.get('pk')
        board = get_object_or_404(Board, pk = board_id)
        lists = get_object_or_404(TrelloList, pk=id)
        card = Card.objects.filter(trello_list=lists)
        form = self.form()
        context = {
            'board':board,
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
            'board_list':board_list,
        }
        return render(request, self.template_name, context)
        
        #return JsonResponse(context)

class UpdateListView(View):

    def post(self, request, **kwargs):
        board_id = kwargs.get('board_id')
        list_id = kwargs.get('list_id')
        blist = get_object_or_404(TrelloList, id=list_id, board__id=board_id)
        blist.title =  request.POST.get('title')
        blist.save()
        return JsonResponse({'title': blist.title})

class UpdateCardView(View):

    def post(self, request, **kwargs):
        board_id = kwargs.get('board_id')
        list_id = kwargs.get('list_id')
        card_id = kwargs.get('card_id')
        bcard = get_object_or_404(Card, id=card_id, trello_list__id=list_id)
        bcard.title = request.POST.get('title')
        bcard.save()
        return JsonResponse({'title': bcard.title})

class CreateCardView(View):

    form = TrelloCardForm

    def post(self, request, **kwargs):
        board_id = kwargs.get('pk')
        list_id = kwargs.get('list_id')
        lists = get_object_or_404(TrelloList, pk=list_id)
        card = Card.objects.filter(trello_list=lists)
        form = self.form(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.trello_list = lists
            card.save()
            return JsonResponse({'title':card.title, 'id':card.id,'list_id':lists.id, 'board_id':board_id})

        return JsonResponse({}, status=400)

class BoardEdit(View):

    form = PostForm

    def post(self,request,**kwargs):
        id = kwargs.get('board_id')
        boards = get_object_or_404(Board, pk=id)
        form = self.form(request.POST, instance=boards)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()
            return JsonResponse({'title':board.title,'board_id':boards.id})
        return JsonResponse({}, status=400)

class BoardCreate(View):

    form = PostForm

    def post(self, request, **kwargs):

        form = self.form(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()
            return JsonResponse({'title':board.title, 'board_id':board.id})
        return JsonResponse({}, status=400)




from django.core import serializers

class DragCard(View):

    def post(self, request, **kwargs):
        card = get_object_or_404(Card, id=kwargs.get('card_id'), trello_list__id= kwargs.get('list_id'))
        card.trello_list = get_object_or_404(TrelloList, id=request.POST.get('list_id'))
        card.save()
        return JsonResponse({'card_id': card.id, 'list_id': card.trello_list.id}, safe=False)

class CardView(TemplateView):

    template_name = 'trelloapp/card.html'

    def get(self, request, **kwargs):
        board_id = kwargs.get('board_id')
        list_id = kwargs.get('list_id')
        blist = TrelloList.objects.get(pk=list_id)
        card_id = kwargs.get('card_id')
        card = Card.objects.get(pk=card_id)
        context = {
            'board_id':board_id,
            'card_id':card_id,
            'card':card,
            'list_id':list_id,
            'blist':blist,
        }
        return render(request, self.template_name, context)

class CardTitleUpdate(View):

    def post(self, request, **kwargs):
        board_id = kwargs.get('board_id')
        list_id = kwargs.get('list_id')
        card_id = kwargs.get('card_id')
        bcard = get_object_or_404(Card, id=card_id, trello_list__id=list_id)
        bcard.title = request.POST.get('title')
        bcard.save()
        return JsonResponse({'title': bcard.title,'card_id':bcard.id})

class CardLabelUpdate(View):

    def post(self, request, **kwargs):
        board_id = kwargs.get('board_id')
        list_id = kwargs.get('list_id')
        card_id = kwargs.get('card_id')
        bcard = get_object_or_404(Card, id=card_id, trello_list__id=list_id)
        bcard.labels = request.POST.get('labels')
        bcard.save()
        return JsonResponse({'labels':bcard.labels})

class InviteMember(TemplateView):

    template_name = 'trelloapp/invite.html'
    form = MemberInviteForm

    def get(self, request, **kwargs):
        board_id = kwargs.get('board_id')
        board = get_object_or_404(Board, pk=board_id)
        form = self.form()
        form.fields['board'].initial=board
        return render(request, self.template_name, {'form':form,'board':board,})

class Email(View):

    form = MemberInviteForm

    def post(self,request,**kwargs):
        board_id = kwargs.get('board_id')
        board = get_object_or_404(Board, pk=board_id)
        form = self.form(request.POST)

        domain = request.META['HTTP_HOST']

        if form.is_valid():
            invite = form.save(commit=False)
            invite.board = board
            invite.save()
            receiver = request.POST.get('email')
            subject = 'Hi hello hey ! You have a Trello board invitation'
            message = 'You have received and invitation to a board!'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [receiver,]
            
            html_message = loader.render_to_string(
                            'trelloapp/invitation.html',
                            {
                             'uid':invite.member,
                             'domain':domain,
                             'board_id':board.id}
            )
            send_mail(subject, message, email_from, recipient_list,fail_silently=True, html_message=html_message)
            return JsonResponse({'receiver':receiver}) 
        return JsonResponse({}, status=400)


class LoginInvite(TemplateView):

    template_name = 'accounts/logininvitaion.html'

    def get(self,request,**kwargs):
        form = AuthenticationForm()

        invite = get_object_or_404(BoardInvite, member=kwargs.get('uid'))
        user_email = User.objects.get(email=invite.email) 
        newMember = BoardMembers.objects.create(board=invite.board,member=user_email) 
        
        return render(request, self.template_name, {'form':form})

    def post(self,request,**kwargs):
        
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                messages.info(request, f"you are logged in as{username}")
                return redirect('dashboard')
            else:
                messages.error(request, f"Invalid username or password")
        return render(request, self.template_name, {'form':form})
        
        

