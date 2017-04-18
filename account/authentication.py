from django.contrib.auth.models import User

# 使用邮箱验证登录
class EmailAuthBackend(object):
    """
    Authenticate using e-mail account.
    """
    def authenticate(self,username=None,password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoseNotExist:
            return None

    def get_user(self,user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoseNotExist:
            return None
