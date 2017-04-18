from django.db import models
from django.conf import settings
from django.utils.text import slugify   # 导入slugify函数
from django.core.urlresolvers import reverse
# Create your models here.

class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='image_created')
    title = models.CharField(max_length=200)            # 图片标题
    slug = models.SlugField(max_length=200,blank=True)      # 图片标签
    url = models.URLField()                             # 图片源链接
    image = models.ImageField(upload_to='image/%Y/%m/%d')   # 图片文件
    description = models.TextField(blank=True)          # 图片描述 可选
    created = models.DateField(auto_now_add=True,       # 图片在数据库创建日期
                               db_index=True)
    # user.images_liked_all() image.user_like.all()
    user_like = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='images_liked',blank=True) # 标记喜欢的用户
    total_likes = models.PositiveIntegerField(db_index=True,default=0)  # 存储被用户喜欢的总数
    def __str__(self):
        return self.title

    # 重写Image模型的save()方法来自动生成slug字段,基于title字段的值
    def save(self, *args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super(Image,self).save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('images:detail',args=[self.id,self.slug])
