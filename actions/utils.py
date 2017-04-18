import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action

# 创建action新对象到数据库
# 在一分钟前没有进行操作返回True,如果对象呗创建了则返回FALSE
def create_action(user,verb,target=None):
    # action = Action(user=user,verb=verb,target=target)
    # action.save()
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id,
                                            verb=verb,
                                            created__gte=last_minute)
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        print('------------------------')
        print(type(ContentType))
        print('------------------------')
        similar_actions = similar_actions.filter(target_ct=target_ct,
                                                 target_id=target.id)
        print(type(similar_actions))
    if not similar_actions:
        action = Action(user=user,verb=verb,target=target)
        action.save()
        return True
    return False