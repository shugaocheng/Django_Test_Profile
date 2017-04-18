from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
# Create your models here.

# 自定义manage管理器,继承models.Manage
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')

class Post(models.Model):
    objects = models.Manager()
    published = PublishedManager()
    STATUS_CHOICES = (
        ('drate','Drate'),
        ('published','Published')
    )
    title = models.CharField(max_length=250,verbose_name='文章标题')    # 博客标题
    slug = models.SlugField(max_length=250,     # 短标签,unique_for_date使该标签只能是唯一
                            unique_for_date='publish_time',verbose_name='文章短标签')
    author = models.ForeignKey(User,
                               related_name='blog_posts',verbose_name='作者')   # 一对一外键,关联User模型
    body = models.TextField(verbose_name='文章内容')                               # 文章内容
    publish_time = models.DateTimeField(default=timezone.now,verbose_name='发布日期')    # 日期,等于当前时间
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建日期')       # 创建日期
    updated_time = models.DateTimeField(auto_now=True,verbose_name='修改日期')           # 修改日期
    status = models.CharField(max_length=10,                # 状态
                              choices=STATUS_CHOICES,
                              default='drate',verbose_name='状态')
    recommend = models.BooleanField(default=False,verbose_name='推荐博文') #布尔字段，我用于标记是否是推荐博文


    def __str__(self):
        return 'author:{} publish_time:{} title:{}'.format(self.author,self.publish_time,self.title)

    class Meta:
        ordering = ('-publish_time',)

    # 自定义博客帖子绝对路径
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish_time.year,
                             self.publish_time.strftime('%m'),
                             self.publish_time.strftime('%d'),
                             self.slug])