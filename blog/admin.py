from django.contrib import admin
from .models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','slug','author','publish_time','status']
    list_filter = ['status','created_time','publish_time','author']
    search_fields = ['title','body','author','slug']
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish_time'
    ordering = ['status','publish_time']
admin.site.register(Post,PostAdmin)