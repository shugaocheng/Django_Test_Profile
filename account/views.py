from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login
from .forms import LoginForm,UserRegistrationForm,UserEditForm,ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile,Contact
from django.contrib import messages
from django.contrib.auth.models import User
from common.decorators import ajax_required
from actions.utils import create_action
from django.views.decorators.http import require_POST
from actions.models import Action
from .model import Job
from django.conf import settings
import redis
# Create your views here.
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)

# 登录认证视图
def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse('身份验证成功')
                else:
                    return HttpResponse('账户未启用')
            else:
                return HttpResponse('Invalid login')
    else:
        login_form = LoginForm()
    return render(request,'account/login.html',{'login_form':login_form})

# login_required会检查当前用户书否通过认证
# 没有通过验证会重定向到带有一个next参数的登录URL—>login
@login_required
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',flat=True)
    if following_ids:
        # actions = actions.filter(user_id=following_ids)
        # select_related()查询集:优化一对一或一对多查询
        # prefetch_related():优化多对多或多对一查询
        actions = actions.filter(user_id__in=following_ids).select_related('user','user__profile').prefetch_related('target')
    actions = actions[:]

    return render(request,
                  'account/dashboard.html',
                  {'section':'dashboard',
                   'actions':actions})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            messages.success(request,'注册成功')
            # 将保存的用户关联到Profile表 根据user字段
            profile = Profile.objects.create(user=new_user)
            create_action(new_user,'注册账号',new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user':new_user})
        else:
            messages.error(request,'注册失败')

    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form':user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # 两个表单对象不是模型模型实例,无法作为target参数传递
            create_action(request.user,'修改资料')
            # create_action(request.user,'修改资料',profile_form)
            messages.success(request,'保存成功')
        else:
            messages.error(request,'保存失败')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request,
                  'account/edit.html',
                  {'user_form':user_form,
                   'profile_form':profile_form})


def zhaopin_all(request):
    all_job = Job.objects.all()
    return render(request,
                  'account/job/all_job.html',
                  {'section':'zhaopin',
                   'all_job':all_job})
# 所有用户列表
@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,
                  'account/user/list.html',
                  {'section':'people',
                   'users':users})

# 用户详情页
@login_required
def user_detail(request,username):
    user = get_object_or_404(User,username=username,is_active=True)
    total_views = r.incr('user:{}'.format(user.id))
    return render(request,
                  'account/user/detail.html',
                  {'section':'people',
                   'user':user,
                   'total_views':total_views})


# 取消或关注
@ajax_required
@login_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user)
                create_action(request.user,'关注用户',user)
            else:
                Contact.objects.filter(
                    user_from=request.user,
                    user_to=user).delete()      # 多对多关系模型无法使用默认管理器的add或remove
                create_action(request.user,'取消关注',user)
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})