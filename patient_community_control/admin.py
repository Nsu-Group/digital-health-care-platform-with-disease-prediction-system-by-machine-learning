from django.contrib import admin
from .models import *


class CommunityPostModelAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "totalLikeCount",
        "totalCommentCount",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "title",
        "author",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    list_per_page = 30
    ordering = ("created_at",)


class CommunityPostCommentModelAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "post",
        "comment",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "author",
        "post",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    list_per_page = 30
    ordering = ("created_at",)


class CommunityPostLikeModelAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "post",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "author",
        "post",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    list_per_page = 30
    ordering = ("created_at",)


admin.site.register(CommunityPostModel, CommunityPostModelAdmin)
admin.site.register(CommunityPostLikeModel, CommunityPostLikeModelAdmin)
admin.site.register(CommunityPostCommentModel, CommunityPostCommentModelAdmin)
