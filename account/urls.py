from django.conf.urls import url
from . import views
# from django.contrib.auth.views import login,login_required,logout
# from django.contrib.auth.views import password_change,password_change_done
from django.contrib.auth import views as auth_views
urlpatterns = [
    # login views
    # url(r'^login/$',views.user_login,name='login'),
    # 使用authentication自带视图
    url(r'^login/$',auth_views.login,name='login'),
    url(r'^logout/$',auth_views.logout,name='logout'),
    url(r'^logout-then-login/$',auth_views.logout_then_login,name='logout_then_login'),
    url(r'^$',views.dashboard,name='dashboard'),
    url(r'^password-change/$','django.contrib.auth.views.password_change',name='password_change'),
    url(r'^password-change/done/$',auth_views.password_change_done,name='password_change_done'),
    url(r'^password-reset/$',auth_views.password_reset,name='password_reset'),
    url(r'^password-reset/done/$',auth_views.password_reset_done,name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        auth_views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^password-reset/complete/$',
        auth_views.password_reset_complete,
        name='password_reset_complete'),
    url(r'^register/$',views.register,name='register'),
    url(r'^edit/$',views.edit,name='edit'),
    url(r'^users/$',views.user_list,name='user_list'),
    url(r'^users/follow/$',views.user_follow,name='user_follow'),   # 必须放在detail之前,Django匹配URL模式只认到第一条就停止
    url(r'^users/(?P<username>[-\w]+)/$',views.user_detail,name='user_detail'),
    url(r'^all_job/$',views.zhaopin_all,name='zhaopin_all'),
]