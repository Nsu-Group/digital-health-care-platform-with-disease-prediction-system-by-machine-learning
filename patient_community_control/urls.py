from django.urls import path

from .views import *

urlpatterns = [
    path('', community_home_view, name='community-home'),
    path('post/post-experience/', community_post_create_view, name='community-post-create'),
    path('post/<str:slug>/', community_post_detail_view, name='community-post-detail'),
    path('post/update/<str:slug>/', community_post_update_view, name='community-post-update'),
    path('post/delete/<str:slug>/', community_post_delete_view, name='community-post-delete'),
    path('post/like/<str:slug>/', community_post_like_view, name='community-post-like'),
    path('post/unlike/<str:slug>/', community_post_unlike_view, name='community-post-unlike'),
    path('post/comment/<str:slug>/', community_post_comment_view, name='community-post-comment'),
]
