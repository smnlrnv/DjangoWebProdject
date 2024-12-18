"""
Definition of forms.
"""

from importlib.metadata import requires
from random import choices
from typing_extensions import Required
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.db import models
from .models import Comment
from .models import BlogArticle




class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class AnketaForm(forms.Form):
    name = forms.CharField(label='Ваше имя', min_length=2, max_length=100)
    city = forms.CharField(label='Ваш город', min_length=2, max_length=100)
    job = forms.CharField(label='Ваш род занятий', min_length=2, max_length=100)
    gender = forms.ChoiceField(label='Ваш пол',
                           choices=[('1', 'мужской'), ('2', 'женский')],
                           widget=forms.RadioSelect,
                           initial='1')

    often = forms.ChoiceField(label='Как часто вы играете на своих игровых устройствах?',
                          choices=(('1', 'каждый день'),
                                   ('2', 'раз в три дня'),
                                   ('3', 'раз в неделю'),
                                   ('4', 'несколько раз в месяц')),
                          initial='1')


    genres = forms.ChoiceField(label='Какие жанры игр вам нравятся больше всего?', 
                             choices=(('1','стратегии'),
                                      ('2','шутеры'),
                                      ('3','мобо игры'),
                                      ('4,','гонки')),
                             initial='1')
    sound = forms.BooleanField(label='Считаете ли вы, что качество звука важно для игрового процесса?',
                              required=False)
    notice = forms.BooleanField(label='Получать новости по email?',
                              required=False)
    email = forms.EmailField(label='ваш email', max_length=254)

    massage = forms.CharField(label='Кортко о себе', 
                             widget=forms.Textarea(attrs={'rows':12,'cols':18}))

class CommentForm(forms.ModelForm):

         class Meta:

           model = Comment # используемая модель

           fields = ('text',) # требуется заполнить только поле text

           labels = {'text': "Комментарий"} # метка к полю формы text

class BlogArticleForm (forms.ModelForm):
    class Meta:
        model= BlogArticle
        fields=('title','summary','content','image')
        labels={'title':"Заголовок",'summary':"Краткое содержание",'content':"Полное содержание",'image':"Картинка"}