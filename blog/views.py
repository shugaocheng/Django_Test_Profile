from django.shortcuts import render,get_object_or_404
from .models import Post
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import EmailPostForm
from django.core.mail import send_mail


# Create your views here.

def post_list_all(request):
    limit = 3
    object_list = Post.published.all()
    paginator = Paginator(object_list,limit)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/all_list.html',
                  {'posts':posts,
                   'page':page,
                   'object_list':object_list,
                   'section':'blog'})

def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post,slug=post,
                                 status = 'published',
                                 publish_time__year=year)
                                 # publish_time__month=month,
                                 # publish_time__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post':post})


def post_share(request,post_id):
    post = get_object_or_404(Post,id=post_id,status='published')
    sent = False  # 验证邮件发件状态
    to = None
    if request.method == 'POST':
        form = EmailPostForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.\
                format(cd['name'],cd['email'],post.title)
            message = 'Read "{}" at {} \n\n 发件人:{} \n 帖子内容:{}'.\
                format(post.title,post_url,cd['name'],cd['comments'])
            send_mail(subject,
                      message,
                      'shugaocheng@163.com',
                      [cd['to']])
            sent = True
            to = cd['to']
            messages.success(request,'邮件发送成功')
    else:
        form = EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,
                                                  'form':form,
                                                  'sent':sent,
                                                  'to':to})
