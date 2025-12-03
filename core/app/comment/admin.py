from django.contrib import admin
from .models import Comment

# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    date_hierarchy ='created_date'
    empty_value_display = '-empty-'
    list_display = ('name','post','approved','created_date')
    list_filter = ('post','approved')
    search_fields = ('name','post')