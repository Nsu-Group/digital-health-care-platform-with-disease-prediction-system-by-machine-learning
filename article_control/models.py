from user_control.models import UserModel
from django.db import models


class ArticleCategoryModel(models.Model):
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Article Category'
        verbose_name_plural = 'Article Categories'


class ArticleModel(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(ArticleCategoryModel, null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField()
    image = models.ImageField(upload_to="images/article/", null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    totalViewCount = models.IntegerField(default=0, null=True, blank=True)
    totalLikeCount = models.IntegerField(default=0, null=True, blank=True)
    totalCommentCount = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + " by " + self.author.name

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'


class ArticleCommentModel(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Article Comment'
        verbose_name_plural = 'Article Comments'


class ArticleLikeModel(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Article Like'
        verbose_name_plural = 'Article Likes'
