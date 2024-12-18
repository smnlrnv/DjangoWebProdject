"""
Definition of views.
"""

from datetime import datetime

from django.shortcuts import render,redirect
from django.http import HttpRequest
from pickle import FALSE, NONE
from .forms import AnketaForm
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.contrib import messages
from .forms import BlogArticleForm
from django.db import models
from  .forms import CommentForm
from .models import  BlogArticle,Comment

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Домашняя страница',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Наша конткатная страница.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Страница описания нашего магазина.',
            'year':datetime.now().year,
        }
    )
def links(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Похожие ресурсы',
           
        }
    )
def anketa(request):
    assert isinstance(request, HttpRequest)
    
    gender = {'1':'мужской','2':'женский'}

    often = {'1':'каждый день','2':'раз в три дня','3':'раз в неделю','4,':'несколько раз в месяц'}
    genres = {'1':'стратегии','2':'шутеры','3':'мобо игры','4,':'гонки'}

    if request.method=='POST':
        form=AnketaForm(request.POST)
        if form.is_valid():
            return render(
                  request,
                  'app/anketa.html',
                   {
                   
                   'data': form,
                   'failed':False
                   }
                 )
        else:
             return render(
                  request,
                  'app/anketa.html',
                   {
                   
                   'data': form,
                   'failed':True
                   }
                 )
    else:
        form = AnketaForm()
    return render(
        request,
       'app/anketa.html',
      {
         'form': form,
         'failed':False
         }
       )



def registration(request):

    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = timezone.now()
            reg_f.last_login = timezone.now()
            reg_f.save()
            messages.success(request, 'Регистрация успешно завершена!')
            return redirect('home')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
          regform = UserCreationForm()
    return render(

    request,

    'app/registration.html',

    {

        'regform': regform,

        'year': timezone.now().year,

    }

)

def blog(request):

    assert isinstance(request, HttpRequest)

    posts =  BlogArticle.objects.all() # запрос на выбор всех статей блога из модели

    return render(

     request,

         'app/blog.html',

          {

            'title':'Блог',

            'posts': posts, # передача списка статей в шаблон веб-страницы

            'year':datetime.now().year,

          }

     )

def blogpost(request, parametr):

    assert isinstance(request, HttpRequest)
    comments = Comment.objects.filter(post=parametr)
    post_1 =  BlogArticle.objects.get(id=parametr) # запрос на выбор конкретной статьи по параметру

    

    if request.method == "POST": # после отправки данных формы на сервер методом POST

        form = CommentForm(request.POST)

        if form.is_valid():

            comment_f = form.save(commit=False)

            comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя

            comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату

            comment_f.post = BlogArticle.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий

            comment_f.save() # сохраняем изменения после добавления полей

            return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария

    else:

          form = CommentForm() # создание формы для ввода комментария
    return render(

       request,

       'app/blogpost.html',

           {
                 'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы

                'form': form, # передача формы добавления комментария в шаблон веб-страницы
                'post_1': post_1, # передача конкретной статьи в шаблон веб-страницы

                 'year':datetime.now().year,

           }

    )
                     
              
def newpost(request):
    assert isinstance(request, HttpRequest)
    
    if request.method == 'POST':
       blogform = BlogArticleForm(request.POST, request.FILES)
       if blogform.is_valid():
           blog_f = blogform.save(commit=False)
           blog_f.posted = datetime.now()
           blog_f.autor = request.user
           blog_f.save()
           return redirect('blog')
           
    else:            
           blogform = BlogArticleForm() 
            
    return render(
                  request,
                  'app/newpost.html',
                   {
                   'blogform': blogform,  
                   'title': 'Добавить статью блога',
                   'year': datetime.now().year,
                   }
                 )


def videopost(request):
    return render(request, 'app/videopost.html')  