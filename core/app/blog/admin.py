from django.contrib import admin
from .models import Post,Category
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    date_hierarchy ='created_date'
    empty_value_display = '-empty-'
    list_display = ('title','author','content_views','status','published_date','created_date',)
    list_filter = ('status',)
    search_fields = ('title','content')
    summernote_fields = ('content',)
    
admin.site.register(Category)
