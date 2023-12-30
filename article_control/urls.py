from django.urls import path

from .views import *

urlpatterns = [
    path('', article_home_view, name='article-home'),

    path('post', post_article_view, name='post-article'),
    path('article/<str:slug>', article_details_view, name='article-details'),
    path('edit/<str:slug>', edit_article_view, name='edit-article'),
    path('delete/<str:slug>', delete_article_view, name='delete-article'),

    path('user/<str:pk>/', users_articles_view, name='users-articles'),
    path('category/<str:cat>/', category_articles_view, name='category-articles'),
    path('like-article/<str:pk>/', like_article_view, name='like-article'),
    path('unlike-article/<str:pk>/', unlike_article_view, name='unlike-article'),
    path('comment-article/<str:pk>/', comment_article_view, name='comment-article'),
]
