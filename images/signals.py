from django.db.models.signals import m2m_changed # 信号函数
from django.dispatch import receiver
from .models import Image

# 将喜欢的总数赋值给total_likes,total_likes可以在任何地方调用
@receiver(m2m_changed,sender=Image.user_like.through)
def users_like_changed(sender,instance,**kwargs):
    instance.total_likes = instance.user_like.count()
    instance.save()