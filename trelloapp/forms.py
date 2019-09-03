from django import forms
from .models import Board,TrelloList,Card


class PostForm(forms.ModelForm):

    class Meta:
        model = Board
        fields = ('title',)

class TrelloListForm(forms.ModelForm):

    class Meta:
        model = TrelloList
        fields = ('title',)

