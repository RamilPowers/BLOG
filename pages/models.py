from django.db import models
from django.utils import timezone
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    STATUS_CHOICES = (
        ('yes', 'Опубликовано'),
        ('no', 'В разработке'),
    )
    title = models.CharField("Заголовок", max_length=250)
    slug = models.SlugField("Ссылка", max_length=250, unique=True)
    meta = models.CharField("Мета-описание", max_length=250)
    image = models.ImageField("Изображение", upload_to='posts')
    description = models.CharField("Описание", max_length=255)
    content = RichTextUploadingField("Контент")
    featured = models.BooleanField("В карусель", default=False)
    created = models.DateTimeField("Создано", auto_now_add=True)
    updated = models.DateTimeField("Обновлено", auto_now=True)
    status = models.CharField(
        "Статус",
        max_length=13,
        choices=STATUS_CHOICES,
        default='no'
    )

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ('-created',)

    def __str__(self):
        return self.title
   
    def get_absolute_url(self):
        """
        Создается ссылка на экземпляр класса Пост
        """
        return reverse('blog:post_detail', args=[self.slug])
    
    def get_next_post(self):
        """
        Переход к следующей статье
        """
        next_post = Post.objects.filter(created__gt=self.created,
                                   status="yes").last()
        return next_post

    def get_previous_post(self):
        """
        Переход к предыдущей статье
        """
        previous_post = Post.objects.filter(created__lt=self.created,
                                   status="yes").first()
        return previous_post
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField("Имя", max_length=50)
    email = models.EmailField("e-mail")
    text = models.TextField("Комментарий")
    created = models.DateTimeField("Создано", auto_now_add=True)
    updated = models.DateTimeField("Обновлено", auto_now=True)
    active = models.BooleanField("Отображать", default=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ('-created',)

    def __str__(self):
        return f"Комментарий от {self.name} в {self.created}"


class About(models.Model):
    updated = models.DateTimeField("Обновлено", auto_now=True)
    text = RichTextUploadingField("Обо мне")    

    class Meta:
        verbose_name = "Обо мне"
        verbose_name_plural = "Обо мне"
