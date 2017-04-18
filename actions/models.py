from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType      # 引入ContentType模型
from django.contrib.contenttypes.fields import GenericForeignKey    # 引入字段
# Create your models here.

class Action(models.Model):
    user = models.ForeignKey(User,
                             related_name='actions',
                             db_index=True,
                             verbose_name='用户')
    verb = models.CharField(max_length=255,
                            verbose_name='操作详情')     # 记录执行操作的动作描述
    target_ct = models.ForeignKey(ContentType,blank=True,
                                  null=True,
                                  related_name='target_obj')
    target_id = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            db_index=True) # 存储被关联对象的主键
    target = GenericForeignKey('target_ct','target_id') #
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True,
                                   verbose_name='执行时间') # 执行时间

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'user {} verb {}'.format(self.user,self.verb)

