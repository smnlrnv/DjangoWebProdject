from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User

class BlogArticle(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    summary = models.TextField(max_length=500, verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Полное содержание")
    image = models.FileField(default = 'temp.jpg', verbose_name= 'Путь к картинке')
    pub_date = models.DateTimeField(default=timezone.now, verbose_name="Дата публикации")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья блога"
        verbose_name_plural = "Статьи блога" 

class BlogArticleAdmin(admin.ModelAdmin):
     list_display = ('title','author', 'pub_date')
     list_filter = ('pub_date','author')
     search_fields = ('title', 'content','author_username')
admin.site.register(BlogArticle, BlogArticleAdmin)
 


class Comment(models.Model):

    post = models.ForeignKey(BlogArticle, on_delete=models.CASCADE, related_name='comments')

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    text = models.TextField()

    date = models.DateTimeField(auto_now_add=True)



    def __str__(self):

        return f'Комментарий от {self.author} к {self.post}'