from django.contrib import admin
from .models import Image
from django.db.models import Count
# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title','slug','image','created','user','get_images_liked']
    list_filter = ['created']

    def get_images_liked(self,obj):
        counts = obj.user_like.all()
        users=[]
        for user in counts:
            users.append(user.username)
        return users
    get_images_liked.short_description = '喜欢这这张照片的用户'
admin.site.register(Image,ImageAdmin)