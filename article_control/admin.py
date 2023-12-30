from django.contrib import admin
from .models import *


class ArticleCategoryModelAdmin(admin.ModelAdmin):
    list_display = ['category', 'created_at', 'updated_at']


class ArticleModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'created_at', 'updated_at']
    list_filter = ['author', 'category']
    search_fields = ['title', 'content']
    list_per_page = 10
    ordering = ['-created_at']
    raw_id_fields = ['author']
    date_hierarchy = 'created_at'


class ArticleCommentModelAdmin(admin.ModelAdmin):
    list_display = ['author', 'article', 'comment', 'created_at', 'updated_at']
    list_filter = ['author', 'article']
    search_fields = ['author', 'article']
    list_per_page = 10
    ordering = ['-created_at']
    raw_id_fields = ['author', 'article']
    date_hierarchy = 'created_at'


class ArticleLikeModelAdmin(admin.ModelAdmin):
    list_display = ['author', 'article', 'created_at', 'updated_at']
    list_filter = ['author', 'article']
    search_fields = ['author', 'article']
    list_per_page = 10
    ordering = ['-created_at']
    raw_id_fields = ['author', 'article']
    date_hierarchy = 'created_at'


admin.site.register(ArticleCategoryModel, ArticleCategoryModelAdmin)
admin.site.register(ArticleModel, ArticleModelAdmin)
admin.site.register(ArticleLikeModel, ArticleLikeModelAdmin)
admin.site.register(ArticleCommentModel, ArticleCommentModelAdmin)
