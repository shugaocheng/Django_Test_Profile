from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,verbose_name='用户')               # 与User表进行一对一关联
    date_of_birth = models.DateTimeField(blank=True,null=True,verbose_name='时间')
    photo = models.ImageField(upload_to='users/%Y/%m/%d',blank=True,verbose_name='图片')    # 需要安装Pillow包

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username) # 返回User表的username字段


# 关注关系模型
class Contact(models.Model):
    user_from = models.ForeignKey(User,related_name='rel_from_set')     # 关注XX的用户
    user_to = models.ForeignKey(User,related_name='rel_to_set')         # 被关注的用户
    created = models.DateTimeField(auto_now_add=True,db_index=True)     # 关注时间

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from,self.user_to)

# 创建中介模型给多对多关系对象,粉丝or明星
User.add_to_class('following',
                  models.ManyToManyField(
                      'self',
                      through=Contact,
                      related_name='followers',
                      symmetrical=False))

