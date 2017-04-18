from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image
from django.http import HttpResponse,JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from actions.utils import create_action
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import redis
from django.conf import settings
# from ..common.decorators import ajax_required
# Create your views here.

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)
# 添加图片
@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            create_action(request.user,'保存图片标签',new_item)
            messages.success(request,'图片保存成功!')
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
    return render(request,'images/image/create.html',
                  {'section':'images',
                   'form':form})

# 查看图片详情
def image_detail(request,id,slug):
    image = get_object_or_404(Image,id=id,slug=slug)
    # 图片浏览总数
    # r.incr用来累加image.id 每次触发该视图就会累加一次
    total_views = r.incr('image:{}'.format(image.id))
    return render(request,'images/image/detail.html',
                  {'section':'images',
                   'image':image,
                   'total_views':total_views})

# 喜欢或取消
@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.user_like.add(request.user)
                create_action(request.user,'喜欢该图片',image)
            else:
                image.user_like.remove(request.user)
                create_action(request.user,'取消喜欢',image)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})

# 查看所有图片列表
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images,8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'images/image/list_ajax.html',
                      {'section':'images',
                       'images':images})
    return render(request,
                  'images/image/list.html',
                  {'section':'images',
                   'images':images})