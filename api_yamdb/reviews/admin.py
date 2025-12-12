from django.contrib import admin

from .models import Review, Comment

admin.site.empty_value_display = 'Не задано'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'pub_date',
        'review',
    )
    list_filter = ('author', 'pub_date', 'review')


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'pub_date',
        'score',
    )
    search_fields = (
        'title',
    )
    list_filter = ('author', 'pub_date', 'score')
    list_display_links = ('title',)


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
